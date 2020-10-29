import vertex as v
import sys
from queue import PriorityQueue


class Graph(object):

    def __init__(self, graph_dict=None):
        if graph_dict is None:
            graph_dict = {}
        self.graph_dict = graph_dict

    def vertices(self):
        return list(self.graph_dict.keys())

    def edges(self):
        return self.generate_edges()

    def get_vertex(self, name):
        vertex_to_ret = None
        for vertex in self.vertices():
            if vertex.name == name:
                vertex_to_ret = vertex
        return vertex_to_ret

    def vertices_names(self):
        name_list = []
        for vertex in self.vertices():
            name_list.append(vertex.name)
        return name_list

    def get_neighbors(self, vertex):
        return self.graph_dict[vertex]

    def edge_weight(self, vertex1, vertex2):
        neighbors = self.get_neighbors(vertex1)
        for neighbor in neighbors:
            if neighbor[0].name == vertex2.name:
                return neighbor[1]

    def vertex_exists(self, vertex):
        return vertex.name in self.vertices_names()

    def add_vertex(self, vertex):
        if not self.vertex_exists(vertex):
            self.graph_dict[vertex] = []

    def add_edge(self, vertex1, vertex2, weight):
        if self.vertex_exists(vertex1):
            self.graph_dict[vertex1].append((vertex2, weight))
        else:
            self.graph_dict[vertex1] = [(vertex2, weight)]

    def generate_edges(self):
        edges = []
        for vertex in self.graph_dict:
            for neighbor_tuple in self.graph_dict[vertex]:
                edges.append((vertex, neighbor_tuple[0], neighbor_tuple[1]))
        return edges

    def __str__(self):
        res = "vertices: "
        for k in self.graph_dict:
            res += str(k) + ", "
        res += "\nedges: "
        for edge in self.generate_edges():
            res += "("+edge[0].name + ", " + edge[1].name + ", " + str(edge[2]) + "), "
        return res


def update_priority(priority_queue, neighbor, new_distance):
    removed_vertices = []
    while not priority_queue.empty():
        vertex_wrapper = priority_queue.get()
        removed_vertices.append(vertex_wrapper)
        if vertex_wrapper.vertex.name == neighbor.name:
            vertex_wrapper.attribute = new_distance
            break
    while len(removed_vertices) > 0:
        vertex_wrapper = removed_vertices.pop()
        priority_queue.put(vertex_wrapper)


def run_dijkstra(g, source):
    priority_queue = PriorityQueue()
    distances_dict = {}
    prev_dict = {}
    infinity = sys.maxsize
    for vertex in g.vertices():
        if vertex.name != source.name:
            distances_dict[vertex] = infinity
            prev_dict[vertex] = None
        else:
            distances_dict[vertex] = 0
        distance = distances_dict[vertex]
        priority_queue.put(v.VertexWrapper(vertex, distance))

    while not priority_queue.empty():
        min_vertex_wrapper = priority_queue.get()
        for neighbor in map(lambda neighbor_tup: neighbor_tup[0], g.get_neighbors(min_vertex_wrapper.vertex)):
            alt = distances_dict[min_vertex_wrapper.vertex] + g.edge_weight(min_vertex_wrapper.vertex, neighbor)
            if alt < distances_dict[neighbor]:
                distances_dict[neighbor] = alt
                prev_dict[neighbor] = min_vertex_wrapper.vertex
                update_priority(priority_queue, neighbor, distances_dict[neighbor])

    return distances_dict, prev_dict



