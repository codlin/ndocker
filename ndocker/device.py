from abc import ABCMeta, abstractmethod
from .networks import DockerNetworking


class Device(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.networking = DockerNetworking()
    
    @abstractmethod
    def create_networks(self, **kwargs):
        raise NotImplementedError()
