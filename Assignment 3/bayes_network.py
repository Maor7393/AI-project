from node import Node


class BayesNetwork:

    def __init__(self):
        self.children_dict = {}
        self.parents_dict = {}

    def add_vertex(self, vertex):
        if not self.children_dict.get(vertex):
            self.children_dict[vertex] = []
        if not self.parents_dict.get(vertex):
            self.parents_dict[vertex] = []

    def add_relation(self, parent: Node, child: Node):
        if child not in self.children_dict[parent]:
            self.children_dict[parent].append(child)
        if parent not in self.parents_dict[child]:
            self.parents_dict[child].append(parent)

    def __str__(self):
        pass