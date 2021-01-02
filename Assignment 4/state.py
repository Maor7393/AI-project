import vertex as v
import copy as cp
import graph as g
import names
import itertools


def generate_states(graph: g.Graph):
	states = []
	vertices = graph.get_vertices()
	edges = graph.get_edges()
	possibilites_for_edges = itertools.product([0, 1, names.U],
	                                           repeat=len([edge for edge in edges if edge.blocked_in_prob > 0]))
	for possibility in possibilites_for_edges:
		edges_status = dict(zip(edges, possibility))
		for vertex in vertices:
			states.append(State(vertex, edges_status))
	return states


class State:

	def __init__(self, current_vertex: v.Vertex, edges_status: dict):
		self.current_vertex = current_vertex
		self.edges_status = cp.copy(edges_status)

	def same_status(self, other) -> bool:
		return self.edges_status == other.edges_status

	def __str__(self):
		s = "Current vertex: " + str(self.current_vertex) + "\n{"
		for edge in self.edges_status:
			s += edge.name + ": " + str(self.edges_status[edge]) + "\n"
		return s + "}"


def state_list_as_string(state_list) -> str:
	s = "STATES:\n"
	for state in state_list:
		s += str(state) + "\n"
	return s


def consistant_states(state1, state2) -> bool:
	pass
