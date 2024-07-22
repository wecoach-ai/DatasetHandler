import pathlib
import unittest

import pytest
import pytest_mock

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
    response: dict[str, pathlib.Path] = download.generate_download_meta_data(str(tmp_path), conftest.DOWNLOAD_URL)

    assert f"{conftest.DOWNLOAD_URL}/test_1.mp4" in set(response.keys())
    assert f"{conftest.DOWNLOAD_URL}/test_1.zip" in set(response.keys())
    assert f"{conftest.DOWNLOAD_URL}/game_1.mp4" in set(response.keys())
    assert f"{conftest.DOWNLOAD_URL}/game_1.zip" in set(response.keys())
    assert tmp_path / "test" / "videos" / "test_1.mp4" in set(response.values())
    assert tmp_path / "test" / "annotations" / "test_1.zip" in set(response.values())
    assert tmp_path / "train" / "videos" / "game_1.mp4" in set(response.values())
    assert tmp_path / "train" / "annotations" / "game_1.zip" in set(response.values())


def test__download_files(
    tmp_path: pathlib.Path,
    mocker: pytest_mock.MockerFixture,
    mock_httpx_stream: unittest.mock.MagicMock,
    mock_open_file: unittest.mock.MagicMock,
) -> None:
    download_file_path: pathlib.Path = tmp_path / "file.mp4"

    mock_response = mocker.MagicMock()
    mock_response.iter_bytes.return_value = conftest.CHUNKED_CONTENTS
    mock_httpx_stream.return_value.__enter__.return_value = mock_response

    download._download_files(conftest.DOWNLOAD_URL, download_file_path)

    mock_httpx_stream.assert_called_once_with("GET", conftest.DOWNLOAD_URL)
    mock_response.iter_bytes.assert_called_once()

    mock_open_file.assert_called_once_with(download_file_path, "wb")
    handler = mock_open_file()
    for chunk in conftest.CHUNKED_CONTENTS:
        handler.write.assert_any_call(chunk)


def test__unarchive_files(tmp_path: pathlib.Path, mock_shutil: unittest.mock.MagicMock) -> None:
    archive_file_path: pathlib.Path = tmp_path / "file.zip"

    download._unarchive_files(archive_file_path)

    mock_shutil.assert_called_once_with(archive_file_path, archive_file_path.with_suffix(""))


def test_clean_archive(tmp_path: pathlib.Path, mock_unlink: unittest.mock.MagicMock) -> None:
    dataset_file_list: list[pathlib.Path] = [tmp_path / "file.zip", tmp_path / "file.mp4"]

    download.clean_archive(dataset_file_list)

    mock_unlink.assert_called_once()


def test_download_multiprocess() -> None:
    assert True


def test_unarchive_multiprocess() -> None:
    assert True
