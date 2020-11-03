import vertex as v
import copy as cp

class State:

	def __init__(self, world, current_vertex: v.Vertex, vertices_status: dict):
		self.current_vertex = current_vertex
		self.vertices_status = cp.copy(vertices_status)
		self.world = world

	def save_current_vertex(self):
		self.vertices_status[self.current_vertex] = True

	def get_unsaved_vertices(self):
		unsaved = []
		for vertex in self.vertices_status.keys():
			if self.vertices_status[vertex]:
				unsaved.append(vertex)
		return unsaved

	def amount_to_save(self):
		counter = 0
		for key in self.vertices_status.keys():
			if self.vertices_status[key]:
				counter += 1
		return counter
