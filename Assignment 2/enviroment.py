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

# def mst_heuristic(vertex_wrapper):
#     global world
#     unsaved_vertices = vertex_wrapper.state.get_unsaved_vertices()
#     essential_vertices = unsaved_vertices
#     if vertex_wrapper.state.current_vertex not in essential_vertices:
#         essential_vertices.append(vertex_wrapper.state.current_vertex)
#     zipped_graph = g.zip_graph(world, essential_vertices)
#     mst_zipped = zipped_graph.MST()
#     return mst_zipped.get_sum_weights()


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
    return graph.get_vertex(name1),graph.get_vertex(name2)


def adversarial_comparator(tuple1, tuple2):
    mine_delta = tuple1[0] - tuple1[1]
    his_delta = tuple2[0] - tuple2[1]
    return True if mine_delta >= his_delta else False

def max_semi_coop_comparator(tuple1, tuple2):
    if tuple1 is None:
        return False
    return True if tuple1[0] > tuple2[0] or (tuple1[0] == tuple2[0] and tuple1[1] >= tuple2[1])  else False


def min_semi_coop_comparator(tuple1, tuple2):
    if tuple1 is None:
        return False
    return True if tuple1[1] > tuple2[1] or (tuple1[1] == tuple2[1] and tuple1[0] >= tuple2[0]) else False


def fully_coop_comparator(tuple1, tuple2):
    if tuple1 is None:
        return False
    return True if tuple1[0] + tuple1[1] > tuple2[0] + tuple2[1] else False


if __name__ == "__main__":
    program_variables.WORLD = generate_graph("graph.txt")
    print("THE WORLD:\n", program_variables.WORLD)
    vertices_status = get_vertices_status_dict_of_graph(program_variables.WORLD)
    max_starting_vertex, min_starting_vertex = get_starting_vertices(program_variables.WORLD, "v1", "v3")
    max_agent = a.MaxAgent(max_starting_vertex, min_starting_vertex, vertices_status, None, adversarial_comparator)
    min_agent = a.MinAgent(max_starting_vertex, min_starting_vertex, vertices_status, max_agent, adversarial_comparator)
    max_agent.other_agent = min_agent
    agent_list = [max_agent, min_agent]
    i = 0
    while not a.all_agents_terminated(agent_list):
        agent_list[i].act()
        i += 1
        i = i % 2
