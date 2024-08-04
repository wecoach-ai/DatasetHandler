import pathlib

import click

from .download import (
    clean_archive,
    download_multiprocess,
    generate_download_meta_data,
    setup_dataset_directory,
    unarchive_multiprocess,
)
from .extract import extract_multiprocess, generate_extract_meta_data


@click.group()
def cli() -> None:
    """Command Line Interface for the data processing pipeline."""
    pass


@cli.command()
@click.argument("download_url", required=True)
@click.argument("path", required=True)
@click.option(
    "--cleanup/--no-cleanup",
    default=False,
    help="A flag to provide optionality for cleaning up of archived dataset (default=False)",
)
def download(download_url: str, path: str, cleanup: bool) -> None:
    """
    Download and unarchive dataset files.

    Args:

        download_url: The base URL for downloading dataset files.

        path: The local directory path to save the downloaded dataset files.
    """
    setup_dataset_directory(path)
    meta_data: dict[str, pathlib.Path] = generate_download_meta_data(path, download_url)

    download_multiprocess(meta_data)
    unarchive_multiprocess(meta_data)

    if cleanup:
        clean_archive(list(meta_data.values()))


@cli.command()
@click.argument("path", required=True)
@click.option(
    "--scope",
    type=click.Choice(["all", "selected", "smooth"], case_sensitive=False),
    default="all",
    help="Select the type of image extraction (default=all)",
)
@click.option("--frame-cutoff", type=int, default=9, help="Cutoff frames for selected/smooth type (default=9)")
def extract(path: str, scope: str, frame_cutoff: int) -> None:
    """
    Extract images from video files based on the specified scope and frame cutoff.

    Args:

        path: The local directory path containing the dataset.
    """
    meta_data: list[pathlib.Path] = generate_extract_meta_data(path)
    extract_multiprocess(meta_data, scope, frame_cutoff)


if __name__ == "__main__":
    cli()
