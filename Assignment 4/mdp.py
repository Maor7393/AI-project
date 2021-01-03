import operator
from functools import reduce

from state import State
from graph import Graph
from state import consistent_states,discovered_edges
import names

def transition(s1: State, s2: State, world: Graph) -> float:
	source_vertex = s1.current_vertex
	destination_vertex = s2.current_vertex
	blockable_edges_from_dest = world.get_adjacent_blockable_edges(destination_vertex)
	if source_vertex.name == "v1" and destination_vertex.name == "v2":
		if list(s1.edges_status.values()) == [names.U, names.U] and (list(s2.edges_status.values())[1] == names.U or list(s2.edges_status.values())[0]) :
			pass
	if not world.edge_exists(source_vertex, destination_vertex):
		return 0
	if s1.same_status(s2):
		for blockable_edge in blockable_edges_from_dest:
			if s2.edges_status[blockable_edge] == names.U:
				return 0
		return 1
	if not consistent_states(s1, s2):
		return 0
	for blockable_edge in s1.edges_status.keys():
		if s1.edges_status[blockable_edge] == names.U and s2.edges_status[blockable_edge] != names.U:
			if blockable_edge not in blockable_edges_from_dest:
				return 0
		elif s1.edges_status[blockable_edge] == names.U and s2.edges_status[blockable_edge] == names.U:
			if blockable_edge in blockable_edges_from_dest:
				return 0
	new_edges = discovered_edges(s1, s2)
	prob = 1
	for edge_tup in new_edges:
		if edge_tup[1] == 1:
			prob *= edge_tup[0].blocked_in_prob
		else:
			prob *= (1 - edge_tup[0].blocked_in_prob)
	return round(prob, 2)
