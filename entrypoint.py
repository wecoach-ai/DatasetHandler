import click

from src import download as dwnld


@click.group()
def cli():
    pass


@cli.command()
@click.argument("download_url", required=True)
@click.argument("path", required=True)
def download(download_url, path):
    dwnld.setup_dataset_directory(path)
    meta_data = dwnld.generate_download_meta_data(path, download_url)
    dwnld.download_multiprocess(meta_data)


@cli.command()
def extract():
    pass


if __name__ == "__main__":
    cli()
