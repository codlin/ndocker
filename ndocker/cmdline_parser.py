import os
import click
from click_ext import MyGroup
from click_ext import MyCommand
import click_ext

manage_cmds = {
    "host": "Manage host networks",
    "container": "Manage containers and networks"
}

host_cmds = {
    "create": "Create a new configuration file of host",
    "config": "Configure networks for host with a configuration file",
    "reset": "Delete the configured networks"
}

container_cmds = {
    "create": "Create a new configuration file of container",
    "restart": "Restart one or more containers",
    "rm": "Remove one or more containers",
    "run": "Run a command in a new container",
    "start": "Start one or more stopped containers",
    "stop": "Stop one or more running containers",
    "up": "Bring all containers up",
}

# groups
@click_ext.group(cls=MyGroup, help="A client for UTE to create containers and configure networks with openvswitch")
@click.version_option('1.0')
def cli():
    pass

@click_ext.group("host", cls=MyGroup, section='Manage Commands', help=manage_cmds.get('host'))
def host_cli():
    pass

@host_cli.command("create", help="Create a new configuration file of host")
def host_create():
    click.echo("I'm host.")

@click_ext.group("container", cls=MyGroup, section='Manage Commands', help=manage_cmds.get('container'))
def container_cli():
    click.echo("I'm container_cli.")

# commands for cli
@cli.command("create", cls=MyCommand, help=container_cmds.get('create'))
@click.argument('container')
@click.option('path', '--path', type=click.Path(exists=True), help="Path to a configuration file (default ~/.ndocker/)")
def cli_create(container, path):
    pass

@cli.command("restart", cls=MyCommand, help=container_cmds.get('restart'))
def cli_restart():
    pass

@cli.command("rm", cls=MyCommand, help=container_cmds.get('rm'))
def cli_rm():
    pass

@cli.command("run", cls=MyCommand, help=container_cmds.get('run'))
def cli_run():
    pass
    
@cli.command("start", cls=MyCommand, help=container_cmds.get('start'))
def cli_start():
    pass

@cli.command("stop", cls=MyCommand, help=container_cmds.get('stop'))
def cli_stop():
    pass

@cli.command("up", cls=MyCommand, help=container_cmds.get('up'))
def cli_up():
    pass

@container_cli.command()
@click.argument('container')
@click.option('path', '--path', type=click.Path(exists=True), help="Path to a configuration file (default ~/.ndocker/)")
def create(container, path):
    click.echo(container)

@container_cli.command()
def restart():
    click.echo("I'm restart.")

@container_cli.command(help='delete container')
@click.confirmation_option(prompt='All data will be lost, are you sure you want to delete?')
def rm():
    click.echo("I'm rm.")

@container_cli.command()
def run():
    click.echo("I'm run.")

@container_cli.command()
def start():
    click.echo("I'm start.")

@container_cli.command()
def stop():
    click.echo("I'm stop.")

@container_cli.command()
def up():
    click.echo("I'm up.")

cli.add_command(host_cli)
cli.add_command(container_cli)

if __name__ == '__main__':
    cli()