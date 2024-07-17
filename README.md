# DatasetHandler

This is a generic package for downloading the data set and any other pre processing required.
As a cli this program provides 2 commands.

```shell
$ python entrypoint.py
Usage: entrypoint.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  download
  extract
```

## Pre-Requisites

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

- Implement archive cleanup after download
