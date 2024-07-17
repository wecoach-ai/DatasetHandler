import click

from src.download import (
    download_multiprocess,
    generate_download_meta_data,
    setup_dataset_directory,
    unarchive_multiprocess,
)
from src.extract import extract_multiprocess, generate_extract_meta_data


@click.group()
def cli():
    pass


@cli.command()
@click.argument("download_url", required=True)
@click.argument("path", required=True)
def download(download_url, path):
    setup_dataset_directory(path)
    meta_data = generate_download_meta_data(path, download_url)

    download_multiprocess(meta_data)
    unarchive_multiprocess(meta_data)


@cli.command()
@click.argument("path", required=True)
def extract(path):
    meta_data = generate_extract_meta_data(path)
    extract_multiprocess(meta_data)


if __name__ == "__main__":
    cli()
