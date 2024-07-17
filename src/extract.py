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
        args_count = len(file_lists)

        executor.map(
            _extract_images,
            file_lists,
            [frame_cutoff for _ in range(args_count)],
            [scope for _ in range(args_count)],
        )


def _extract_images(video_file_path: pathlib.Path, frame_cutoff: int, strategy: str):
    image_directory = (
        video_file_path.parent.parent / "images" / video_file_path.with_suffix("").name
    )
    selected_indices = set()
    if strategy != "all":
        events_annotations_file = (
            video_file_path.parent.parent
            / "annotations"
            / video_file_path.with_suffix("").name
            / "events_markup.json"
        )
        selected_indices = _get_frame_indices(
            events_annotations_file, frame_cutoff, strategy
        )

    capture = cv2.VideoCapture(str(video_file_path))

    counter = -1
    while True:
        flag, frame = capture.read()
        if not flag:
            break

        counter += 1
        if strategy != "all" and counter not in selected_indices:
            continue

        image_path = image_directory / f"img_{counter:06d}.jpg"
        cv2.imwrite(image_path, frame)

    capture.release()


def _get_frame_indices(
    file_path: pathlib.Path, num_frames: int, strategy: str
) -> typing.Set[int]:
    result = set()

    with open(file_path, "r") as fp:
        events = json.load(fp)

    for frame_string in sorted(events.keys()):
        frame = int(frame_string)

        if strategy == "selected":
            multiplier = 1

        if strategy == "smooth":
            multiplier = 1 if events[frame_string] == "empty_event" else 2

        for index in range(
            frame - num_frames * multiplier, frame + num_frames * multiplier + 1
        ):
            result.add(index)

    return result
