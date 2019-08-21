import click

from .type import type

VERSION = '0.1'

@click.group()
@click.version_option(version=VERSION)
def terminal_client():
    pass


terminal_client.add_command(type)