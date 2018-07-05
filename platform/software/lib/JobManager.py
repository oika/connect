# -*- coding: utf-8 -*-

import socket
import pickle
import importlib
import struct
import ipaddress
import asyncio
from Commands import Commands


class JobManager:

    def __init__(self, cluster_info, logger):
        self.cluster_info = cluster_info
        self.logger = logger
        self.jobs = {}
        self.rm_addr = self.cluster_info.resource_manager_info.manager_address
        self.rm_port = self.cluster_info.resource_manager_info.manager_port

    def add_job(self, job_file, job_name):
        self.logger.info("Adding job {}:{}.".format(job_file, job_name))

        # read job
        global dst_mac
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
                                        data_mac, data_addr, data_port = self.cluster_info\
                                                .task_manager_infos[d.tm_name]\
                                                .reserve_data_interface()
                                        nw_interfaces[interface] = (data_addr, data_port, data_mac)
                    for pre in job.df.predecessors(op):
                        if not dlg.has_operator(pre):
                            for d in job.dlgs.values():
                                if d.has_operator(pre):
                                    edge = (pre, op)
                                    indices = job.df.interfaces[edge]
                                    interface = (op.name, indices[0])
                                    if not nw_interfaces.get(interface):
                                        data_mac, data_addr, data_port = self.cluster_info\
                                                .task_manager_infos[tm_name]\
                                                .reserve_data_interface()
                                        nw_interfaces[interface] = (data_addr, data_port, data_mac)

        # distribute tasks
        for dlg in job.dlgs.values():
            tm_addr = self.cluster_info.task_manager_infos[dlg.tm_name].manager_address
            tm_port = self.cluster_info.task_manager_infos[dlg.tm_name].manager_port
            if dlg.device_type == 'CPU':
                message = {'cmd': 'submit', 'job_file': job_file, 'job_name': job_name,
                           'interface': nw_interfaces}
                self.__send_message(tm_addr, tm_port, message)
            elif dlg.device_type == 'FPGA':
                assert len(dlg.tlgs) == 1
                assert len(dlg.tlgs[0].operators) == 1
                op = dlg.tlgs[0].operators[0]
                device = dlg.tm_name
                bitfile = op.bitfile
                req = 'wrbit'
                param = {'device': device, 'bitfile': bitfile}
                message = {'req': 'program', 'param': param}
                ret_message = self.__send_and_wait_message(self.rm_addr, self.rm_port, message)
                if ret_message == 'Success':
                    self.logger.info("Wrote bitstream {} to {}".format(bitfile, device))
                else:
                    # Currently ResourceManager only returns 'Success'
                    pass
                logic_in_port = int(nw_interfaces[(op.name, 0)][1])
                if len(tuple(job.df.successors(op))) > 0:
                    suc = tuple(job.df.successors(op))[0]
                    suc_if_index = job.df.interfaces[(op, suc)][1]
                    dst_mac = nw_interfaces[(suc.name, suc_if_index)][2]
                    dst_addr = nw_interfaces[(suc.name, suc_if_index)][0]
                    logic_out_port = int(nw_interfaces[(suc.name, suc_if_index)][1])
                else:
                    dst_addr = 0
                    dst_mac = 0
                    logic_out_port = 0
                dst_mac_array = dst_mac.split(':')
                message = struct.pack('<I', Commands.submit) + struct.pack('<H', logic_in_port)\
                    + struct.pack('<H', logic_out_port)\
                    + struct.pack('<I', int(ipaddress.IPv4Address(dst_addr)))\
                    + struct.pack('BBBBBB', int(dst_mac_array[0], 16),
                                  int(dst_mac_array[1], 16),
                                  int(dst_mac_array[2], 16),
                                  int(dst_mac_array[3], 16),
                                  int(dst_mac_array[4], 16),
                                  int(dst_mac_array[5], 16))
                self.__send_message(tm_addr, tm_port, message, encoded=True, udp=True)

        self.logger.info("Finished adding job {}:{}.".format(job_file, job_name))

    def prepare_job(self, job_name):
        self.logger.info("Preparing job {}.".format(job_name))
        for dlg in self.jobs[job_name].dlgs.values():
            tm_addr = self.cluster_info.task_manager_infos[dlg.tm_name].manager_address
            tm_port = self.cluster_info.task_manager_infos[dlg.tm_name].manager_port
            if dlg.device_type is not 'FPGA':
                message = {'cmd': 'prepare', 'job_name': job_name}
                self.__send_message(tm_addr, tm_port, message)
            else:
                message = struct.pack('<I', Commands.prepare) + struct.pack('<I', 0)
                self.__send_message(tm_addr, tm_port, message, encoded=True, udp=True)

    def run_job(self, job_name):
        self.logger.info("Running job {}.".format(job_name))
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
        self.logger.info("Pausing job {}.".format(job_name))
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
        self.logger.info("Cancelling job {}.".format(job_name))
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

    def __send_and_wait_message(self, address, port, message, encoded=False, udp=False):
        if not encoded:
            message = pickle.dumps(message)
        client_sock = socket.socket()
        client_sock.connect((address, port))
        client_sock.send(message)
        message = client_sock.recv(1024).decode()
        return message
