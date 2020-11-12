class Vertex(object):
	def __init__(self, name, number_of_people):
		self.name = name
		self.num_of_people = number_of_people

	def __str__(self):
		return "[" + self.name + ", " + str(self.num_of_people) + "]"


class VertexWrapper(object):

	def __init__(self, state, parent_wrapper, acc_weight):
		self.state = state
		self.parent_wrapper = parent_wrapper
		self.acc_weight = acc_weight


def get_vertices_list_as_string(vertices_list):
	s = "[ "
	for vertex in vertices_list:
		s += str(vertex) + ", "
	last_index_of_comma = s.rfind(",")
	s = s[:last_index_of_comma] + s[last_index_of_comma + 1:]
	return s + "]"
