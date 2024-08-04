import concurrent.futures
import pathlib
import shutil

import httpx


def setup_dataset_directory(path: str) -> None:
    """
    Set up the necessary directory structure for the dataset.

    Args:
        path: The local directory path for the dataset.
    """
    directory: pathlib.Path = pathlib.Path(path)
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


def generate_download_meta_data(path: str, url: str) -> dict[str, pathlib.Path]:
    """
    Generate metadata for downloading dataset files.

    Args:
        path: The local directory path for the dataset.
        url: The base URL for downloading dataset files.

    Returns:
        A dictionary mapping download URLs to local file paths.
    """
    testing_meta_data: dict[str, pathlib.Path] = dict()
    training_meta_data: dict[str, pathlib.Path] = dict()

    for i in range(1, 8):
        testing_meta_data[f"{url}/test_{i}.zip"] = pathlib.Path(path) / "test" / "annotations" / f"test_{i}.zip"
        testing_meta_data[f"{url}/test_{i}.mp4"] = pathlib.Path(path) / "test" / "videos" / f"test_{i}.mp4"

    for i in range(1, 6):
        training_meta_data[f"{url}/game_{i}.zip"] = pathlib.Path(path) / "train" / "annotations" / f"game_{i}.zip"
        training_meta_data[f"{url}/game_{i}.mp4"] = pathlib.Path(path) / "train" / "videos" / f"game_{i}.mp4"

    return testing_meta_data | training_meta_data


def download_multiprocess(meta_data: dict[str, pathlib.Path]) -> None:
    """
    Download files using multiprocessing.

    Args:
        meta_data: A dictionary mapping download URLs to local file paths.
    """
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(_download_files, list(meta_data.keys()), list(meta_data.values()))


def _download_files(url: str, file_path: pathlib.Path) -> None:
    """
    Helper function to download a single file.

    Args:
        url: Download url for the dataset
        file_path: Local file path to download the data to.
    """
    print(f"Downloading data from {url=} and saving to {file_path=}")
    with httpx.stream("GET", url) as response, open(file_path, "wb") as fp:
        for chunk in response.iter_bytes():
            fp.write(chunk)


def unarchive_multiprocess(meta_data: dict[str, pathlib.Path]) -> None:
    """
    Unarchive downloaded files using multiprocessing.

    Args:

        meta_data: A dictionary mapping download URLs to local file paths.
    """
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(_unarchive_files, [item for item in list(meta_data.values()) if str(item).endswith(".zip")])


def _unarchive_files(archive_file_path: pathlib.Path) -> None:
    """
    Helper function to unarchive a single file.

    Args:

        archive_file_path: The path to the archive file to be unarchived.
    """
    unarchive_file_path: pathlib.Path = archive_file_path.with_suffix("")

    print(f"Unarchiving data from {archive_file_path=} and saving to {unarchive_file_path=}")
    shutil.unpack_archive(archive_file_path, unarchive_file_path)


def clean_archive(file_list: list[pathlib.Path]) -> None:
    """
    The function is used to clean up all the archived data.
    Saving memory resources, by deleting ".zip" files.

    Args:

        file_list: A list of local file paths, used to access ".zip" files.
    """
    for file_path in file_list:
        if str(file_path).endswith(".zip"):
            file_path.unlink()
