import typing
import unittest

import pytest


DATASET_DIRECTORIES_NOT_EXISTS = ["dir1", "dir2"]
CHUNKED_CONTENTS = [b"chunk1", b"chunk2"]
DOWNLOAD_URL = "https://example.com"


@pytest.fixture
def mock_httpx_stream() -> typing.Generator[unittest.mock.MagicMock, None, None]:
    with unittest.mock.patch("httpx.stream") as mocked_stream:
        yield mocked_stream


@pytest.fixture
def mock_open_file() -> typing.Generator[unittest.mock.MagicMock, None, None]:
    with unittest.mock.patch("builtins.open", unittest.mock.mock_open()) as mocked_file:
        yield mocked_file


@pytest.fixture
def mock_shutil() -> typing.Generator[unittest.mock.MagicMock, None, None]:
    with unittest.mock.patch("shutil.unpack_archive") as mocked_unarchive:
        yield mocked_unarchive


@pytest.fixture
def mock_unlink() -> typing.Generator[unittest.mock.MagicMock, None, None]:
    with unittest.mock.patch("pathlib.Path.unlink") as mocked_unlink:
        yield mocked_unlink
