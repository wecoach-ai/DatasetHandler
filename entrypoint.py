import click


@click.group()
def cli():
    pass


@cli.command()
@click.argument("download_url", required=True)
@click.argument("path", required=True)
@click.option("--hard/--no-hard", default=False, help="If the directory contents ahve to be removed before download (default=--no-hard)")
def download(download_url, path, hard):
    click.echo(f"Downlaoding the data set from {download_url} at {path}")
    click.echo(f"This command will wipe up the current dataset {hard}")


@cli.command()
def extract():
    pass


if __name__ == "__main__":
    cli()
