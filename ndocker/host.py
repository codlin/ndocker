from .device import Device
from common.yamler import *

class Host(Device):
    def __init__(self, ymal_cfg):
        self.infos = Yaml(ymal_cfg).infos
    
    def create_networks(self, **kwargs):
        for info in self.infos:
            self.networking.create_bridge(info.get('bridge_name'), info.get('physicalport'))