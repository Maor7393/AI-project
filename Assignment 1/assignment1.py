import graph as g
import vertex as v

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
            vertex = v.Vertex(name, number_of_people)
            name_vertices_dict[vertex.name] = vertex
            output_graph.add_vertex(vertex)
        elif element_type == 'E':
            source_name = line[1]
            target_name = line[2]
            edge_weight = int(line[3])
            v1 = name_vertices_dict[source_name]
            v2 = name_vertices_dict[target_name]
            output_graph.add_edge(v1, v2, edge_weight)
    return output_graph, time


if __name__ == "__main__":
    world, total_time = generate_program_variables("graph.txt")
    distances, prevs = g.run_dijkstra(world, world.get_vertex("Arad"))
    agent = Greedy(world.get_vertex("Arad"))
    time_passed = 0
    while not agent.is_terminated() and time_passed < total_time:
        message = agent.act(world)
        print(message)
        time_passed = time_passed + 1

    print("Agent Score: " + str(agent.score))
    print(world)
