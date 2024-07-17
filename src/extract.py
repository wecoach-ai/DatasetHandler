import concurrent.futures
import json
import pathlib
import typing

import cv2


def generate_extract_meta_data(path: str) -> typing.List[pathlib.Path]:
    dataset_directory = pathlib.Path(path)
    train_video_directory = dataset_directory / "train" / "videos"
    test_video_directory = dataset_directory / "test" / "videos"

    result = [video_file for video_file in train_video_directory.iterdir()] + [
        video_file for video_file in test_video_directory.iterdir()
    ]

    for files in result:
        image_directory = files.parent.parent / "images" / files.with_suffix("").name
        image_directory.mkdir()

    return result


def extract_multiprocess(
    file_lists: typing.List[pathlib.Path], scope: str, frame_cutoff: int
):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        match scope:
            case "all":
                extract_fn = _extract_all_images
                args = file_lists
            case "selected":
                extract_fn = _extract_selected_images
                args = [(frame_cutoff, file_path) for file_path in file_lists]
            case "smooth":
                extract_fn = None

        executor.map(extract_fn, args)


def _extract_all_images(video_file_path: pathlib.Path):
    image_directory = (
        video_file_path.parent.parent / "images" / video_file_path.with_suffix("").name
    )

    capture = cv2.VideoCapture(str(video_file_path))

    counter = -1
    while True:
        flag, frame = capture.read()
        if not flag:
            break
        counter += 1
        image_path = image_directory / f"img_{counter:06d}.jpg"
        cv2.imwrite(image_path, frame)

    capture.release()


def _extract_selected_images(video_file_path: pathlib.Path, frame_cutoff: int):
    image_directory = (
        video_file_path.parent.parent / "images" / video_file_path.with_suffix("").name
    )
    events_annotations_file = (
        video_file_path.parent.parent
        / "annotations"
        / video_file_path.with_suffix("").name
        / "events_markup.json"
    )
    selected_indices = _get_frame_indices(events_annotations_file, frame_cutoff)

    capture = cv2.VideoCapture(str(video_file_path))

    counter = -1
    while True:
        flag, frame = capture.read()
        if not flag:
            break
        counter += 1
        if counter not in selected_indices:
            continue
        image_path = image_directory / f"img_{counter:06d}.jpg"
        cv2.imwrite(image_path, frame)

    capture.release()


def _get_frame_indices(file_path: pathlib.Path, num_frames: int) -> typing.Set[int]:
    result = set()

    with open(file_path, "r") as fp:
        events = json.load(fp)

    for frame_string in sorted(events.keys()):
        frame = int(frame_string)
        for index in range(frame - num_frames, frame + num_frames + 1):
            result.add(index)

    return result
