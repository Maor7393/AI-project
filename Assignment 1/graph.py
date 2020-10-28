import vertex

class Graph(object):

    def __init__(self, graph_dict=None):
        if graph_dict == None:
            graph_dict = {}
        self.__graph_dict = graph_dict

    def vertices(self):
        return list(self.__graph_dict.keys())

    def vertices_names(self):
        name_list = []
        for vertex in self.vertices(self):
            name_list.append(vertex.name)
        return name_list

    def edges(self):
        return self.__generate_edges()

    def vertexExists(self,vertex):
        return vertex.name in self.vertices_names();

    def add_vertex(self, vertex):
        if not self.vertexExists(vertex):
            self.__graph_dict[vertex] = []

    def add_edge(self, vertex1,vertex2,weight):
        if  self.vertexExists(vertex1):
            self.__graph_dict[vertex1].append((vertex2,weight))
        else:
            self.__graph_dict[vertex1] = [(vertex2,weight)]

    def __generate_edges(self):
        edges = []
        for vertex in self.__graph_dict:
            for neighbor_tuple in self.__graph_dict[vertex]:
                edges.append((vertex,neighbor_tuple[0],neighbor_tuple[1]))
        return edges

    def __str__(self):
        res = "vertices: "
        for k in self.__graph_dict:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.__generate_edges():
            res += str(edge) + ", "
        return res
		