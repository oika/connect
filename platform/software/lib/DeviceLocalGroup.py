# -*- coding: utf-8 -*-


class DeviceLocalGroup:

    def __init__(self, tm_name, device_type, *thread_local_groups):
        self.__tm_name = tm_name
        self.__device_type = device_type
        self.__tlgs = tuple(thread_local_groups)
    
    @property
    def tm_name(self):
        return self.__tm_name
    
    @property
    def device_type(self):
        return self.__device_type
    
    @property
    def tlgs(self):
        return self.__tlgs

    def has_operator(self, operator):
        for tlg in self.__tlgs:
            for op in tlg.operators:
                if op is operator:
                    return True
        return False
