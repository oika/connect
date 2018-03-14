# -*- coding: utf-8 -*-

import socket
import pickle
from StreamingConf import StreamingConf


class RxNetworkStream:

    def __init__(self, address, data_port):
        self.address = address
        self.data_port = data_port
        conf = StreamingConf('cluster.yaml')
        self.bundling = conf.get_network_bundling()
        self.event_bundle = []

        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind((self.address, self.data_port))

    def get(self):
        if len(self.event_bundle) == 0:
            data, addr = self.server.recvfrom(8192)
            if data:
                self.event_bundle = pickle.loads(data)
            else:
                return None
        return self.event_bundle.pop(0)
    
    def empty(self):
        if len(self.event_bundle) == 0:
            data, addr = self.server.recvfrom(8192)
            if data:
                self.event_bundle = pickle.loads(data)
                return False
            else:
                return True
        else:
            return False


class TxNetworkStream:

    def __init__(self):
        self.dest_index = 0
        self.destination = []
        conf = StreamingConf('cluster.yaml')
        self.bundling = conf.get_network_bundling()
        self.event_bundle = []
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def add_dest(self, dest_address, dest_data_port):
        self.destination.append((dest_address, dest_data_port))

    def put(self, val, packed=False):
        if packed:
            assert self.bundling == 1
            self.client.sendto(val, self.destination[self.dest_indnex])
        else:
            self.event_bundle.append(val)
            if len(self.event_bundle) == self.bundling:
                self.client.sendto(pickle.dumps(self.event_bundle),\
                                   self.destination[self.dest_index])
                self.event_bundle.clear()

        if self.dest_index == len(self.destination) - 1:
            self.dest_index = 0
        else:
            self.dest_index += 1

    def full(self):
        if len(self.event_bundle) == self.bundling:
            return True
        else:
            return False
