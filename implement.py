import numpy as np
from collections import deque

# Bellman-Ford algorithm for finding the shortest paths in digraph with negative weights
def bf(nw, src, tar):
    dist = [float('inf')] * nw.V  # initialize distance
    dist[src] = 0
    pred = [None] * nw.V  # initialize predecessor
    pred[src] = src
    stp = [tar]  # initialize ShP
    u_p = float('inf')

    for i in range(nw.V):
        for u in nw.edge:
            for v in nw.edge[u]:
                if nw.edge[u][v]['flow'] > 0:
                    w = nw.edge[u][v]['cost']
                    if dist[u] + w < dist[v]:

                        # Check for negative-weight cycles.
                        if i == nw.V - 1:
                            print("Graph contains a negative-weight cycle.")
                            return 0, None
                        dist[v] = dist[u] + w
                        pred[v] = u

    while stp[0] != src and stp[0] is not None and dist[tar] != float('inf'):
        current_node = stp[0]
        pre_node = pred[current_node]
        # print(pre_node)
        u_p = min(u_p, nw.edge[pre_node][current_node]['flow'])
        stp.insert(0, pred[stp[0]])

    return dist[tar], stp, u_p


# Breadth-first search
def bfs(graph, src, tar):
    # Initialize a queue for BFS and a dictionary to track the path.
    queue = deque([(src, [src], float('inf'))])
    visited = set()
    while queue:
        current_node, path, u_p = queue.popleft()

        if current_node == tar:
            return path, u_p  # Return the first path found to the destination.

        if current_node not in visited:
            visited.add(current_node)

            # Enqueue neighbors with the extended path.
            for neighbor in graph.edge[current_node]:
                ca = graph.edge[current_node][neighbor]['flow']
                if neighbor not in visited and ca > 0:
                    # print(neighbor, list(np.array(path + [neighbor])+1), min(u_p, ca))
                    queue.append((neighbor, path + [neighbor], min(u_p, ca)))

    return None  # If no path is found, return None.

def ek(nw, src, tar):    # Edmonds-Karp algorithm
    f = 0
    bfs_result = bfs(nw, src, tar)
    while bfs_result:
        path, u_p = bfs_result
        print(list(np.array(path) + 1), u_p)
        for u, v in zip(path, path[1:]):
            nw.add_flow(u, v, u_p)
        f += u_p
        bfs_result = bfs(nw, src, tar)
    return f, nw


def sshp(nw):

    '''Shortest Successive Path algorithm for finding the minimum cost flow in a network,
    must check the existence of b-flow first,
    the algorithm is not efficient for multigraph'''

    src = next((node for node, value in nw.b.items() if value > 0), None)
    tar = next((node for node, value in nw.b.items() if value < 0), None)
    flow = 0
    cost = 0    # cost
    i = 0
    while src is not None and tar is not None and i < 10:
        c, path, u_p = bf(nw, src, tar)
        print(f'iteration: {i+1}\nfind path: {list(np.array(path) + 1)}\nbottleneck capacity: {u_p}')
        if c == float('inf'):
            break
        for u, v in zip(path, path[1:]):
            nw.add_flow(u, v, max(u_p,nw.b[src]))
        nw.update_balance(src, nw.b[src] - u_p)
        nw.update_balance(tar, nw.b[tar] + u_p)
        flow += u_p
        cost += c * u_p
        src = next((node for node, value in nw.b.items() if value > 0), None)
        tar = next((node for node, value in nw.b.items() if value < 0), None)
        i += 1
    return flow, cost
