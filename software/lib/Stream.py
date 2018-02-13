# -*- coding: utf-8 -*-

import socket
import pickle
from StreamingConf import StreamingConf


class RxNetworkStream:

    def __init__(self, address, data_port):
        self.address = address
        self.data_port = data_port

        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind((self.address, self.data_port))


    def get(self):
        data, addr = self.server.recvfrom(8192)
        return data


    def empty(self):
        return False
    
    
class TxNetworkStream:

    def __init__(self):
        self.dest_index = 0
        self.destination = []
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


    def add_dest(self, dest_address, dest_data_port):
        self.destination.append((dest_address, dest_data_port))


    def put(self, event):
        self.client.sendto(event, self.destination[self.dest_index])

        if self.dest_index == len(self.destination) - 1:
            self.dest_index = 0
        else:
            self.dest_index += 1


    def full(self):
        return False
