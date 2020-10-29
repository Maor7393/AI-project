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


def update_priority(priority_queue, neighbor, distances_dict):
    removed_vertices = []
    while not priority_queue.empty():
        vertex = priority_queue.get()
        removed_vertices.append(vertex)
        if vertex.name == neighbor.name:
            break
    while len(removed_vertices) > 0:
        vertex = removed_vertices.pop()
        priority_queue.put(distances_dict[vertex], vertex)


def run_dijkstra(g, source):
    priority_queue = PriorityQueue()
    distances_dict = {}
    prev_dict = {}
    infinity = sys.maxsize

    for vertex in g.vertices():
        if vertex.name != source.name:
            distances_dict[vertex.name] = infinity
            prev_dict[vertex] = None
        distance = distances_dict[vertex.name]
        priority_queue.put((distance, vertex))

    while not priority_queue.empty():
        min_vertex = priority_queue.get()
        for neighbor in g.get_neighbors(min_vertex):
            alt = distances_dict[min_vertex] + g.edge_weight(min_vertex, neighbor)
            if alt < distances_dict[neighbor.vertex]:
                distances_dict[neighbor] = alt
                prev_dict[neighbor] = min_vertex
                update_priority(priority_queue, neighbor, distances_dict)

    return distances_dict, prev_dict


def generate_graph(file_name):
    output_graph = Graph()
    file = open(file_name)
    lines = file.readlines()
    name_vertices_dict = {}
    for line in lines:
        element_type = line[0]
        line = line.split(' ')
        if element_type == 'V':
            name = line[1]
            number_of_people = int(line[2])
            vertex = v.Vertex(name, number_of_people)
            name_vertices_dict[vertex.name] = vertex
            output_graph.add_vertex(vertex)
        elif element_type == 'E':
            source_name = line[1]
            target_name = line[2]
            edge_weight = int(line[3])
            v1 = name_vertices_dict[source_name]
            v2 = name_vertices_dict[target_name]
            output_graph.add_edge(v1, v2, edge_weight)
    return output_graph
