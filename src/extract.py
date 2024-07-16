import concurrent.futures
import pathlib
import typing

import cv2


def get_file_paths(path: str) -> typing.List[pathlib.Path]:
    dataset_directory = pathlib.Path(path)
    train_video_directory = dataset_directory / "train" / "videos"
    test_video_directory = dataset_directory / "test" / "videos"

    return [video_file for video_file in train_video_directory.iterdir()] + [
        video_file for video_file in test_video_directory.iterdir()
    ]


def extract_multiprocess(file_lists: typing.List[pathlib.Path]):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(_extract_images, file_lists)


def _extract_images(video_file_path: pathlib.Path):
    image_directory = video_file_path.parent.parent / "images"

    capture = cv2.VideoCapture(str(video_file_path))

    counter = -1
    while True:
        flag, frame = capture.read()
        if not flag:
            break
        counter += 1
        image_path = image_directory / f"img_{counter}.jpg"
        cv2.imwrite(image_path, frame)

    capture.release()
