#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import asyncore
import socket
import pickle
import importlib
import struct
import ipaddress
from ClusterInfo import ClusterInfo
from Commands import Commands


class JobManagerCommandHandler(asyncore.dispatcher):

    def __init__(self, svr_sock, job_manager):
        asyncore.dispatcher.__init__(self, sock=svr_sock)
        self.jm = job_manager
    
    
    def handle_read(self):
        data = self.recv(8192)
        if data:
            message = pickle.loads(data)
            command = message['cmd']
            job_name = message['job_name']

            if command == 'submit':
                job_file = message['job_file']
                self.jm.add_job(job_file, job_name)
            elif command == 'prepare':
                self.jm.prepare_job(job_name)
            elif command == 'run':
                self.jm.run_job(job_name)
            elif command == 'pause':
                self.jm.pause_job(job_name)
            elif command == 'cancel':
                self.jm.cancel_job(job_name)


class JobManager(asyncore.dispatcher):

    def __init__(self):
        asyncore.dispatcher.__init__(self)
        self.cluster_info = ClusterInfo()
        self.jobs = {}
        address = self.cluster_info.job_manager_info.address
        port = self.cluster_info.job_manager_info.port
        self.create_socket()
        self.set_reuse_addr()
        self.bind((address, port))
        self.listen(1)
    
    
    def handle_accepted(self, sock, addr):
        handler = JobManagerCommandHandler(sock, self)
    
    
    def add_job(self, job_file, job_name):
        # read job
        module_name = job_file.rstrip('.py')
        module = importlib.import_module(module_name)
        job = module.UserJob(job_name)

        # build job
        job.define_dataflow()

        # add job to JobManager's attributes
        self.jobs[job_name] = job

        nw_interfaces = {}
        for tm_name, dlg in job.dlgs.items():
            for tlg in dlg.tlgs:
                for op in tlg.operators:
                    for suc in job.df.successors(op):
                        if not dlg.has_operator(suc):
                            for d in job.dlgs.values():
                                if d.has_operator(suc):
                                    edge = (op, suc)
                                    indices = job.df.interfaces[edge]
                                    interface = (suc.name, indices[1])
                                    if not nw_interfaces.get(interface):
                                        data_addr, data_port = self.cluster_info\
                                                                   .task_manager_infos[d.tm_name]\
                                                                   .reserve_data_interface()
                                        nw_interfaces[interface] = (data_addr, data_port)
                    for pre in job.df.predecessors(op):
                        if not dlg.has_operator(pre):
                            for d in job.dlgs.values():
                                if d.has_operator(pre):
                                    edge = (pre, op)
                                    indices = job.df.interfaces[edge]
                                    interface = (op.name, indices[0])
                                    if not nw_interfaces.get(interface):
                                        data_addr, data_port = self.cluster_info\
                                                                   .task_manager_infos[tm_name]\
                                                                   .reserve_data_interface()
                                        nw_interfaces[interface] = (data_addr, data_port)

        # distribute tasks
        for dlg in job.dlgs.values():
            tm_addr = self.cluster_info.task_manager_infos[dlg.tm_name].manager_address
            tm_port = self.cluster_info.task_manager_infos[dlg.tm_name].manager_port
            if dlg.device_type == 'CPU':
                message = {'cmd': 'submit', 'job_file': job_file, 'job_name': job_name,\
                           'interface': nw_interfaces}
                self.__send_message(tm_addr, tm_port, message)
            elif dlg.device_type == 'FPGA':
                assert len(dlg.tlgs) == 1
                assert len(dlg.tlgs[0].operators) == 1
                op = dlg.tlgs[0].operators[0]
                logic_in_port = int(nw_interfaces[(op.name, 0)][1])
                if len(tuple(job.df.successors(op))) > 0:
                    suc = tuple(job.df.successors(op))[0]
                    suc_if_index = job.df.interfaces[(op, suc)][1]
                    dest_addr = nw_interfaces[(suc.name, suc_if_index)][0]
                    logic_out_port = int(nw_interfaces[(suc.name, suc_if_index)][1])
                else:
                    dest_addr = 0
                    logic_out_port = 0
                message = struct.pack('<I', Commands.submit) + struct.pack('<H', logic_in_port)\
                          + struct.pack('<H', logic_out_port)\
                          + struct.pack('<I', int(ipaddress.IPv4Address(dest_addr)))
                self.__send_message(tm_addr, tm_port, message, encoded=True, udp=True)
    
    
    def prepare_job(self, job_name):
        for dlg in self.jobs[job_name].dlgs.values():
            tm_addr = self.cluster_info.task_manager_infos[dlg.tm_name].manager_address
            tm_port = self.cluster_info.task_manager_infos[dlg.tm_name].manager_port
            if dlg.device_type is not 'FPGA':
                message = {'cmd': 'prepare', 'job_name': job_name}
                manager_port = self.cluster_info.task_manager_infos[dlg.tm_name].manager_port
                self.__send_message(tm_addr, tm_port, message)
            else:
                message = struct.pack('<I', Commands.prepare) + struct.pack('<I', 0)
                self.__send_message(tm_addr, tm_port, message, encoded=True, udp=True)
    
    
    def run_job(self, job_name):
        for dlg in self.jobs[job_name].dlgs.values():
            tm_addr = self.cluster_info.task_manager_infos[dlg.tm_name].manager_address
            tm_port = self.cluster_info.task_manager_infos[dlg.tm_name].manager_port
            if dlg.device_type is not 'FPGA':
                message = {'cmd': 'run', 'job_name': job_name}
                self.__send_message(tm_addr, tm_port, message)
            else:
                message = struct.pack('<I', Commands.run) + struct.pack('<I', 0)
                self.__send_message(tm_addr, tm_port, message, encoded=True, udp=True)


    def pause_job(self, job_name):
        for dlg in self.jobs[job_name].dlgs.values():
            tm_addr = self.cluster_info.task_manager_infos[dlg.tm_name].manager_address
            tm_port = self.cluster_info.task_manager_infos[dlg.tm_name].manager_port
            if dlg.device_type is not 'FPGA':
                message = {'cmd': 'pause', 'job_name': job_name}
                self.__send_message(tm_addr, tm_port, message)
            else:
                message = struct.pack('<I', Commands.pause) + struct.pack('<I', 0)
                self.__send_message(tm_addr, tm_port, message, encoded=True, udp=True)
    
    
    def cancel_job(self, job_name):
        for dlg in self.jobs[job_name].dlgs.values():
            tm_addr = self.cluster_info.task_manager_infos[dlg.tm_name].manager_address
            tm_port = self.cluster_info.task_manager_infos[dlg.tm_name].manager_port
            if dlg.device_type is not 'FPGA':
                message = {'cmd': 'cancel', 'job_name': job_name}
                self.__send_message(tm_addr, tm_port, message)
            else:
                message = struct.pack('<I', Commands.cancel) + struct.pack('<I', 0)
                self.__send_message(tm_addr, tm_port, message, encoded=True, udp=True)
        del(self.jobs[job_name])
      
    
    def __send_message(self, address, port, message, encoded=False, udp=False):
        if not encoded:
            message = pickle.dumps(message)
        if udp:
            client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            client_sock.sendto(message, (address, port))
        else:
            client_sock = socket.socket()
            client_sock.connect((address, port))
            client_sock.send(message)
            client_sock.close()
