# -*- coding: utf-8 -*-

class TaskManagerInfo:

  def __init__(self, name, manager_address, manager_port, device_type, slots, data_interfaces):
    self.name = name
    self.manager_address = manager_address
    self.manager_port = manager_port
    self.device_type = device_type
    self.slots = slots
    self.data_interfaces = {}
    for interface in data_interfaces:
      address = interface['address']
      port = str(interface['port'])
      self.data_interfaces[address + ':' + port] = True # True means available


  def reserve_data_interface(self):
    for interface in self.data_interfaces:
      #address = interface['address']
      #port = str(interface['port'])
      address = interface.split(':')[0]
      port = interface.split(':')[1]
      if self.data_interfaces[address + ':' + port]:
        self.data_interfaces[address + ':' + port] = False
        return (address, port)


