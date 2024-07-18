# DatasetHandler

## Introduction

DatasetHandler is a generic helper package for downloading datasets and performing any necessary preprocessing. 
This CLI program provides two main commands: `download` and `extract`, enabling easy management of datasets.

```shell
$ python entrypoint.py
Usage: entrypoint.py [OPTIONS] COMMAND [ARGS]...

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

- Before running this CLI make sure you have an appropriate version of python interpreter installed.

```shell
python -V
```

- Create a virtual env

```shell
python -m venv env
source env/bin/activate
pip install --upgrade pip
```

- Install the dependencies from `requirements.txt`

```shell
pip install --requirement requirements.txt
```
## TODO

- [documentation] Add badges to `README.md`.