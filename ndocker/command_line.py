# pylint: disable=W0614
import os
import click
from common.click_ext import MyGroup
from common.click_ext import MyCommand
from common import click_ext
from cmds import *

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

container_opts = {
    "path": "Path to a configuration file (default {})".format(DEFAULT_CONFIGURATION_PATH)
}

# groups
@click_ext.group(cls=MyGroup, help="A client for UTE to create containers and configure networks with openvswitch")
@click.version_option('1.0')
def cli(): #be equaivalent to: cli = click_ext.group(**attrs)(cli)
    pass

@click_ext.group("host", cls=MyGroup, section='Manage Commands', help=manage_cmds.get('host'))
def host_cli():
    pass

@click_ext.group("container", cls=MyGroup, section='Manage Commands', help=manage_cmds.get('container'))
def container_cli():
    pass

# commands for host
@host_cli.command("create", help=host_cmds.get('create'))
@click.argument('filename')
@click.option('path', '--path', type=click.Path(exists=True), help=container_opts.get('path'))
def host_create(filename, path):
    create_host_cfg(filename, path)

@host_cli.command("config", help=host_cmds.get('config'))
@click.argument('filename')
@click.option('path', '--path', type=click.Path(exists=True), help=container_opts.get('path'))
def host_config(filename, path):
    click.echo("I'm host.")

@host_cli.command("reset", help=host_cmds.get('reset'))
@click.confirmation_option(prompt='All networks will be lost, are you sure you want to delete?')
@click.argument('filename')
@click.option('path', '--path', type=click.Path(exists=True), help=container_opts.get('path'))
def host_reset(filename, path):
    click.echo("I'm host.")

# commands for cli
@cli.command("create", cls=MyCommand, help=container_cmds.get('create'))
@click.argument('container')
@click.argument('device', type=click.Choice(['fzm', 'fzc']))
@click.option('path', '--path', type=click.Path(exists=True), help=container_opts.get('path'))
def cli_create(container, device, path):
    create_container_cfg(container, device, path)

@cli.command("restart", cls=MyCommand, help=container_cmds.get('restart'))
@click.argument('container')
@click.option('path', '--path', type=click.Path(exists=True), help=container_opts.get('path'))
def cli_restart(container, path):
    pass

@cli.command("rm", cls=MyCommand, help=container_cmds.get('rm'))
@click.confirmation_option(prompt='All data will be lost, are you sure you want to delete?')
@click.argument('container')
def cli_rm(container):
    pass

@cli.command("run", cls=MyCommand, help=container_cmds.get('run'))
@click.argument('path', type=click.Path(exists=True))
def cli_run(path):
    pass
    
@cli.command("start", cls=MyCommand, help=container_cmds.get('start'))
@click.argument('container')
@click.option('path', '--path', type=click.Path(exists=True), help=container_opts.get('path'))
def cli_start(container, path):
    pass

@cli.command("stop", cls=MyCommand, help=container_cmds.get('stop'))
@click.argument('container')
def cli_stop(container):
    pass

@cli.command("up", cls=MyCommand, help=container_cmds.get('up'))
@click.option('path', '--path', type=click.Path(exists=True), help=container_opts.get('path'))
def cli_up(path):
    pass

# commands for container_cli
@container_cli.command("create", help=container_cmds.get('create'))
@click.argument('container')
@click.argument('device', type=click.Choice(['fzm', 'fzc']))
@click.option('path', '--path', type=click.Path(exists=True), help=container_opts.get('path'))
def container_create(container, device, path):
    create_container_cfg(container, device, path)

@container_cli.command("restart", help=container_cmds.get('restart'))
@click.argument('container')
@click.option('path', '--path', type=click.Path(exists=True), help=container_opts.get('path'))
def container_restart(container, path):
    pass

@container_cli.command("rm", help=container_cmds.get('rm'))
@click.confirmation_option(prompt='All data will be lost, are you sure you want to delete?')
@click.argument('container')
def container_rm(container):
    pass

@container_cli.command("run", help=container_cmds.get('run'))
@click.argument('path', type=click.Path(exists=True))
def container_run(path):
    pass
    
@container_cli.command("start", help=container_cmds.get('start'))
@click.argument('container')
@click.option('path', '--path', type=click.Path(exists=True), help=container_opts.get('path'))
def container_start(container, path):
    pass

@container_cli.command("stop", help=container_cmds.get('stop'))
@click.argument('container')
def container_stop(container):
    pass

@container_cli.command("up", help=container_cmds.get('up'))
@click.option('path', '--path', type=click.Path(exists=True), help=container_opts.get('path'))
def container_up(path):
    pass

cli.add_command(host_cli)
cli.add_command(container_cli)

if __name__ == '__main__':
    cli()