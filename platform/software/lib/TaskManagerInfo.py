# -*- coding: utf-8 -*-

from DataInterface import DataInterface


class TaskManagerInfo:

    def __init__(self, name, manager_mac, manager_address, manager_port,
                 device_type, slots, data_interfaces):
        self.__name = name
        self.__manager_address = manager_address
        self.__manager_mac = manager_mac
        self.__manager_port = manager_port
        self.__device_type = device_type
        self.__slots = slots
        self.__data_interfaces = []
        for interface in data_interfaces:
            mac_addr = interface['mac']
            ip_addr = interface['address']
            port = str(interface['port'])
            self.__data_interfaces.append(DataInterface(mac_addr, ip_addr, port))

    @property
    def name(self):
        return self.__name

    @property
    def manager_address(self):
        return self.__manager_address
    
    @property
    def manager_mac(self):
        return self.__manager_mac
    
    @property
    def manager_port(self):
        return self.__manager_port
    
    @property
    def device_type(self):
        return self.__device_type
    
    @property
    def slots(self):
        return self.__slots

    def reserve_data_interface(self):
        for interface in self.__data_interfaces:
            mac_addr = interface.mac_addr
            ip_addr = interface.ip_addr
            port = interface.port
            if interface.is_available:
                interface.reserve()
                return mac_addr, ip_addr, port
