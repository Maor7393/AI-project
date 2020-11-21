import vertex as v
import copy as cp
import graph as g
from program_variables import TIME_LIMIT

def amount_to_save(vertices_status):
	counter = 0
	for key in vertices_status.keys():
		if not vertices_status[key]:
			counter += 1
	return counter


class State:

	def __init__(self, max_agent_current_location, min_agent_current_location, max_vertices_status: dict, min_vertices_status: dict, max_agent_score: int, min_agent_score: int, max_acc_weight: int, min_acc_weight: int):
		self.max_agent_current_location = max_agent_current_location
		self.min_agent_current_location = min_agent_current_location
		self.max_vertices_status = cp.copy(max_vertices_status)
		self.min_vertices_status = cp.copy(min_vertices_status)
		self.max_agent_score = max_agent_score
		self.min_agent_score = min_agent_score
		self.max_acc_weight = max_acc_weight
		self.min_acc_weight = min_acc_weight


	def get_unsaved_vertices(self):
		unsaved = []
		for vertex in self.vertices_status.keys():
			if not self.vertices_status[vertex]:
				unsaved.append(vertex)
		return unsaved

	def terminal_state(self):
		return amount_to_save(self.max_vertices_status) == 0 or amount_to_save(self.min_vertices_status) == 0 or self.min_acc_weight + self.max_acc_weight >= TIME_LIMIT

	def __str__(self):
		s = "Current vertex: " + str(self.current_vertex) + "\n{"
		for vertex in self.vertices_status:
			s += vertex.name + ": " + str(self.vertices_status[vertex]) + "\n"
		return s + "}"

	def save_current_vertex(self,):
		self.vertices_status[self.current_vertex] = True



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
