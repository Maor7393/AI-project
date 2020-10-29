import graph as g
import priority_queue as pq
import vertex as v
from queue import PriorityQueue


if __name__ == "__main__":
    world = g.generate_graph("graph.txt")
    distances, prevs = g.run_dijkstra(world, world.get_vertex("Arad"))
    print(distances)
