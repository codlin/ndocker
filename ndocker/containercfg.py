# pylint: disable=W0614
from common.utils import *
from common.yamler import Yaml

class Service(object):
    def __init__(self, service, **kwargs):
        self.service = service
        for key in kwargs.keys():
            setattr(self, key, kwargs.get(key))
        
        set_value_or_use_default(self, 'hostname', '{}-nj'.format(hostname), **kwargs)
        set_value_or_raise_exception(self, 'image', **kwargs)
        
class ContainerCfg(object):
    def __init__(self, yaml_cfg):
        self.cfg = Yaml(yaml_cfg)
        self.networks = self.cfg.networks

    def containers(self):
        return self.cfg.services.keys()
    
    def infos(self, container_name):
        cfgs = self.cfg.services['container_name']
        s = Service(cfgs)

    def _verify_data(self):
        pass