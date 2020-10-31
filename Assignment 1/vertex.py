class Vertex (object):
    def __init__(self, name, number_of_people):
        self.name = name
        self.num_of_people = number_of_people

    def __str__(self):
        return "["+self.name + ", " + str(self.num_of_people)+"]"


class VertexWrapper(object):

    def __init__(self, vertex, parent_wrapper, acc_weight):
        self.vertex = vertex
        self.parent_wrapper = parent_wrapper
        self.acc_weight = acc_weight
