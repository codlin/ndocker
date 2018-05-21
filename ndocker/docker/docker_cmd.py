# Copyright (C) 2018  Sean Z <sean.z.ealous@gmail.com>

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import shlex
import netaddr
from distutils.spawn import find_executable

rootpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, rootpath)
# pylint: disable=no-name-in-module,import-error
from rootpath.common.parser import line_parser
from rootpath.common.utils import run
from rootpath.common import logger

INSTALLED_DOCKER = find_executable('docker')

class DockerCmd(object):
    def __init__(self):    
        self.docker_path = INSTALLED_DOCKER

    def execute(self, command, parser=line_parser, ignore_errcode=False):
        # Constructs command.
        args = [self.docker_path]
        args.extend(shlex.split(command))

        # Executes command.
        # pylint: disable=undefined-variable
        process = run(args)
        if (process.returncode != 0) and (not ignore_errcode):
            raise DockerCmdExecError(process.stderr.read())

        # If parser is specified, applies parser and returns it.
        if parser:
            try:
                if process.returncode != 0:
                    return parser(process.stderr.read())
                else:
                    return parser(process.stdout.read())
            except Exception as e:  # pylint: disable=invalid-name
                raise DockerCmdParseError(e)

        # Returns outputs in str type.
        return process
    
    def pull(self, img):
        self.execute("pull {}".format(img))

    def run(self, args):
        result = self.execute("run {}".format(args))
        return result
    
    def stop(self, containers):
        cmd = "stop {}".format(" ".join(containers))
        self.execute(cmd)
    
    def start(self, containers):
        cmd = "start {}".format(" ".join(containers))
        self.execute(cmd)

    def restart(self, containers):
        cmd = "restart {}".format(" ".join(containers))
        self.execute(cmd)
    
    def rm(self, containers):
        cmd = "rm {}".format(" ".join(containers))
        self.execute(cmd)
    
    def ps(self, args=""):
        return self.execute("ps {}".format(args))
    
    def isExist(self, container):
        res = self.ps("-a --format '{{.Names}}' ")
        if container not in '\n'.join(res):
            logger.info('Container {} does not exist.'.format(container))
            return False
        
        return True
    
    def isHealth(self, container):
        res = self.ps("--filter status=running  --filter 'name={}$' ".format(container))
        if ' {}'.format(container) not in '\n'.join(res):
            logger.info('Container {} is not in health.'.format(container))
            return False
        
        return True

    def nspid(self, container):
        cmd = "inspect -f '{{.State.Pid}}' {}".format(container)
        nspid = self.execute(cmd).replace('\n', '')
        return nspid
    
class DockerCmdExecError(Exception):
    """
    Raised exception when 'ovs-vsctl' command returns non-zero exit code.
    """

class DockerCmdParseError(Exception):
    """
    Raised exception when fails to parse the outputs of 'ovs-vsctl' command.
    """