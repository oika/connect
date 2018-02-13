# -*- coding: utf-8 -*-

class DeviceLocalGroup:
    
    def __init__(self, tm_name, device_type, *thread_local_groups):
        self.tm_name = tm_name
        self.device_type = device_type
        self.tlgs = list(thread_local_groups)
    
    def has_operator(self, operator):
        for tlg in self.tlgs:
            for op in tlg.operators:
                if op is operator:
                    return True
        return False
