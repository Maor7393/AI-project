import vertex as v


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
        return self.graph_dict[vertex];
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
