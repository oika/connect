# -*- coding: utf-8 -*-


class DataInterface:

    def __init__(self, mac_addr, ip_addr, port):
        self.__mac_addr = mac_addr
        self.__ip_addr = ip_addr
        self.__port = port
        self.__available = True

    @property
    def ip_addr(self):
        return self.__ip_addr

    @property
    def mac_addr(self):
        return self.__mac_addr

    @property
    def port(self):
        return self.__port

    @property
    def is_available(self):
        return self.__available

    def reserve(self):
        self.__available = False

    def release(self):
        self.__available = True
