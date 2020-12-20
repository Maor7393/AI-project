from node import Node
from table import Table, make_table
import names


def create_bayes_network(file_name):
    with open(file_name, 'r') as graph_file:
        network = BayesNetwork()
        for line in graph_file.readlines():
            words_array = line.split(' ')
            if len(words_array) > 0:
                first_letter = words_array[0]
                if first_letter == 'N':
                    pass
                elif first_letter == 'V':
                    vertex_name = words_array[1]
                    people_prob = float(words_array[2])
                    node = Node(vertex_name, make_table([[names.empty]], [people_prob]))
                    network.add_node(node)
                elif first_letter == 'E':
                    edge_name = words_array[1] + '_t:0'
                    vertex_1_name = words_array[2]
                    vertex_2_name = words_array[3]
                    weight = int(words_array[4])
                    edge_node = Node(edge_name, make_table(create_all_entries(vertex_1_name, vertex_2_name),
                                                           calculate_edge_block_prob(weight)))
                    vertex_1_node = network.get_node(vertex_1_name)
                    vertex_2_node = network.get_node(vertex_2_name)
                    network.add_node(edge_node)
                    network.add_relation(vertex_1_node, edge_node, weight)
                    network.add_relation(vertex_2_node, edge_node, weight)
                elif first_letter == 'P':
                    pass
        return network


def calculate_edge_block_prob(weight):
    return [0.001, 0.6 * 1 / weight, 0.6 * 1 / weight, 1 - pow(1 - (0.6 * 1 / weight), 2)]


def create_all_entries(name_1, name_2):
    return [[(name_1, False), (name_2, False)], [(name_1, True), (name_2, False)], [(name_1, False), (name_2, True)],
            [(name_1, True), (name_2, True)]]


class BayesNetwork:
    def __init__(self):
        self.children_dict = {}
        self.parents_dict = {}

    def add_node(self, node: Node):
        if not self.children_dict.get(node):
            self.children_dict[node] = []
        if not self.parents_dict.get(node):
            self.parents_dict[node] = []

    def add_relation(self, parent: Node, child: Node, weight: int):
        if child not in self.children_dict[parent]:
            self.children_dict[parent].append((child, weight))
        if parent not in self.parents_dict[child]:
            self.parents_dict[child].append((parent, weight))

    def get_node(self, node_name):
        for node in self.children_dict.keys():
            if node.name == node_name:
                return node
        return None

    def __str__(self):
        s = 'Bayes Network:'
        s += 'nodes: \n'
        for node in self.children_dict.keys():
            s += str(node)
        return s
