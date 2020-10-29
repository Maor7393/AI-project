import graph as g

if __name__ == "__main__":
    world = g.generate_graph("graph.txt")
    distances, prevs = g.run_dijkstra(world, world.get_vertex("Arad"))
    print(distances)
