from ydk.errors import YError
from ydk.path import Repository
from ydk.filters import YFilter

from ydk.gnmi.providers import gNMIServiceProvider
from ydk.gnmi.services import gNMIService
from ydk.models.openconfig import openconfig_interfaces

# test vars
debug = True
repo = './models'
port = 6030
username = 'yangconf'
password = '_my_c00l_pass_'

# setup logging
if debug: 
    import logging
    logger = logging.getLogger("ydk")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(("%(asctime)s - %(name)s - %(levelname)s - %(message)s "))
    handler.setFormatter(formatter)
    logger.addHandler(handler)


# provider setup
def create_provider(repository, host, port, username, password):
    return gNMIServiceProvider(repo=repository, address=host, port=port, username=username, password=password)


# interface funsies 
def create_interface_config(provider, port_name, port_desc, port_ip, port_cidr):    
    # create a service
    gnmi_service = gNMIService()

    # create the object model instance
    interface = openconfig_interfaces.Interfaces.Interface()
    # set the name
    interface.name = port_name
    interface.config.name = interface.name
    interface.config.description = port_desc
    interface.config.enabled = True
    subinterface = interface.subinterfaces.Subinterface()
    subinterface.index = 0
    subinterface.config.index = 0
    subinterface.ipv4 = subinterface.Ipv4()
    address = subinterface.ipv4.Addresses.Address()
    address.ip = port_ip
    address.config.ip = address.ip
    address.config.prefix_length = port_cidr
    subinterface.ipv4.addresses.address.append(address)
    interface.subinterfaces.subinterface.append(subinterface)
    
    # configure the action type in gnmi
    interface.yfilter = YFilter.update

    # do stuff
    try: 
        ok = gnmi_service.set(provider, interface)
        return ok
    except YError as errm: 
        print('An Error occurred whilst creating the interface: {}'.format(errm))
     

if __name__ == "__main__":
    # setup shit
    repository = Repository(repo)
    spine1_sp = create_provider(repository, '192.168.77.11', port, username, password)
    spine2_sp = create_provider(repository, '192.168.77.12', port, username, password)

    # do shit
    # spine 1
    s1_l1_ok = create_interface_config(spine1_sp, 'Ethernet1', 'Leaf1 Port', '169.254.11.1', 30)
    if s1_l1_ok: 
        print("Spine1 Leaf1: ok")
    else:
        print("Spine1 Leaf1: nok")
    s1_l2_ok = create_interface_config(spine1_sp, 'Ethernet2', 'Leaf2 Port', '169.254.12.1', 30)
    if s1_l2_ok: 
        print("Spine1 Leaf2: ok")
    else:
        print("Spine1 Leaf2: nok")
    
    # spine 2
    s2_l1_ok = create_interface_config(spine2_sp, 'Ethernet1', 'Leaf1 Port', '169.254.21.1', 30)
    if s2_l1_ok: 
        print("Spine2 Leaf1: ok")
    else:
        print("Spine2 Leaf1: nok")
    s2_l2_ok = create_interface_config(spine2_sp, 'Ethernet2', 'Leaf2 Port', '169.254.22.1', 30)
    if s2_l2_ok: 
        print("Spine2 Leaf2: ok")
    else:
        print("Spine2 Leaf2: nok")
    exit()

                                                                                                                                            
