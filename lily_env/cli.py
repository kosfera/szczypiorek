
import click

from .parser import Env


@click.group()
def cli():
    """Expose multiple commands allowing one to work with lily_env."""
    pass


@click.command()
def dump():
    """
    Dump currently loaded env variables into a console.

    """

    print('\n'.join([
        f'{k.upper()}: {v}' for k, v in Env.from_dump().items()]))


cli.add_command(dump)
