import concurrent.futures
import json
import pathlib
import typing

import cv2
import numpy as np


def generate_extract_meta_data(path: str) -> list[pathlib.Path]:
    """
    Generate metadata for extracting images from video files.

    Args:

        path: The local directory path containing the dataset.

    Returns:

        A list of video file paths to extract images from.
    """
    dataset_directory: pathlib.Path = pathlib.Path(path)
    train_video_directory: pathlib.Path = dataset_directory / "train" / "videos"
    test_video_directory: pathlib.Path = dataset_directory / "test" / "videos"

    result: list[pathlib.Path] = [video_file for video_file in train_video_directory.iterdir()] + [
        video_file for video_file in test_video_directory.iterdir()
    ]

    for files in result:
        image_directory = files.parent.parent / "images" / files.with_suffix("").name
        image_directory.mkdir()

    return result


def extract_multiprocess(file_lists: list[pathlib.Path], scope: str, frame_cutoff: int) -> None:
    """
    Extract images from video files using multiprocessing.

    Args:

        file_lists: A list of video file paths to extract images from.

        scope: The type of image extraction ("all", "selected", "smooth").

        frame_cutoff: The cutoff frames for selected/smooth type extraction.
    """
    with concurrent.futures.ProcessPoolExecutor() as executor:
        args_count: int = len(file_lists)

        executor.map(
            _extract_images, file_lists, [frame_cutoff for _ in range(args_count)], [scope for _ in range(args_count)]
        )


def _extract_images(video_file_path: pathlib.Path, frame_cutoff: int, strategy: str) -> None:
    """
    This function reads the event annotations from a JSON file if the strategy is not "all".
    It generates a set of frame indices (by calling _get_frame_indices() func) to extract based on the annotations
    and the specified strategy. The extracted frames are saved as images in the "images" directory.

    Args:

        video_file_path: The path to the video file.

        frame_cutoff: The number of frames to include before and after each annotated event.
                      This is required only if the strategy is "selected" or "smooth".

        strategy:   The extraction strategy. Can be "all", "selected", or "smooth".
                    "all" extracts all frames.
                    "selected" extracts frames around annotated events.
                    "smooth" extracts frames around annotated events with smooth labelling.
    """
    image_directory: pathlib.Path = video_file_path.parent.parent / "images" / video_file_path.with_suffix("").name
    selected_indices: set[int]
    if strategy != "all":
        events_annotations_file: pathlib.Path = (
            video_file_path.parent.parent / "annotations" / video_file_path.with_suffix("").name / "events_markup.json"
        )
        selected_indices = _get_frame_indices(events_annotations_file, frame_cutoff, strategy)

    capture: cv2.VideoCapture = cv2.VideoCapture(str(video_file_path))

    counter: int = -1
    flag: bool
    frame: cv2.Mat | np.ndarray[typing.Any, np.dtype[np.integer[typing.Any] | np.floating[typing.Any]]]
    while True:
        flag, frame = capture.read()
        if not flag:
            break

        counter += 1
        if strategy != "all" and counter not in selected_indices:
            continue

        image_path: pathlib.Path = image_directory / f"img_{counter:06d}.jpg"
        cv2.imwrite(str(image_path), frame)

    capture.release()


def _get_frame_indices(file_path: pathlib.Path, num_frames: int, strategy: str) -> set[int]:
    """
    This function reads the event annotations from a JSON file and generates a set of frame indices to extract.
    For each event at frame `f`, the function will include frames from `f-num_frames*multiplier` to
    `f+num_frames*multiplier`, where `multiplier` is determined based on the strategy and event type.

    Args:

        file_path: The path to the JSON file(events_markup) containing event annotations.

        num_frames: The number of frames to include before and after each annotated event.

        strategy: The extraction strategy. Can be "selected" or "smooth".
                  "selected" includes frames directly around the annotated event.
                  "smooth" applies a multiplier based on the event type.

    Returns:

        A set of frame indices to extract, covering the range around each annotated event.
    """
    multiplier: int
    result: set[int] = set()

    with open(file_path, "r") as fp:
        events: dict[str, str] = json.load(fp)

    for frame_string in sorted(events.keys()):
        frame: int = int(frame_string)

        if strategy == "selected":
            multiplier = 1

        if strategy == "smooth":
            multiplier = 1 if events[frame_string] == "empty_event" else 2

        for index in range(frame - num_frames * multiplier, frame + num_frames * multiplier + 1):
            result.add(index)

    return result
