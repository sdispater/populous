import click

from .loader import load_yaml
from .blueprint import Blueprint


@click.group()
@click.version_option()
def cli():
    pass


@cli.command()
@click.argument('files', nargs=-1)
def predict(files):
    """
    Predict how many objects will be created if the given files are used.
    """
    blueprint = Blueprint.from_description(load_yaml(*files))

    for item in blueprint.items:
        click.echo("{name}: {count} {by}".format(
            name=item.name, count=item.count.number,
            by="by {}".format(item.count.by) if item.count.by else ""
        ))
