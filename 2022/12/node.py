class Node:
    def __init__(self, coords, height) -> None:
        self._visited = False
        self._min_dist = None
        self._accessible_neighbors = []
        self._height = height
        self._coords = coords

    @property
    def height(self):
        return self._height

    @property
    def visited(self):
        return self._visited

    @visited.setter
    def visited(self, value):
        self._visited = value

    @property
    def min_dist(self):
        return self._min_dist

    @min_dist.setter
    def min_dist(self, value):
        self._min_dist = value

    def register_neighbor(self, new_neighbor):
        if new_neighbor not in self._accessible_neighbors:
            self._accessible_neighbors.append(new_neighbor)

    def get_unvisited_neighbors(self):
        unvisited_neighbors = filter(lambda n: not n.visited, self._accessible_neighbors)
        return list(unvisited_neighbors)

    def reset(self):
        self._min_dist = None
        self._visited = False
