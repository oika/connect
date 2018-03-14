# -*- coding: utf-8 -*-

from DataInterface import DataInterface


class TaskManagerInfo:

    def __init__(self, name, manager_mac, manager_address, manager_port,
                 device_type, slots, data_interfaces):
        self.name = name
        self.manager_address = manager_address
        self.manager_mac = manager_mac
        self.manager_port = manager_port
        self.device_type = device_type
        self.slots = slots
        self.data_interfaces = []
        for interface in data_interfaces:
            mac_addr = interface['mac']
            ip_addr = interface['address']
            port = str(interface['port'])
            self.data_interfaces.append(DataInterface(mac_addr, ip_addr, port))

    def reserve_data_interface(self):
        for interface in self.data_interfaces:
            mac_addr = interface.get_mac_addr()
            ip_addr = interface.get_ip_addr()
            port = interface.get_port()
            if interface.available:
                interface.reserve()
                return mac_addr, ip_addr, port
