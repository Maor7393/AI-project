import graph as g
import vertex as v
import agent as a
from program_variables import CUTOFF,TIME_LIMIT
import compartors as cmp

def generate_time_limit(file_name):
	file = open(file_name)
	lines = file.readlines()
	line = lines[0]
	line = line.split(' ')
	time = int(line[1])
	file.close()
	return time


def generate_graph(file_name):
	output_graph = g.Graph()
	file = open(file_name)
	lines = file.readlines()
	name_vertices_dict = {}
	for line in lines:
		element_type = line[0]
		line = line.split(' ')
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
	file.close()
	return output_graph


def get_vertices_with_positive_num_of_people(world_graph):
	list_of_positives = []
	for vertex in world_graph.get_vertices():
		if vertex.num_of_people > 0:
			list_of_positives.append(vertex)
	return list_of_positives


def get_vertices_list_as_vertices_status_dict(vertices_list):
	vertices_status_dict = dict()
	for vertex in vertices_list:
		vertices_status_dict[vertex] = False
	return vertices_status_dict


def get_vertices_status_dict_of_graph(graph: g.Graph):
	vertices_status = dict()
	vertices_with_people = get_vertices_with_positive_num_of_people(graph)
	for vertex in graph.get_vertices():
		vertices_status[vertex] = True
	for vertex in vertices_with_people:
		vertices_status[vertex] = False
	return vertices_status


def create_vertices_list_size(n):
	v_list = []
	for i in range(n):
		v = 'v' + str(i + 1)
		v_list.append(v)
	return v_list


def create_clique_graph_file_size(n):
	v_list = create_vertices_list_size(n)
	with open('graph.txt', 'w+') as file:
		for vertex_name in v_list:
			str_to_write = 'V ' + vertex_name + ' ' + '3' + '\n'
			file.write(str_to_write)
		for vertex_name in v_list:
			for other_vertex_name in v_list:
				if vertex_name != other_vertex_name:
					if abs(int(vertex_name[1:]) - int(other_vertex_name[1:])) == 1 or (
							(vertex_name[1:] == "1" and other_vertex_name[1:] == str(n)) or (
							vertex_name[1:] == str(n) and other_vertex_name[1:] == "1")):
						file.write('E ' + vertex_name + ' ' + other_vertex_name + ' 6' + '\n')
					else:
						file.write('E ' + vertex_name + ' ' + other_vertex_name + ' 1' + '\n')


def query_number_from_user(text, limit):
	inserted_valid_value = False
	inserted_num = 0
	inserted_value = None
	while not inserted_valid_value:
		inserted_value = input(text)
		if inserted_value == 'exit':
			exit(0)
		try:
			inserted_num = int(inserted_value)
			if limit > inserted_num > 0:
				inserted_valid_value = True
			else:
				print('invalid value: ' + inserted_value + '.. should be a number smaller than ' + str(limit))
		except ValueError:
			print('invalid value: ' + inserted_value + '.. should be a number smaller than ' + str(limit))
	return inserted_num


def get_starting_vertices(graph: g.Graph, name1, name2):
	return graph.get_vertex(name1), graph.get_vertex(name2)


if __name__ == "__main__":
	WORLD = generate_graph("Assignment 2/input.txt")
	print('Please enter the desired type of game:\n')
	print('For Adversarial with Alpha-Beta Pruning press 1')
	print('For Semi-Cooperative press 2')
	print('for Fully-Cooperative press 3')
	game_type = query_number_from_user('', 4)
	print("THE VERTICES: ", v.get_vertices_list_as_string(WORLD.get_vertices()))
	print("Choose starting vertex for first agent:")
	max_starting_vertex = WORLD.get_vertex(input())
	print("Choose starting vertex for second agent:")
	min_starting_vertex = WORLD.get_vertex(input())
	vertices_status = get_vertices_status_dict_of_graph(WORLD)
	max_agent = None
	min_agent = None
	if game_type == 1:
		max_agent = a.MaxAgent(max_starting_vertex, min_starting_vertex, vertices_status,[max_starting_vertex, 0, max_starting_vertex], None, None, True)
		min_agent = a.MinAgent(max_starting_vertex, min_starting_vertex, vertices_status,[min_starting_vertex, 0, min_starting_vertex], max_agent, None, True)
		max_agent.other_agent = min_agent

	elif game_type == 2:
		max_agent = a.MaxAgent(max_starting_vertex, min_starting_vertex, vertices_status, [max_starting_vertex, 0, max_starting_vertex], None, cmp.max_semi_cooperative_comparator, False)
		min_agent = a.MinAgent(max_starting_vertex, min_starting_vertex, vertices_status, [min_starting_vertex, 0, min_starting_vertex], max_agent, cmp.min_semi_cooperative_comparator, False)
		max_agent.other_agent = min_agent

	else:
		max_agent = a.MaxAgent(max_starting_vertex, min_starting_vertex, vertices_status, [max_starting_vertex, 0, max_starting_vertex], None, cmp.fully_cooperative_comparator, False)
		min_agent = a.MinAgent(max_starting_vertex, min_starting_vertex, vertices_status, [min_starting_vertex, 0, min_starting_vertex], max_agent, cmp.fully_cooperative_comparator, False)
		max_agent.other_agent = min_agent

	print("THE WORLD:\n", WORLD, "\nDEADLINE: ", TIME_LIMIT, "CUTOFF: ", CUTOFF)
	agent_list = [max_agent, min_agent]
	i = 0
	while not a.all_agents_terminated(agent_list):
		agent_list[i].act(WORLD)
		i += 1
		i = i % 2

	for agent in agent_list:
		print(agent)

	print("WORLD AT END:\n", WORLD)