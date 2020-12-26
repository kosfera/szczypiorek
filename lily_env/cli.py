
from glob import glob
import os
import re

import click

from .parser import EnvParser
from .utils import load_yaml
from .git import assert_is_git_ignored
from .exceptions import BaseException
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
        f'{k}: {v}' for k, v in parser.get_env_variables().items()]))


@click.command()
@click.argument('directory')
def encrypt(directory):
    """Encrypt all yml files in a given directory."""

    filepaths = sorted(
        glob(os.path.join(directory, '*.yml')) +
        glob(os.path.join(directory, '*.yaml')))

    for filepath in filepaths:
        with open(filepath, 'r') as f:
            gpg_filepath = re.sub(r'(\.yml|\.yaml)', '.gpg', filepath)

            with open(gpg_filepath, 'w') as g:
                click.secho(f'[ENCRYPTING] {filepath}', color='green')

                try:
                    assert_is_git_ignored(filepath)

                    content = f.read()
                    # -- used here only to validate
                    load_yaml(content)
                    g.write(crypto.encrypt(content))

                except BaseException as e:
                    raise click.ClickException(e.args[0])


@click.command()
@click.argument('directory')
def decrypt(directory):
    for filepath in glob(os.path.join(directory, '*.gpg')):
        with open(filepath, 'r') as f:
            yml_filepath = filepath.replace('.gpg', '.yml')
            print('>>> filepath', filepath)
            print('>>> yml_filepath', yml_filepath)
            with open(yml_filepath, 'w') as g:
                click.secho(f'[DECRYPTING] {filepath}', color='green')

                try:
                    g.write(crypto.decrypt(f.read()))

                except BaseException as e:
                    raise click.ClickException(e.args[0])


@click.command()
def validate():
    pass


cli.add_command(encrypt)
cli.add_command(decrypt)
cli.add_command(validate)
cli.add_command(print_env)
