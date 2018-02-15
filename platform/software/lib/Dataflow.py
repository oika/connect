import networkx

class Dataflow(networkx.DiGraph):

    def __init__(self):
        super().__init__()
        self.interfaces = {}
    
    def add_edge(self, pre_op, pre_if, suc_op, suc_if):
        super().add_edge(pre_op, suc_op)
        self.interfaces[(pre_op, suc_op)] = (pre_if, suc_if)
