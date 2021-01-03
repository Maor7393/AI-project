import vertex as v
import sys
from edge import Edge
import copy


class Graph(object):

    def __init__(self, graph_dict=None):
        if graph_dict is None:
            graph_dict = {}
        self.graph_dict = graph_dict

    def get_vertices(self):
        return list(self.graph_dict.keys())

    def get_adjacent_blockable_edges(self,vertex):
        blockable_edges = []
        for neighbor_tup in self.expand(vertex):
            if neighbor_tup[2].blocked_in_prob > 0:
                blockable_edges.append(neighbor_tup[2])
        return blockable_edges

    def get_edges(self):
        edges = set()
        for vertex in self.graph_dict:
            for neighbor_tuple in self.graph_dict[vertex]:
                edges.add(neighbor_tuple[2])
        return list(edges)

    def get_vertex(self, name):
        vertex_to_ret = None
        for vertex in self.get_vertices():
            if vertex.name == name:
                vertex_to_ret = vertex
        return vertex_to_ret

    def vertices_names(self):
        name_list = []
        for vertex in self.get_vertices():
            name_list.append(vertex.name)
        return name_list

    def expand(self, vertex):
        return self.graph_dict[vertex]

    def expand_just_vertices(self, vertex):
        return list(map(lambda neighbor_tup: neighbor_tup[0], self.expand(vertex)))

    def get_edge_weight(self, vertex1, vertex2):
        neighbors = self.expand(vertex1)
        for neighbor in neighbors:
            if neighbor[0].name == vertex2.name:
                return neighbor[1]

    def get_closest_neighbor(self, vertex):
        min_weight = sys.maxsize
        min_neighbor_tup = None
        for neighbor_tup in self.expand(vertex):
            if min_weight >= neighbor_tup[1]:
                min_weight = neighbor_tup[1]
                min_neighbor_tup = neighbor_tup
        return min_neighbor_tup

    def vertex_exists(self, vertex):
        return vertex.name in self.vertices_names()

    def edge_exists(self, vertex1, vertex2):
        neighbor_list = self.expand(vertex1)
        for neighbor_tup in neighbor_list:
            if vertex2 == neighbor_tup[0]:
                return True
        return False

    def add_vertex(self, vertex):
        if not self.vertex_exists(vertex):
            self.graph_dict[vertex] = []

    def add_edge(self, vertex1, vertex2, weight, edge_name, probability=0):
        edge = Edge(edge_name, weight, vertex1, vertex2, probability)
        if vertex2 not in self.expand_just_vertices(vertex1) and vertex1 not in self.expand_just_vertices(vertex2):
            self.graph_dict[vertex1].append((vertex2, weight, edge))
            self.graph_dict[vertex2].append((vertex1, weight, edge))

    def generate_edges(self):
        edges = []
        for vertex in self.graph_dict:
            for neighbor_tuple in self.graph_dict[vertex]:
                edges.append((vertex, neighbor_tuple[0], neighbor_tuple[1]))
        return edges

    def __str__(self):
        s =""
        for edge in self.get_edges():
            s += str(edge) + "\n"
        s += "\n"
        return s

    def copy_graph(self):
        new_graph = Graph()
        for vertex in self.get_vertices():
            new_graph.graph_dict[vertex] = list(self.expand(vertex))
        return new_graph



