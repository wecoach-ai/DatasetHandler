import concurrent.futures
import pathlib
import shutil
import typing

import httpx


def setup_dataset_directory(path: str):
    directory = pathlib.Path(path)
    if not directory.exists():
        directory.mkdir(parents=True)
    dataset_directories = [
        directory / "test" / "annotations",
        directory / "test" / "images",
        directory / "test" / "videos",
        directory / "train" / "annotations",
        directory / "train" / "images",
        directory / "train" / "videos",
    ]
    for item in dataset_directories:
        item.mkdir(parents=True, exist_ok=True)


def generate_download_meta_data(path: str, url: str) -> typing.Dict[str, pathlib.Path]:
    training_annotations = {
        f"{url}/game_{i}.zip": pathlib.Path(path)
        / "train"
        / "annotations"
        / f"game_{i}.zip"
        for i in range(1, 6)
    }
    training_videos = {
        f"{url}/game_{i}.mp4": pathlib.Path(path) / "train" / "videos" / f"game_{i}.mp4"
        for i in range(1, 6)
    }

    testing_annotations = {
        f"{url}/test_{i}.zip": pathlib.Path(path)
        / "test"
        / "annotations"
        / f"test_{i}.zip"
        for i in range(1, 8)
    }
    testing_videos = {
        f"{url}/test_{i}.mp4": pathlib.Path(path) / "test" / "videos" / f"test_{i}.mp4"
        for i in range(1, 8)
    }

    return training_annotations | testing_annotations | training_videos | testing_videos


def download_multiprocess(meta_data: typing.Dict[str, pathlib.Path]):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(_download_files, list(meta_data.items()))


def _download_files(data: typing.Tuple[str, pathlib.Path]):
    url, file_path = data

    print(f"Downloading data from {url=} and saving to {file_path=}")
    with httpx.stream("GET", url) as response, open(file_path, "wb") as fp:
        for data in response.iter_bytes():
            fp.write(data)


def unarchive_multiprocess(meta_data: typing.Dict[str, pathlib.Path]):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(
            _unarchive_files,
            [item for item in list(meta_data.values()) if str(item).endswith(".zip")],
        )


def _unarchive_files(archive_file_path: pathlib.Path):
    unarchive_file_path = archive_file_path.with_suffix("")
    shutil.unpack_archive(archive_file_path, unarchive_file_path)
