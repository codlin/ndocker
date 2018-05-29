import os
import sys
import shutil
from ne import Host
from ne import Container

root = os.path.join(os.path.dirname(os.path.abspath(__file__)))
data = os.path.join(root, 'data')
DEFAULT_CONFIGURATION_PATH = "~/.ndocker/"

def create_host_cfg(filename, dest):
    if not filename.endswith('.yaml'):
        filename = '{}.yaml'.format(filename)
    
    _create_configration(filename, 'host', dest)

def create_container_cfg(container, device, dest):
    if len(container) > 5:
        print "The length of container name too long, should be <= 5."
        sys.exit(1)
    
    filename = '{}_EDITTHISPART.yaml'.format(container)
    _create_configration(filename, device, dest)

def _create_configration(filename, ne_type, dest):
    if ne_type not in [ f[:-5] for f in os.listdir(data) if os.path.isfile(os.path.join(data,f)) ]:
        print 'Unsupport device: {}'.format(ne_type)
        sys.exit(1)
    
    if dest is None:
        dest = DEFAULT_CONFIGURATION_PATH
    subdir = 'containers' if ne_type != 'host' else 'host'
    dest = os.path.join(dest, subdir)
    if not os.path.exists(dest):
        os.makedirs(dest)
    
    template = os.path.join(data, '{}.yaml'.format(ne_type))
    dest = os.path.join(dest, filename)
    shutil.copy(template, dest)
    print "Create configration file at: {}".format(dest)

def _verify_file(func):
    def wrapper(filename, path):
        if path is None:
            path = DEFAULT_CONFIGURATION_PATH
        
        filename = os.path.join(path, filename)
        if not os.path.exists(filename):
            print "Configuration file doesn't exist at {}".format(filename)
            sys.exit(1)
        
        func(filename, path)
    return wrapper

@_verify_file
def config_host(filename, path):
    host = Host(filename)
    host.create_networks()

@_verify_file
def reset_host(filename, path):  
    host = Host(filename)
    host.reset_networks()

def restart_container(container, path):
    pass