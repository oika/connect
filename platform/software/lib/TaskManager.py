#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import importlib
import time
import asyncore
import pickle
from TaskManagerInfo import TaskManagerInfo
from StreamingConf import StreamingConf
from Stream import TxNetworkStream, RxNetworkStream
from TaskProcess import TaskProcess
import multiprocessing


class TaskManagerCommandHandler(asyncore.dispatcher):

    def __init__(self, sock, task_manager):
        asyncore.dispatcher.__init__(self, sock)
        self.tm = task_manager

    def handle_read(self):
        data = self.recv(8192)
        if data:
            message = pickle.loads(data)
            command = message['cmd']

            if command == 'submit':
                job_file = message['job_file']
                job_name = message['job_name']
                nw_interfaces = message['interface']
                self.tm.add_job(job_file, job_name, nw_interfaces)
            elif command == 'prepare':
                job_name = message['job_name']
                self.tm.prepare_tasks(job_name)
            elif command == 'run':
                job_name = message['job_name']
                self.tm.run_tasks(job_name)
            elif command == 'pause':
                job_name = message['job_name']
                self.tm.pause_tasks(job_name)
            elif command == 'cancel':
                job_name = message['job_name']
                self.tm.cancel_tasks(job_name)


class TaskManager(asyncore.dispatcher):

    def __init__(self, hostname):
        asyncore.dispatcher.__init__(self)
        self.info = self.__get_task_manager_info(hostname)
        self.jobs = {}
        self.processes = {}

        self.create_socket()
        self.set_reuse_addr()
        addr = self.info.manager_address
        port = self.info.manager_port
        self.bind((addr, port))
        self.listen(1)

    def handle_accepted(self, sock, address):
        handler = TaskManagerCommandHandler(sock, self)

    def __get_task_manager_info(self, name):
        conf = StreamingConf('cluster.yaml')
        manager_addr = conf.get_tm_address(name)
        manager_mac = conf.get_tm_mac(name)
        manager_port = conf.get_tm_port(name)
        device_type = conf.get_tm_device_type(name)
        slots = conf.get_tm_slots(name)
        data_interfaces = conf.get_tm_data_interfaces(name)
        info = TaskManagerInfo(name, manager_mac, manager_addr, manager_port,\
                               device_type, slots, data_interfaces)
        return info

    def add_job(self, job_file, job_name, nw_interfaces):
        # read job
        module_name = job_file.rstrip('.py')
        module = importlib.import_module(module_name)
        job = module.UserJob(job_name)

        # build job
        job.define_dataflow()

        # add job and tasks to TaskManager's attributes
        self.jobs[job.name] = job
        self.processes[job_name] = []
        dlg = job.get_device_local_group(self.info.name)
        self.__attach_streams(job.df, dlg, nw_interfaces)

    def __attach_internal_stream(self, pre, suc, df):
        interface = (pre, suc)
        out_if_index = df.interfaces[interface][0]
        in_if_index  = df.interfaces[interface][1]
        
        if not suc.in_streams.get(in_if_index):
            stream = multiprocessing.Queue()
            suc.in_streams[in_if_index] = stream
        pre.out_streams[out_if_index] = suc.in_streams[in_if_index]

    def __attach_tx_stream(slef, pre, suc, df, nw_interfaces):
        edge = (pre, suc)
        index = df.interfaces[edge][0]
        dest_index = df.interfaces[edge][1]
        if not pre.out_streams.get(index):
            dest_address = nw_interfaces[(suc.name, dest_index)][0]
            dest_data_port = int(nw_interfaces[(suc.name, dest_index)][1])
            stream = TxNetworkStream()
            stream.add_dest(dest_address, dest_data_port)
            pre.out_streams[index] = stream

    def __attach_rx_stream(self, pre, suc, df, nw_interfaces):
        edge = (pre, suc)
        index = df.interfaces[edge][1]
        if not suc.in_streams.get(index):
            address = nw_interfaces[(suc.name, index)][0]
            data_port = int(nw_interfaces[(suc.name, index)][1])
            stream = RxNetworkStream(address, data_port)
            suc.in_streams[index] = stream

    def __attach_streams(self, df, dlg, nw_interfaces):
        for tlg in dlg.tlgs:
            for op in tlg.operators:
                for suc in df.successors(op):
                    if dlg.has_operator(suc):
                        self.__attach_internal_stream(op, suc, df)
                    elif not dlg.has_operator(suc):
                        self.__attach_tx_stream(op, suc, df, nw_interfaces)
                for pre in df.predecessors(op):
                    if not dlg.has_operator(pre):
                        self.__attach_rx_stream(pre, op, df, nw_interfaces)

    def prepare_tasks(self, job_name):
        tlgs = self.jobs[job_name].dlgs[self.info.name].tlgs
        for tlg in tlgs:
            for op in tlg.operators:
                op.prepare()
            process = TaskProcess(tlg, multiprocessing.Event())
            self.processes[job_name].append(process)
            process.start()

    def run_tasks(self, job_name):
        self.__start_processes(job_name)

    def pause_tasks(self, job_name):
        self.__stop_processes(job_name)
        for process in self.processes[job_name]:
            for op in process.tlg.operators:
                op.pause()

    def cancel_tasks(self, job_name):
        self.__stop_processes(job_name)
        for process in self.processes[job_name]:
            for op in process.tlg.operators:
                op.cancel()
            process.terminate()
        for process in self.processes[job_name]:
            process.join()
        del(self.jobs[job_name])
        del(self.processes[job_name])

    def __start_processes(self, job_name):
        for process in self.processes[job_name]:
            process.running.set()

    def __stop_processes(self, job_name):
        for process in self.processes[job_name]:
            process.running.clear()
