# DatasetHandler

## Introduction

DatasetHandler is a generic helper package for downloading datasets and performing any necessary preprocessing.
This CLI program provides two main commands: `download` and `extract`, enabling easy management of datasets.

```shell
$ datasets
Usage: datasets [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  download
  extract
```

## Performance

DatasetHandler leverages multiprocessing to significantly enhance performance by utilizing multiple CPU cores.
This parallel processing capability ensures **faster execution** of time-consuming tasks, making the tool **efficient for handling large datasets**.

### Key Areas Utilizing Multiprocessing:

- _Downloading Files_: The `download_multiprocess` function employs multiple processes to download files concurrently, reducing the time required to fetch large datasets from the internet.
- _Unarchiving Files_: The `unarchive_multiprocess` function unpacks multiple archive files simultaneously, speeding up the extraction process of downloaded data.
- _Extracting Images from Videos_: The `extract_multiprocess` function processes multiple video files in parallel to extract frames, which is especially useful for large collections of video data.

> By parallelizing these tasks, DatasetHandler ensures that data preparation steps are performed efficiently, saving valuable time and computational resources.

## Scripts

You can use the following script to run the cli in background

```shell
nohup bash bin/background.sh >> /data/logs/dataset_handler.log &
```

## Contributing

- We use poetry for managing dependencies, please make sure you have poetry installed.

```shell
poetry version
```

- Install the dependencies using `poetry`

```shell
poetry install --with dev
```

- Before you commit and push your changes please run the following

```shell
poetry run ruff check
poetry run ruff format
poetry run mypy
poetry run pytest
```

## TODO

- [documentation] Add badges to `README.md`.
- [refactor] Add error handling.
- [refactor] Add logging.
- [test] Try to minimize fixtures by using more of pytest-mock.
- [test] Increase code coverage to 40%.
- [fix] Triage why coverage data is different on certain versions of python
