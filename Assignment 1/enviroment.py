import graph as g
import vertex as v
import agent as a
import state as s


class Limits:
	ASTAR_LIMIT = 10000
	REALTIME_ASTAR_LIMIT = 10
	GREEDY_LIMIT = 1
	T = 0.01
	TIME_LIMIT = 5


def generate_program_variables(file_name):
	output_graph = g.Graph()
	file = open(file_name)
	lines = file.readlines()
	name_vertices_dict = {}
	time = 0
	for line in lines:
		element_type = line[0]
		line = line.split(' ')
		if element_type == 'D':
			time = int(line[1])
		if element_type == 'V':
			name = line[1]
			number_of_people = int(line[2])
			u = v.Vertex(name, number_of_people)
			name_vertices_dict[u.name] = u
			output_graph.add_vertex(u)
		elif element_type == 'E':
			source_name = line[1]
			target_name = line[2]
			edge_weight = int(line[3])
			v1 = name_vertices_dict[source_name]
			v2 = name_vertices_dict[target_name]
			output_graph.add_edge(v1, v2, edge_weight)
	return output_graph, time


def mst_heuristic(vertex_wrapper):
	unsaved_vertices = vertex_wrapper.state.get_unsaved_vertices()
	zipped_graph = g.zip_graph(vertex_wrapper.state.world, unsaved_vertices)
	mst_zipped = zipped_graph.MST()
	return mst_zipped.get_sum_weights()


def get_vertices_with_positive_num_of_people(world_graph):
	essential_vertices = []
	for vertex in world_graph.get_vertices():
		if vertex.num_of_people > 0:
			essential_vertices.append(vertex)
	return essential_vertices


def get_vertices_list_as_vertices_status_dict(vertices_list):
	vertices_status_dict = dict()
	for vertex in vertices_list:
		vertices_status_dict[vertex] = False
	return vertices_status_dict


if __name__ == "__main__":
	world, Limits.TIME_LIMIT = generate_program_variables("graph.txt")
	vertices_with_people = get_vertices_with_positive_num_of_people(world)
	vertices_status = get_vertices_list_as_vertices_status_dict(vertices_with_people)
	world = g.zip_graph(world, vertices_with_people)
	greedy = a.GreedyAgent(world.get_vertex("v1"), vertices_status, mst_heuristic)
	astar = a.AStarAgent(world.get_vertex("v1"), vertices_status, mst_heuristic)
	realtime_astar = a.RealTimeAStarAgent(world.get_vertex("v1"), vertices_status, mst_heuristic)
	agent_list = [greedy, astar, realtime_astar]
	i = 0
	while not a.all_agents_terminated(agent_list):
		agent_list[i].act(world)
		i += 1
		i = i % len(agent_list)

	for agent in agent_list:
		print(agent)

