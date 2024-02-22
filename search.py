from collections import deque


class Graph:
    def __init__(self, data=None):
        if data is None:
            data = {}
        self.graph = data

    def add_vertex(self, vertex):
        if vertex not in self.graph:
            self.graph[vertex] = []

    def add_edge(self, vertex1, vertex2):
        if vertex1 in self.graph and vertex2 in self.graph:
            if vertex2 not in self.graph[vertex1]:
                self.graph[vertex1].append(vertex2)
            if vertex1 not in self.graph[vertex2]:
                self.graph[vertex2].append(vertex1)

    def display(self):
        for node in self.graph:
            print(f"{node}: {', '.join(map(str, self.graph[node]))}")

    def bfs_shortest_path(self, start, end):
        if start not in self.graph or end not in self.graph:
            print("Invalid start or end node.")
            return

        visited = set()
        queue = deque([(start, [start])])

        while queue:
            current, path = queue.popleft()

            if current == end:
                return path

            if current not in visited:
                visited.add(current)
                for neighbor in self.graph[current]:
                    if neighbor not in visited:
                        queue.append((neighbor, path + [neighbor]))

        print("No path found.")
        return None
