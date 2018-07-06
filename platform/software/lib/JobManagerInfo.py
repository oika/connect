# -*- coding: utf-8 -*-


class JobManagerInfo:

    def __init__(self, mac_addr, ip_addr, port):
        self.__mac_addr = mac_addr
        self.__ip_addr = ip_addr
        self.__port = port

    @property
    def mac_addr(self):
        return self.__mac_addr

    @property
    def ip_addr(self):
        return self.__ip_addr

    @property
    def port(self):
        return self.__port
