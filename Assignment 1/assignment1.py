import graph as g
from queue import PriorityQueue
import vertex as v
import sys

if __name__ == "__main__":
    world = g.generate_graph("graph.txt")
    # distances, prevs = g.run_dijkstra(world, world.get_vertex("Arad"))
    q = PriorityQueue()
    print(sys.maxsize)
    q.put(v.VertexWrapper(v.Vertex("a", 1), 4))
    q.put(v.VertexWrapper(v.Vertex("b", 1), 7))

    print(q.get().vertex)
    print(q.get().vertex)

