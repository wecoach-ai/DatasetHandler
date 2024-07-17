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
    """Command Line Interface for the data processing pipeline."""
    pass


@cli.command()
@click.argument("download_url", required=True)
@click.argument("path", required=True)
def download(download_url, path):
    """
    Download and unarchive dataset files.

    Args:
        download_url (str): The base URL for downloading dataset files.
        path (str): The local directory path to save the downloaded dataset files.
    """
    setup_dataset_directory(path)
    meta_data = generate_download_meta_data(path, download_url)

    download_multiprocess(meta_data)
    unarchive_multiprocess(meta_data)


@cli.command()
@click.argument("path", required=True)
@click.option(
    "--scope",
    type=click.Choice(["all", "selected", "smooth"], case_sensitive=False),
    default="all",
    help="Select the type of image extraction (default=all)",
)
@click.option(
    "--frame-cutoff",
    type=int,
    default=9,
    help="Cutoff frames for selected/smooth type (default=9)",
)
def extract(path, scope, frame_cutoff):
    """
    Extract images from video files based on the specified scope and frame cutoff.

    Args:
        path (str): The local directory path containing the dataset.
        scope (str): The type of image extraction ("all", "selected", "smooth").
        frame_cutoff (int): The cutoff frames for selected/smooth type extraction. (default=9)
    """
    meta_data = generate_extract_meta_data(path)
    extract_multiprocess(meta_data, scope, frame_cutoff)


if __name__ == "__main__":
    cli()
