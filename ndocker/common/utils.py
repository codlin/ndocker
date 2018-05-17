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

import subprocess
import paramiko
import socket

import logger

def run(args):
    popen = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    popen.wait()

    return popen

def run_cmd(args):
    logger.info(args)
    p = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = []
    while True:
        line = p.stdout.readline()
        logger.info(line)
        out.append(line)
        if line == '' and p.poll() != None:
            break
    
    return ''.join(out)

class SshClient(object):
    def __init__(self, host, user, passwd, port=22):
        self._connect(host, port, user, passwd)

    def __del__(self):
        if self.ssh != None:
            self.ssh.close()

    def _connect(self, ip, port, user, passwd):
        self.ssh = paramiko.SSHClient()
        try:
            #self.ssh.load_system_host_keys()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            logger.info("{}:{}/{}".format(ip, user, passwd))
            self.ssh.connect(hostname=ip, port=port, username=user, password=passwd, timeout=20)
        except paramiko.AuthenticationException:
            self.ssh = None
            raise Exception("SSH Error: Authentication failed!")
        except socket.error:
            self.ssh = None
            raise Exception("SSH Error: Server is unreachable!")
        
    def run_cmd(self, command):
        logger.info(command)
        return self.ssh.exec_command(command)
    