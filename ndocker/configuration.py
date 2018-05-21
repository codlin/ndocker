# pylint: disable=W0614
from common import logger
from common.utils import *
from common.yamler import Yaml

class ContainerCfg(object):
    def __init__(self, name, **kwargs):
        self.name = name
        
        for key in kwargs.keys():
            setattr(self, key, kwargs.get(key))
        
        self.hostname = kwargs.get('hostname', '{}-nj'.format(self.name))
        self.image = kwargs.get('image')
        self.volumes = kwargs.get('volumes')
        self.ports = kwargs.get('ports')
        self.networks = kwargs.get('networks')
        self.vnc_resolution = kwargs.get('vnc_resolution')
        
class ServicesCfg(object):
    def __init__(self, yaml_cfg):
        self.cfg = Yaml(yaml_cfg).infos
        self._verify_data()

        self.services = self.cfg['services']
        self.networks = self.cfg['networks']
    
    '''
    Return containers name in list.
    '''
    def containers(self):
        return self.services.keys()
    
    '''
    Return a container configration by an object of ContainerCfg
    '''
    def infos(self, container_name):
        if not self.services.has_key(container_name):
            logger.error('Unknown container name {}.'.format(container_name))
            return None
        
        container = self.cfg.services[container_name]
        container['networks'] = dict((i, self.networks[i]) for i in container['networks'])
        return ContainerCfg(container_name, **container)

    def _verify_data(self):
        pass