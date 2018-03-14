# -*- coding: utf-8 -*-


class JobManagerInfo:

    def __init__(self, mac_addr, ip_addr, port):
        self.mac_addr = mac_addr
        self.ip_addr = ip_addr
        self.port = port

    def get_mac_addr(self):
        return self.mac_addr

    def get_ip_addr(self):
        return self.ip_addr

    def get_port(self):
        return self.port
