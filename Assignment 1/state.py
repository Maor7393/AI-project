class State:

	def __init__(self, current_vertex, vertices_to_save):
		self.current_vertex = current_vertex
		self.vertices_saved = vertices_to_save

	def save_vertex(self, vertex):
		self.vertices_saved[vertex] = True

	def amount_to_save(self):
		counter = 0
		for key in self.vertices_saved.keys():
			if self.vertices_saved[key]:
				counter += 1

		return counter
