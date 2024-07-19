import pathlib

import pytest

from src import download


@pytest.mark.parametrize("path", ["/tmp/test123/", "/tmp/test456/"])
def test_setup_dataset_directory_not_exists(path: str) -> None:
    test_directory_path: pathlib.Path = pathlib.Path(path)

    assert not test_directory_path.exists()

    download.setup_dataset_directory(path)

    assert test_directory_path.exists()
    assert (test_directory_path / "test").exists()
    assert (test_directory_path / "test" / "annotations").exists()
    assert (test_directory_path / "test" / "images").exists()
    assert (test_directory_path / "test" / "videos").exists()


@pytest.mark.parametrize("path", ["/tmp"])
def test_setup_dataset_directory_exists(path: str) -> None:
    test_directory_path: pathlib.Path = pathlib.Path(path)

    assert test_directory_path.exists()

    download.setup_dataset_directory(path)

    assert test_directory_path.exists()
    assert (test_directory_path / "test").exists()
    assert (test_directory_path / "test" / "annotations").exists()
    assert (test_directory_path / "test" / "images").exists()
    assert (test_directory_path / "test" / "videos").exists()


def test_generate_download_meta_data() -> None:
    assert True


def test__unarchive_files() -> None:
    assert True


def test_clean_archive() -> None:
    assert True
