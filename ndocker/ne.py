# pylint: disable=W0614
from abc import ABCMeta, abstractmethod
from .networks import DockerNetworking
from .common.yamler import Yaml

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

class UTE(NE):
    def __init__(self, yaml_cfg):
        self.cfg = Yaml(yaml_cfg)
    
    def create_networks(self, **kwargs):
        container_name = self.cfg.services
        networks = self.infos.get('networks')
        i = 0
        for item in networks:
            br_name = item.get('bridge')
            network = item.get('network')
            for info in network:
                ip = info.get('ip')
                tag = info.get('vtag')
                gw = False if not info.has_key('gw') else info.get('gw')
                veth_name = "eth{}".format(i)
                i += 1
                self.networking.config_container(container_name, br_name, veth_name, ip, tag, gw, txoff=(br_name == 'br-s1'))