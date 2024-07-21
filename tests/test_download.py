import pathlib

import pytest

from src import download
from tests import conftest


@pytest.mark.parametrize("path", conftest.DATASET_DIRECTORIES_NOT_EXISTS)
def test_setup_dataset_directory_not_exists(tmp_path: pathlib.Path, path: str) -> None:
    test_directory_path: pathlib.Path = tmp_path / path

    assert not test_directory_path.exists()

    download.setup_dataset_directory(str(test_directory_path))

    assert test_directory_path.exists()
    assert (test_directory_path / "test").exists()
    assert (test_directory_path / "test" / "annotations").exists()
    assert (test_directory_path / "test" / "images").exists()
    assert (test_directory_path / "test" / "videos").exists()


def test_setup_dataset_directory_exists(tmp_path: pathlib.Path) -> None:
    test_directory_path: pathlib.Path = tmp_path

    assert test_directory_path.exists()

    download.setup_dataset_directory(str(test_directory_path))

    assert test_directory_path.exists()
    assert (test_directory_path / "test").exists()
    assert (test_directory_path / "test" / "annotations").exists()
    assert (test_directory_path / "test" / "images").exists()
    assert (test_directory_path / "test" / "videos").exists()


def test_generate_download_meta_data(tmp_path: pathlib.Path) -> None:
    download_url = "https://example.com"

    response = download.generate_download_meta_data(str(tmp_path), download_url)

    assert type(response) is dict
    assert f"{download_url}/test_1.mp4" in set(response.keys())
    assert f"{download_url}/test_1.zip" in set(response.keys())
    assert f"{download_url}/game_1.mp4" in set(response.keys())
    assert f"{download_url}/game_1.zip" in set(response.keys())


def test__unarchive_files() -> None:
    assert True


def test_clean_archive() -> None:
    assert True
