import click

VERSION = '0.1'

@click.group()
@click.version_option(version=VERSION)
def terminal_client():
    pass


# terminal_client.add_command()