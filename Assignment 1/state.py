import vertex as v
import copy as cp
import graph as g


class State:

	def __init__(self, current_vertex: v.Vertex, vertices_status: dict):
		self.current_vertex = current_vertex
		self.vertices_status = cp.copy(vertices_status)

	def save_current_vertex(self):
		self.vertices_status[self.current_vertex] = True

	def get_unsaved_vertices(self):
		unsaved = []
		for vertex in self.vertices_status.keys():
			if not self.vertices_status[vertex]:
				unsaved.append(vertex)
		return unsaved

	def amount_to_save(self):
		counter = 0
		for key in self.vertices_status.keys():
			if not self.vertices_status[key]:
				counter += 1
		return counter

	def update_vertices_status(self, world: g.Graph):
		for vertex in world.get_vertices():
			if vertex.num_of_people > 0:
				self.vertices_status[vertex] = False
			else:
				self.vertices_status[vertex] = True

	def does_current_vertex_need_saving(self):
		if not self.vertices_status[self.current_vertex]:
			return True
		return False
