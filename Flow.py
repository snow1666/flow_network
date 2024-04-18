from implement import ek, sshp
from collections import defaultdict


class FlowNw:

    def __init__(self, vertices):
        self.V = vertices
        self.edge = defaultdict(dict)
        self.b = dict()

    def add_edge(self, u, v, cost=0, capacity=float('inf')):
        self.edge[u][v] = {'cost': cost, 'flow': capacity}
        self.edge[v][u] = {'cost': -cost, 'flow': 0}

    def add_flow(self, u, v, f):
        self.edge[u][v]['flow'] -= f
        self.edge[v][u]['flow'] = f

    def add_balance(self, b):
        self.b = b

    def update_balance(self, node, value):
        self.b[node] = value

    def max_flow(self, src, tar, method='ek'):
        if method == "ek":
            return ek(self, src, tar)

    def min_cost_flow(self):
        return sshp(self)

