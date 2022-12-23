from node import Node

class Landscape:
    def __init__(self, num_rows, num_cols, height_map, neighbor_map):
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._nodes = {}

        # Create all nodes
        for coord in height_map:
            self._nodes[coord] = Node(coord, height_map[coord])
        
        # Now give nodes references to their neighbors.
        # Note that a neighbor is an adjacent (not diagonal) node that is no more
        # than one step higher than the current one.
        for coord in neighbor_map:
            current_node = self._nodes[coord]
            for potential_neighbor_coord in neighbor_map[coord]:
                potential_neighbor_node = self._nodes[potential_neighbor_coord]
                if potential_neighbor_node.height <= current_node.height + 1:
                    current_node.register_neighbor(potential_neighbor_node)

    def reset(self):
        for coord in self._nodes:
            n = self._nodes[coord]
            n.reset()

    def get_unvisited_node_with_lowest_dist(self):
        all_nodes = [self._nodes[i] for i in self._nodes]
        unvisited_nodes = filter(lambda n: not n.visited, all_nodes)
        unvisited_nodes_with_tentative_dist = list(filter(lambda n: n.min_dist is not None, unvisited_nodes))
        if len(unvisited_nodes_with_tentative_dist) == 0:
            return None
        
        unvisited_nodes_with_tentative_dist.sort(key=lambda x: x.min_dist)
        return unvisited_nodes_with_tentative_dist[0]

    def get_node(self, coord) -> Node|None:
        if coord in self._nodes:
            return self._nodes[coord]
        else:
            return None

    def shortest_route(self, start_coord, dest_coord):
        self.reset()
        start_node = self.get_node(start_coord)
        end_node = self.get_node(dest_coord)
        if start_node is None or end_node is None:
            return

        # Set min_dist for the start coord to 0 but don't set it as visited.
        start_node.min_dist = 0
        current_node = start_node
        
        while not end_node.visited:
            # Get the unvisited neighbors of the current node
            unvisited_neighbors = current_node.get_unvisited_neighbors()

            # Set the min_dist of each neighbor to the minimum of its current min_dist
            # and the current node's min_dist plus 1
            for n in unvisited_neighbors:
                if n.min_dist is None:
                    n.min_dist = current_node.min_dist + 1
                else:
                    n.min_dist = min(n.min_dist, current_node.min_dist + 1)
        
            # Now mark the current node as visited
            current_node.visited = True

            # Pick a new current node (the unvisited node with the lowest min_dist)
            current_node = self.get_unvisited_node_with_lowest_dist()

        return end_node.min_dist
