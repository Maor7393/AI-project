import operator
from functools import reduce

from state import State
from graph import Graph
from state import consistant_states
import names

def transition(s1: State, s2: State, world: Graph) -> float:
	source_vertex = s1.current_vertex
	destination_vertex = s2.current_vertex
	blockable_edges_from_dest = world.get_adjacent_blockable_edges(destination_vertex)
	if not world.edge_exists(source_vertex, destination_vertex):
		return 0
	if s1.same_status(s2):
		for blockable_edge in blockable_edges_from_dest:
			if s2.edges_status[blockable_edge] == names.U:
				return 0
		return 1
	if not consistant_states(s1,s2):
		return 0
	for blockable_edge in s1.edges_status.keys():
		if s1.edges_status[blockable_edge] == names.U and s2.edges_status[blockable_edge] != names.U:
			if blockable_edge not in blockable_edges_from_dest:
				return 0
	return reduce(operator.mul, blockable_edges_from_dest, initial=1)