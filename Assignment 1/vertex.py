class Vertex (object):
    def __init__(self, name, number_of_people):
        self.name = name
        self.num_of_people = number_of_people

    def __str__(self):
        return "["+self.name + ", " + str(self.num_of_people)+"]"


class VertexWrapper(object):

    def __init__(self, vertex, attribute):
        self.vertex = vertex
        self.attribute = attribute

    def __lt__(self, other):
        if self.attribute < other.attribute:
            return True
        else:
            return False

    def __gt__(self, other):
        if self.attribute > other.attribute:
            return True
        else:
            return False

    def __eq__(self, other):
        if self.attribute == other.attribute:
            return True
        else:
            return False
