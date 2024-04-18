import numpy as np
from Flow import FlowNw
import time

g1 = FlowNw(8)
arcs = np.loadtxt('network1.txt', skiprows=2, delimiter=";")
for u, v, ca, cost in arcs:
    g1.add_edge(int(u) - 1, int(v) - 1, capacity=ca, cost=cost)
str_tm = time.time()
g1.update_balance(0, 40)
g1.update_balance(7, -40)
g1.min_cost_flow()
end_tm = time.time()
run_time = end_tm - str_tm

print("The computation took %0.5f seconds" % run_time)
