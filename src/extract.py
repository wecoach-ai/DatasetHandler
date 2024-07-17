import concurrent.futures
import json
import pathlib
import typing

import cv2


def generate_extract_meta_data(path: str) -> typing.List[pathlib.Path]:
    """
    Generate metadata for extracting images from video files.

    Args:
        path: The local directory path containing the dataset.

    Returns:
        typing.List[pathlib.Path]: A list of video file paths to extract images from.
    """
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
    """
    Extract images from video files using multiprocessing.

    Args:
        file_lists: A list of video file paths to extract images from.
        scope: The type of image extraction ("all", "selected", "smooth").
        frame_cutoff: The cutoff frames for selected/smooth type extraction.
    """
    with concurrent.futures.ProcessPoolExecutor() as executor:
        match scope:
            case "all":
                extract_fn = _extract_all_images
                args = [file_lists]
            case "selected":
                extract_fn = _extract_selected_images
                args = [file_lists, [frame_cutoff for _ in range(len(file_lists))]]
            case "smooth":
                extract_fn = _extract_smooth_images
                args = [
                    file_lists,
                    [(frame_cutoff - 1) // 2 for _ in range(len(file_lists))],
                ]

        executor.map(extract_fn, *args)


def _extract_all_images(video_file_path: pathlib.Path):
    """
    Extract all frames from a video file and save them as images.

    Args:
        video_file_path: The path to the video file.
    """
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
    """
    Extract selected frames from a video file based on annotations (event_markup.json) and save them as images.

    Args:
        video_file_path: The path to the video file.
        frame_cutoff: The number of frames to include before and after each annotated event.
    """
    image_directory = (
        video_file_path.parent.parent / "images" / video_file_path.with_suffix("").name
    )
    events_annotations_file = (
        video_file_path.parent.parent
        / "annotations"
        / video_file_path.with_suffix("").name
        / "events_markup.json"
    )
    selected_indices = _get_frame_indices_selected(
        events_annotations_file, frame_cutoff
    )

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


def _extract_smooth_images(video_file_path: pathlib.Path, frame_cutoff: int):
    """
    Extract smooth labelled frames from a video file around annotated events and save them as images.

    Args:
        video_file_path: The path to the video file.
        frame_cutoff: The number of frames to include before and after each annotated event,
                            with a multiplier based on the event type.
    """
    image_directory = (
        video_file_path.parent.parent / "images" / video_file_path.with_suffix("").name
    )
    events_annotations_file = (
        video_file_path.parent.parent
        / "annotations"
        / video_file_path.with_suffix("").name
        / "events_markup.json"
    )
    selected_indices = _get_frame_indices_smooth(events_annotations_file, frame_cutoff)

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


def _get_frame_indices_selected(
    file_path: pathlib.Path, num_frames: int
) -> typing.Set[int]:
    """
    This function reads the event annotations from events_markup JSON file and generates a set of selected frame indices
    to extract. For each event at frame `f`, the function will include frames from `f-num_frames` to `f+num_frames`.

    Args:
        file_path: The path to the JSON file containing event annotations.
        num_frames: The number of frames to include before and after each annotated event.

    Returns:
        typing.Set[int]: A set of selected frame indices to extract.
    """
    result = set()

    with open(file_path, "r") as fp:
        events = json.load(fp)

    for frame_string in sorted(events.keys()):
        frame = int(frame_string)
        for index in range(frame - num_frames, frame + num_frames + 1):
            result.add(index)

    return result


def _get_frame_indices_smooth(
    file_path: pathlib.Path, num_frames: int
) -> typing.Set[int]:
    """
    This function reads the event annotations from events_markup JSON file and generates a set of smooth labelled
    frame indices to extract. For each event at frame `f`, function will include frames from `f-num_frames*multiplier`
    to `f+num_frames*multiplier`,where `multiplier` is 1 for "empty_event" and 2 for other events.

    Args:
        file_path: The path to the JSON file containing event annotations.
        num_frames: The number of frames to include before and after each annotated event.

    Returns:
        typing.Set[int]: A set of smooth labelled frame indices to extract.
    """
    result = set()

    with open(file_path, "r") as fp:
        events = json.load(fp)

    for frame_string in sorted(events.keys()):
        frame = int(frame_string)
        multiplier = 1 if events[frame_string] == "empty_event" else 2

        for index in range(
            frame - num_frames * multiplier, frame + num_frames * multiplier + 1
        ):
            result.add(index)

    return result
