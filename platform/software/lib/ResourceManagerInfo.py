# -*- coding: utf-8 -*-

class ResourceManagerInfo:

    def __init__(self, manager_address, manager_port):
        self.__manager_address = manager_address
        self.__manager_port = manager_port
    
    @property
    def manager_address(self):
        return self.__manager_address
    
    @property
    def manager_port(self):
        return self.__manager_port
