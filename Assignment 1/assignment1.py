import graph as g
import vertex as v
import priority_queue as pq
import agent as a
import state as s
import copy


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


if __name__ == "__main__":
    world, total_time = generate_program_variables("graph.txt")
    print('world: ' + str(world))
    zipped = g.zip_graph(world, [world.get_vertex("v1"), world.get_vertex("v4")])
    zipped2 = g.zip_graph(zipped, [world.get_vertex("v4")])
    fringe = pq.PriorityQueue(mst_heuristic)
    essential_vertices = []
    for vertex in world.get_vertices():
        if vertex.num_of_people > 0:
            essential_vertices.append(vertex)
    zipped = g.zip_graph(world, [world.get_vertex("v1"), world.get_vertex("v4")])
    state = s.State(zipped, zipped.get_vertex("v1"), {zipped.get_vertex("v1"): False, zipped.get_vertex("v4"): False})
    greedy = a.GreedyAgent(state, mst_heuristic)
    print(greedy.search())
    print('sequence: ' + str(greedy.act_sequence))


    # distances, prevs = g.run_dijkstra(world, world.get_vertex("Arad"))
    # agent = Greedy(world.get_vertex("Arad"))
    # time_passed = 0
    # while not agent.is_terminated() and time_passed < total_time:
    #     message = agent.act(world)
    #     print(message)
    #     time_passed = time_passed + 1

    # print("Agent Score: " + str(agent.score))
    # print(world)
