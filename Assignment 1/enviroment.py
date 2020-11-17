import graph as g
import vertex as v
import agent as a
from saboteur import Saboteur


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
                    if abs(int(vertex_name[1:]) - int(other_vertex_name[1:])) == 1 or ((vertex_name[1:] == "1" and other_vertex_name[1:] == str(n)) or (vertex_name[1:] == str(n) and other_vertex_name[1:] == "1")):
                        file.write('E ' + vertex_name + ' ' + other_vertex_name + ' 6' + '\n')
                    else:
                        file.write('E ' + vertex_name + ' ' + other_vertex_name + ' 1' + '\n')


if __name__ == "__main__":
    world = generate_graph("graph.txt")
    positive_vertices = get_vertices_with_positive_num_of_people(world)
    vertices_status = get_vertices_list_as_vertices_status_dict(positive_vertices)
    print("World at start: \n" + str(world) + "\n")
    greedy = a.GreedyAgent(world.get_vertex("v1"), vertices_status, mst_heuristic)
    astar = a.AStarAgent(world.get_vertex("v1"), vertices_status, mst_heuristic)
    realtime_astar = a.RealTimeAStarAgent(world.get_vertex("v1"), vertices_status, mst_heuristic)
    agent_list = [greedy, astar, realtime_astar]

    i = 0
    while not a.all_agents_terminated(agent_list):
        agent_list[i].act(world)
        i += 1
        i = i % (len(agent_list))

    print("\n\nWorld at the end: \n" + str(world))
    for agent in agent_list:
        print(agent)
