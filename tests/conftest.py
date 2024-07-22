import typing
import unittest

import pytest


DATASET_DIRECTORIES_NOT_EXISTS = ["dir1", "dir2"]


@pytest.fixture
def mock_httpx_stream() -> typing.Generator[unittest.mock.MagicMock, None, None]:
    with unittest.mock.patch("httpx.stream") as mocked_stream:
        yield mocked_stream


@pytest.fixture
def mock_open_file() -> typing.Generator[unittest.mock.MagicMock, None, None]:
    with unittest.mock.patch("builtins.open", unittest.mock.mock_open()) as mocked_file:
        yield mocked_file
