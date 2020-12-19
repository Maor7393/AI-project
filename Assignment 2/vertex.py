class Vertex(object):
	def __init__(self, name, number_of_people):
		self.name = name
		self.num_of_people = number_of_people

	def __str__(self):
		return "[" + self.name + ", " + str(self.num_of_people) + "]"


def all_vertex_saved(vertices_list):
	for vertex in vertices_list:
		if vertex.num_of_people > 0:
			return False
	return True


def get_vertices_list_as_string(vertices_list):
	s = "[ "
	for vertex in vertices_list:
		s += str(vertex) + ", "
	last_index_of_comma = s.rfind(",")
	if last_index_of_comma != -1:
		s = s[:last_index_of_comma] + s[last_index_of_comma + 1:]

	return s + "]"
