from Graph import *

if __name__ == "__main__":
    g = SimpleGraph(directed=False)
    g.add_node("A", color="red")
    g.add_node("B", color="blue")
    g.add_edge("A", "B", weight=3, label="A-B")

    print("Nodes:", g.nodes())
    print("Edges:", g.edges())
    print("Neighbors of A:", g.neighbors("A"))
    print("Node A's attributes:", g.node_attributes("A"))
    print("Edge (A, B) attributes:", g.edge_attributes("A", "B"))

    print(g)  # Check representation


def dfs(graph, start_node):
    visited = set()
    stack = [start_node]

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            # Add neighbors in reverse order to mimic standard recursion-based DFS
            neighbors = graph.neighbors(node)
            for nbr in reversed(neighbors):
                if nbr not in visited:
                    stack.append(nbr)
    return visited

from collections import deque

def bfs(graph, start_node):
    visited = set()
    queue = deque([start_node])

    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            for nbr in graph.neighbors(node):
                if nbr not in visited:
                    queue.append(nbr)
    return visited


import heapq

def dijkstra(graph, source):
    # Distances dictionary
    dist = {node: float("inf") for node in graph.nodes()}
    dist[source] = 0

    # Priority queue: (distance, node)
    pq = [(0, source)]

    while pq:
        current_dist, node = heapq.heappop(pq)

        if current_dist > dist[node]:
            continue  # Skip if we already found a better path

        for nbr in graph.neighbors(node):
            # Retrieve the weight from edge attributes
            weight = graph.edge_attributes(node, nbr).get("weight", 1)
            new_dist = current_dist + weight
            if new_dist < dist[nbr]:
                dist[nbr] = new_dist
                heapq.heappush(pq, (new_dist, nbr))

    return dist
