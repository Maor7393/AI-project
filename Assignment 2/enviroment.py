import graph as g
import vertex as v
import agent as a
import program_variables


def generate_time_limit(file_name):
    file = open(file_name)
    lines = file.readlines()
    line = lines[0]
    line = line.split(' ')
    time = int(line[1])
    file.close()
    return time


world = None


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


def mst_heuristic(vertex_wrapper):
    global world
    unsaved_vertices = vertex_wrapper.state.get_unsaved_vertices()
    essential_vertices = unsaved_vertices
    if vertex_wrapper.state.current_vertex not in essential_vertices:
        essential_vertices.append(vertex_wrapper.state.current_vertex)
    zipped_graph = g.zip_graph(world, essential_vertices)
    mst_zipped = zipped_graph.MST()
    return mst_zipped.get_sum_weights()


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


def create_agent(agent_type, starting_vertex, world):
    positive_vertices = get_vertices_with_positive_num_of_people(world)
    vertices_status = get_vertices_list_as_vertices_status_dict(positive_vertices)
    if agent_type == 1:
        return a.GreedyAgent(starting_vertex, vertices_status, mst_heuristic)
    elif agent_type == 2:
        return a.AStarAgent(starting_vertex, vertices_status, mst_heuristic)
    elif agent_type == 3:
        return a.RealTimeAStarAgent(starting_vertex, vertices_status, mst_heuristic)


if __name__ == "__main__":
    pass
    # print('----Welcome to Hurricane Evacuation Problem----')
    # world = generate_graph("graph.txt")
    #
    # agent_list = []
    # num_of_agents = query_number_from_user('Please enter the number of desired agents: ', 1000)
    #
    # for i in range(1, num_of_agents + 1):
    #     print('Please enter the desired type for agent number ' + str(i) + ':')
    #     print('for greedy press 1')
    #     print('a* press 2')
    #     print('for a* real time press 3')
    #     agent_type = query_number_from_user('', 4)
    #     vertices_names = world.vertices_names()
    #     print('Please enter starting vertex number: ')
    #     picked_valid_vertex = False
    #     starting_vertex = None
    #     while not picked_valid_vertex:
    #         for j in range(1, len(vertices_names) + 1):
    #             print(str(j) + ') ' + vertices_names[j - 1])
    #         starting_vertex_index = query_number_from_user('insert vertex number and press Enter ',
    #                                                        len(vertices_names) + 1)
    #         starting_vertex_index -= 1
    #         starting_vertex = world.get_vertex(vertices_names[starting_vertex_index])
    #         if starting_vertex is not None:
    #             picked_valid_vertex = True
    #         else:
    #             print('Please pick a valid vertex')
    #     new_agent = create_agent(agent_type, starting_vertex, world)
    #     agent_list.append(new_agent)
    # program_deadline = query_number_from_user('Enter program time limit: ', 10001)
    # program_variables.TIME_LIMIT = program_deadline
    #
    # print('world: ')
    # print(world)
    # input('Press Enter to start..')
    #
    # i = 0
    # while not a.all_agents_terminated(agent_list):
    #     agent_list[i].act(world)
    #     i += 1
    #     i = i % num_of_agents
    # for agent in agent_list:
    #     print(agent)
    #
    # print("World at End: ")
    # print(world)
# create_clique_graph_file_size(15)
#
# positive_vertices = get_vertices_with_positive_num_of_people(world)
# vertices_status = get_vertices_list_as_vertices_status_dict(positive_vertices)
# print("World at start: \n" + str(world) + "\n")
# greedy = a.GreedyAgent(world.get_vertex("v0"), vertices_status, mst_heuristic)
# astar = a.AStarAgent(world.get_vertex("v0"), vertices_status, mst_heuristic)
# realtime_astar = a.RealTimeAStarAgent(world.get_vertex("v0"), vertices_status, mst_heuristic)
# saboteur = Saboteur(world.get_vertex("v0"))
# agent_list = [greedy, astar, realtime_astar]

# i = 0
# while not a.all_agents_terminated(agent_list):
# 	agent_list[i].act(world)
# 	i += 1
# 	i = i % (len(agent_list))

# print("\n\nWorld at the end: \n" + str(world))
