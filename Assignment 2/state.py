import vertex as v
import copy as cp
import graph as g
from program_variables import TIME_LIMIT
from program_variables import WORLD


def amount_to_save(vertices_status):
	counter = 0
	for key in vertices_status.keys():
		if not vertices_status[key]:
			counter += 1
	return counter


class Location(object):
	def __init__(self, prev: v.Vertex, edge_progress: int, successor: v.Vertex):
		self.prev = prev
		self.edge_progress = edge_progress
		self.successor = successor

	def get_new_closer_location(self):
		return Location(self.prev, self.edge_progress - 1, self.successor)

	def __str__(self):
		return "( " + self.prev.name + ", " + str(self.edge_progress) + ", " + self.successor.name + ")"


class State:

	def __init__(self, max_agent_current_location: Location, min_agent_current_location: Location, vertices_status: dict, max_agent_score: int, min_agent_score: int, max_acc_weight: int, min_acc_weight: int):
		self.max_agent_current_location = cp.copy(max_agent_current_location)
		self.min_agent_current_location = cp.copy(min_agent_current_location)
		self.vertices_status = cp.copy(vertices_status)
		self.max_agent_score = max_agent_score
		self.min_agent_score = min_agent_score
		self.max_acc_weight = max_acc_weight
		self.min_acc_weight = min_acc_weight

	def get_new_state(self):
		return State(self.max_agent_current_location, self.min_agent_current_location, self.vertices_status, self.max_agent_score, self.min_agent_score, self.max_acc_weight, self.min_acc_weight)

	def successor(self, type_of_agent: str):
		if type_of_agent == "MAX":
			return self.max_successor()
		elif type_of_agent == "MIN":
			return self.min_successor()

	def max_successor(self):
		new_states = []
		if self.max_agent_current_location.edge_progress > 0:
			new_state = self.get_new_state()
			new_state.max_agent_current_location = new_state.max_agent_current_location.get_new_closer_location()
			new_state.max_acc_weight = new_state.max_acc_weight + 1
			new_states.append(new_state)
		else:
			arrived_to_vertex = self.max_agent_current_location.successor
			max_new_score = self.max_agent_score
			if not self.vertices_status[arrived_to_vertex]:
				max_new_score = self.max_agent_score + arrived_to_vertex.num_of_people
				self.mark_save_vertex(arrived_to_vertex)
			for neighbor_tup in WORLD.expand(arrived_to_vertex):
				max_new_location = Location(arrived_to_vertex, neighbor_tup[1] - 1, neighbor_tup[0])
				new_state = self.get_new_state()
				new_state.max_agent_current_location = max_new_location
				new_state.max_agent_score = max_new_score
				new_states.append(new_state)
		return new_states

	def min_successor(self):
		new_states = []
		if self.min_agent_current_location.edge_progress > 0:
			new_state = self.get_new_state()
			new_state.min_agent_current_location = new_state.min_agent_current_location.get_new_closer_location()
			new_state.min_acc_weight = new_state.min_acc_weight + 1
			new_states.append(new_state)
		else:
			arrived_to_vertex = self.min_agent_current_location.successor
			min_new_score = self.min_agent_score
			if not self.vertices_status[arrived_to_vertex]:
				min_new_score = self.min_agent_score + arrived_to_vertex.num_of_people
				self.mark_save_vertex(arrived_to_vertex)
			for neighbor_tup in WORLD.expand(arrived_to_vertex):
				min_new_location = Location(arrived_to_vertex, neighbor_tup[1], neighbor_tup[0])
				new_state = self.get_new_state()
				new_state.min_agent_current_location = min_new_location
				new_state.min_agent_score = min_new_score
				new_states.append(new_state)
		return new_states

	def mark_save_vertex(self, vertex):
		self.vertices_status[vertex] = True

	# TODO: implement with MST
	def evaluate(self):
		return self.max_agent_score, self.min_agent_score

	def get_unsaved_vertices(self):
		unsaved = []
		for vertex in self.vertices_status.keys():
			if not self.vertices_status[vertex]:
				unsaved.append(vertex)
		return unsaved

	def terminal_state(self):
		return amount_to_save(self.vertices_status) == 0 or self.min_acc_weight + self.max_acc_weight >= TIME_LIMIT

	def __str__(self):
		s = "Current vertex: " + str(self.current_vertex) + "\n{"
		for vertex in self.vertices_status:
			s += vertex.name + ": " + str(self.vertices_status[vertex]) + "\n"
		return s + "}"

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
