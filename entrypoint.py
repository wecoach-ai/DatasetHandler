import click


@click.group()
def cli():
    pass


@cli.command()
@click.argument("path", required=True)
@click.option("--hard/--no-hard", default=False)
def download(path, hard):
    click.echo(f"Downlaoding the data set at {path}")
    click.echo(f"This command will wipe up the current dataset {hard}")


@cli.command()
def extract():
    pass


if __name__ == "__main__":
    cli()
