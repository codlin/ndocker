# pylint: disable=W0614
import time
from abc import ABCMeta, abstractmethod
from .networks import DockerNetworking
from .common.yamler import Yaml
from .common import logger
from .docker.docker_cmd import *
from necfg import *

class NE(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.networking = DockerNetworking()
    
    @abstractmethod
    def create_networks(self, **kwargs):
        raise NotImplementedError()

class Host(NE):
    def __init__(self, ymal_cfg):
        self.infos = Yaml(ymal_cfg).infos
    
    def create_networks(self, **kwargs):
        vswitches = self.infos.get('vswitches')
        for vswitch in vswitches:
            self.networking.create_bridge(vswitch.get('bridge_name'), vswitch.get('physicalport'))
    
    def reset_networks(self):
        vswitches = self.infos.get('vswitches')
        for vswitch in vswitches:
            self.networking.del_bridge(vswitch.get('bridge_name'))
        
class Container(NE):
    def __init__(self, yaml_cfg):
        self.cfg = ServicesCfg(yaml_cfg)
    
    def create_networks(self, **kwargs):
        for container in self.cfg.containers():
            infos = self.cfg.infos(container)
            i = 0
            for br_name, network in infos.networks.items():
                for info in network:
                    ip = info.get('ip')
                    tag = info.get('vtag')
                    gw = info.get('gw', False)
                    veth_name = "eth{}".format(i)
                    i += 1
                    self.networking.attach_container(container, br_name, veth_name, ip, tag, gw, txoff=(br_name == 'br-s1'))
    
    def create_service(self):
        docker = DockerCmd()
        for container in self.cfg.containers():
            if docker.isExist(container):
                logger.info('{} already exist.'.format(container))
                continue
            
            infos = self.cfg.infos(container)
            docker.pull(infos.image)

            cmd = "--name {} --hostname {} --net='none' {} --init --restart=always -e VNC_RESOLUTION={} {} --privileged -d {}".format(
                container, infos.hostname, '-p '.join(infos.ports), infos.vnc_resolution, infos.volumes, infos.image)
            docker.run(cmd)
            time.sleep(3)

            if not docker.isHealth(container):
                logger.info('Create {} failed.'.format(container))
                raise DockerCmdExecError()
        
        self.create_networks()
    
    def start_service(self):
        docker = DockerCmd()
        for container in self.cfg.containers():
            if not docker.isExist(container):
                logger.info('Container {} does not exist.'.format(container))
                raise DockerCmdExecError()
            
            docker.restart(container)
            time.sleep(3)

            if not docker.isHealth(container):
                logger.info('Create {} failed.'.format(container))
                raise DockerCmdExecError()
         
        self.create_networks()
    
    def stop_service(self):
        docker = DockerCmd()
        for container in self.cfg.containers():       
            docker.stop(container)
            infos = self.cfg.infos(container)
            i = 0
            for br_name, _ in infos.networks.items():
                self.networking.dettach_container(container, br_name, "eth{}".format(i))
                i += 1
    
    def rm_service(self):
        docker = DockerCmd()
