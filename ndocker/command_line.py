# pylint: disable=W0614
import os
import argparse

cmds = {
    ('host', 'Manage host networks'),
    ('container', 'Manage containers'),
}

subcmds = {
    ('create'),
}

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file {} does not exist!".format(arg))
    else:
        return arg

def _add_subcmd(parser, cmd, cmdhelp):
    subparser = parser.add_parser(cmd, help=cmdhelp)
    subparser.add_argument('--file', '-f', type=lambda x: is_valid_file(parser, x), required=True, default='cfg.yaml', help='jenkins configure file')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage='%(prog)s COMMAND', 
                                     description="ndocker: create container and confiure networks",
                                     epilog="Run 'ndocker COMMAND --help' for more information on a command.") 

    subparsers = parser.add_subparsers(dest='deploy_type', help='commands help')
    subparser.add_argument_group('Management Commands:')
    for cmd in cmds:
        _add_subcmd(subparsers, cmd[0], cmd[1])

    args = parser.parse_args()
    #print args

