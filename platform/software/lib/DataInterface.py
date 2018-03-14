# -*- coding: utf-8 -*-


class DataInterface:

    def __init__(self, mac_addr, ip_addr, port):
        self.mac_addr = mac_addr
        self.ip_addr = ip_addr
        self.port = port
        self.available = True

    def get_ip_addr(self):
        return self.ip_addr

    def get_mac_addr(self):
        return self.mac_addr

    def get_port(self):
        return self.port

    def is_available(self):
        return self.available

    def reserve(self):
        self.available = False

    def release(self):
        self.available = True
