import vertex as v
import sys
from queue import PriorityQueue
import copy


class Graph(object):

    def __init__(self, graph_dict=None):
        if graph_dict is None:
            graph_dict = {}
        self.graph_dict = graph_dict

    def get_vertices(self):
        return list(self.graph_dict.keys())

    def get_edges(self):
        return self.generate_edges()

    def get_vertex(self, name):
        vertex_to_ret = None
        for vertex in self.get_vertices():
            if vertex.name == name:
                vertex_to_ret = vertex
        return vertex_to_ret

    def get_edge(self, vertex1, vertex2: v.Vertex):
        neighbors = self.expand(vertex1)
        for neighbor_tup in neighbors:
            if neighbor_tup[0].name == vertex2.name:
                return vertex1, neighbor_tup[1], vertex2
        return None

    def vertices_names(self):
        name_list = []
        for vertex in self.get_vertices():
            name_list.append(vertex.name)
        return name_list

    def expand(self, vertex):
        return self.graph_dict[vertex]

    def expand_just_vertices(self, vertex):
        return map(lambda neighbor_tup: neighbor_tup[0], self.expand(vertex))

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

    def get_sum_weights(self):
        sum_weight_mst = 0
        for edge in self.get_edges():
            sum_weight_mst += edge[2]
        return sum_weight_mst / 2

    def add_vertex(self, vertex):
        if not self.vertex_exists(vertex):
            self.graph_dict[vertex] = []

    def add_edge(self, vertex1, vertex2, weight):
        if vertex2 not in self.expand_just_vertices(vertex1) and vertex1 not in self.expand_just_vertices(vertex2):
            self.graph_dict[vertex1].append((vertex2, weight))
            self.graph_dict[vertex2].append((vertex1, weight))

    def delete_edge(self, vertex1, vertex2):
        index_of_vertex2_in_vertex_1 = 0
        index_of_vertex1_in_vertex_2 = 0
        for neighbor_tup in self.expand(vertex1):
            if neighbor_tup[0] == vertex2:
                break
            index_of_vertex2_in_vertex_1 += 1
        for neighbor_tup in self.expand(vertex2):
            if neighbor_tup[0] == vertex1:
                break
            index_of_vertex1_in_vertex_2 += 1
        del self.graph_dict[vertex1][index_of_vertex2_in_vertex_1]
        del self.graph_dict[vertex2][index_of_vertex1_in_vertex_2]

    def add_or_replace_edge(self, vertex1, vertex2, weight):
        if vertex2 not in self.expand_just_vertices(vertex1) and vertex1 not in self.expand_just_vertices(vertex2):
            self.graph_dict[vertex1].append((vertex2, weight))
            self.graph_dict[vertex2].append((vertex1, weight))
        elif weight < self.get_edge_weight(vertex1, vertex2):
            self.replace_edge(vertex1, vertex2, weight)

    def replace_edge(self, vertex1, vertex2, weight):
        self.delete_edge(vertex1, vertex2)
        self.graph_dict[vertex1].append((vertex2, weight))
        self.graph_dict[vertex2].append((vertex1, weight))

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

        res = res[:len(res)-2]
        res += "\nedges: "
        for edge in self.generate_edges():
            res += "(" + edge[0].name + ", " + edge[1].name + ", " + str(edge[2]) + "), "
        res = res[:len(res)-2]
        return res

    def copy_graph(self):
        new_graph = Graph()
        for vertex in self.get_vertices():
            new_graph.graph_dict[vertex] = list(self.expand(vertex))
        return new_graph

    def remove_unessential_vertices(self, unessential_vertices_array):
        for vertex in unessential_vertices_array:
            self.delete_all_occurrences(vertex)

    def delete_all_occurrences(self, vertex):
        for u in self.graph_dict.keys():
            neighbors_tuples = self.graph_dict[u]
            for tup in neighbors_tuples:
                if tup[0] == vertex:
                    neighbors_tuples.remove(tup)
        self.graph_dict.pop(vertex)

    def zip_edges(self):
        for vertex in self.get_vertices():
            min_edges = {}
            neighbors_tuples = self.expand(vertex)
            for neighbor_tup in neighbors_tuples:
                if min_edges.get(neighbor_tup[0]) is not None:
                    if min_edges[neighbor_tup[0]] > neighbor_tup[1]:
                        min_edges[neighbor_tup[0]] = neighbor_tup[1]
                else:
                    min_edges[neighbor_tup[0]] = neighbor_tup[1]
            self.graph_dict[vertex] = [(key, val) for key, val in min_edges.items()]

    def connect_all_neighbors(self, vertex):
        neighbor_tuples = self.expand(vertex)
        for neighbor_tuple in neighbor_tuples:
            for other_neighbor_tuple in neighbor_tuples:
                if not (neighbor_tuple == other_neighbor_tuple):
                    both_edges_weight = neighbor_tuple[1] + other_neighbor_tuple[1]
                    self.add_or_replace_edge(neighbor_tuple[0], other_neighbor_tuple[0], both_edges_weight)

    def get_lowest_cost_edge_between_sets(self, in_set, out_set):
        min_edge = None
        min_weight = sys.maxsize
        for in_vertex in in_set:
            for out_vertex in out_set:
                if self.edge_exists(in_vertex, out_vertex) and min_weight >= self.get_edge_weight(in_vertex, out_vertex):
                    current_edge_weight = self.get_edge_weight(in_vertex, out_vertex)
                    min_weight = current_edge_weight
                    min_edge = (in_vertex, out_vertex, min_weight)
        return min_edge

    def MST(self):
        mst = Graph()
        in_set = {self.get_vertices()[0]}
        out_set = set(self.get_vertices()[1:])
        edge_set = set()
        while len(out_set) > 0:
            edge = self.get_lowest_cost_edge_between_sets(in_set, out_set)
            edge_set.add(edge)
            in_set.add(edge[1])
            out_set.remove(edge[1])
        for vertex in in_set:
            mst.add_vertex(vertex)
        for edge in edge_set:
            mst.add_edge(*edge)
        return mst


def zip_graph(original_graph: Graph, essential_vertices):
    essential_graph = original_graph.copy_graph()
    for vertex in essential_graph.get_vertices():
        if vertex not in essential_vertices:
            essential_graph.connect_all_neighbors(vertex)
    essential_graph.remove_unessential_vertices(
        list(filter(lambda u: u not in essential_vertices, essential_graph.get_vertices())))
    essential_graph.zip_edges()
    return essential_graph
