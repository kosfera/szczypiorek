
from glob import glob
import os

import click

from .parser import EnvParser
from .utils import yaml_is_valid
from .git import assert_is_git_ignored
from . import crypto


@click.group()
def cli():
    """Expose multiple commands allowing one to work with lily_env."""
    pass


@click.command()
def print_env():
    """Print currently loaded env variables into stdout."""

    parser = EnvParser()
    click.echo('\n'.join([
        f'{k.upper()}: {v}' for k, v in parser.env_variables.items()]))


@click.command()
@click.argument('directory')
def encrypt(directory):
    """Encrypt all yml files in a given directory."""

    for filepath in glob(os.path.join(directory, '*.yml')):
        with open(filepath, 'r') as f:
            with open(filepath.replace('yml', 'gpg'), 'w') as g:
                content = f.read()
                yaml_is_valid(content)
                g.write(crypto.encrypt(content))

            click.secho(f'[ENCRYPTING] {filepath}', color='green')

            assert_is_git_ignored(filepath)


@click.command()
@click.argument('directory')
def decrypt(directory):
    for filepath in glob(os.path.join(directory, '*.gpg')):
        with open(filepath, 'r') as f:
            with open(filepath.replace('gpg', 'yml'), 'w') as g:
                g.write(crypto.decrypt(f.read()))

            click.secho(f'[DECRYPTING] {filepath}', color='green')

            assert_is_git_ignored(filepath)


@click.command()
def validate():
    pass


cli.add_command(encrypt)
cli.add_command(decrypt)
cli.add_command(validate)
cli.add_command(print_env)
