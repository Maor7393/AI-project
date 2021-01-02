class Vertex(object):
	def __init__(self, name, target = False):
		self.name = name
		self.target = target

	def __str__(self):
		return "[VERTEX " + self.name + ", " + "target: " + str(self.target) + "]"


def get_vertices_list_as_string(vertices_list):
	s = "[ "
	for vertex in vertices_list:
		s += str(vertex) + ", "
	last_index_of_comma = s.rfind(",")
	if last_index_of_comma != -1:
		s = s[:last_index_of_comma] + s[last_index_of_comma + 1:]

	return s + "]"
