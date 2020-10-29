import graph as g
from greedy import Greedy


if __name__ == "__main__":
    world = g.generate_graph("graph.txt")
    distances, prevs = g.run_dijkstra(world, world.get_vertex("Arad"))
    agent = Greedy(world.get_vertex("Arad"))
    while not agent.is_terminated():
        message = agent.act(world)
        print(message)
    print(agent.score)
    print(world)

