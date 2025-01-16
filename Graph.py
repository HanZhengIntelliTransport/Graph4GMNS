class SimpleGraph:
    def __init__(self, directed=False):
        self._adjacency = {}
        self._node_attrs = {}
        self._edge_attrs = {}
        self._directed = directed

    def add_node(self, node, **attrs):
        """Add a single node to the graph with optional attributes."""
        if node not in self._adjacency:
            self._adjacency[node] = []
        # Store node attributes in a dictionary
        if node not in self._node_attrs:
            self._node_attrs[node] = {}
        self._node_attrs[node].update(attrs)

    def add_nodes_from(self, nodes, **common_attrs):
        """Add multiple nodes. Common attributes get applied to all nodes."""
        for node in nodes:
            self.add_node(node, **common_attrs)

    def remove_node(self, node):
        """Remove a node and any edges referencing it."""
        if node in self._adjacency:
            # Remove all edges pointing to 'node'
            for n, neighbors in self._adjacency.items():
                self._adjacency[n] = [nbr for nbr in neighbors if nbr != node]

            # Now remove the node entirely
            del self._adjacency[node]

        if node in self._node_attrs:
            del self._node_attrs[node]

        # Remove edges from _edge_attrs
        to_delete = []
        for (u, v), attrs in self._edge_attrs.items():
            if u == node or v == node:
                to_delete.append((u, v))
        for key in to_delete:
            del self._edge_attrs[key]

    def add_edge(self, u, v, **attrs):
        """Add an edge between u and v. If undirected, add both ways."""
        if u not in self._adjacency:
            self.add_node(u)
        if v not in self._adjacency:
            self.add_node(v)

        # Add edge in adjacency
        if v not in self._adjacency[u]:
            self._adjacency[u].append(v)

        if not self._directed and u not in self._adjacency[v]:
            self._adjacency[v].append(u)

        # Store edge attributes
        self._edge_attrs[(u, v)] = attrs
        if not self._directed:
            self._edge_attrs[(v, u)] = attrs

    def remove_edge(self, u, v):
        """Remove the edge between u and v."""
        if u in self._adjacency and v in self._adjacency[u]:
            self._adjacency[u].remove(v)
        if not self._directed and v in self._adjacency and u in self._adjacency[v]:
            self._adjacency[v].remove(u)

        if (u, v) in self._edge_attrs:
            del self._edge_attrs[(u, v)]
        if not self._directed and (v, u) in self._edge_attrs:
            del self._edge_attrs[(v, u)]

    def neighbors(self, node):
        """Return the list of neighbors of a node."""
        return self._adjacency.get(node, [])

    def nodes(self):
        """Return a list of nodes in the graph."""
        return list(self._adjacency.keys())

    def edges(self):
        """Return a list of edges in the graph."""
        if self._directed:
            return list(self._edge_attrs.keys())
        else:
            # For undirected, only return each edge once (u, v) where u < v, for example
            edges = set()
            for (u, v) in self._edge_attrs.keys():
                if (v, u) not in edges:
                    edges.add((u, v))
            return list(edges)

    def node_attributes(self, node):
        """Return the dictionary of attributes for the node."""
        return self._node_attrs.get(node, {})

    def edge_attributes(self, u, v):
        """Return the dictionary of attributes for the edge (u, v)."""
        return self._edge_attrs.get((u, v), {})

    def __repr__(self):
        return f"<SimpleGraph directed={self._directed}, nodes={len(self._adjacency)}, edges={len(self._edge_attrs)}>"
