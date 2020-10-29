import agent
import sys
import graph as g


class Greedy(agent.Agent):

	def __init__(self, vertex):
		super().__init__(vertex)
		self.sequence = []
		self.in_edge_progress = 0

	def move(self, graph):
		next_vertex = self.sequence[0]
		edge_weight = graph.edge_weight(self.current_vertex, next_vertex)
		move_description = "MOVING FROM " + self.current_vertex.name + "TO " + next_vertex.name + " : " + str(edge_weight)
		self.in_edge_progress = edge_weight
		self.current_vertex = next_vertex
		self.sequence = self.sequence[1:]
		return move_description

	def save(self):
		amount_of_people = self.current_vertex.num_of_people
		self.score = self.score + amount_of_people
		self.current_vertex.num_of_people = 0
		move_description = "SAVED " + str(amount_of_people)
		return move_description

	def act(self, graph):
		if self.terminated:
			return "TERMINATED"
		if len(self.sequence) == 0:
			save_description = ""
			if self.current_vertex.num_of_people > 0:
				save_description = self.save()

			distances, prevs = g.run_dijkstra(graph, self.current_vertex)
			min_distance = sys.maxsize
			destination = None
			for vertex in distances.keys():
				if vertex.number_of_people > 0 and min_distance > distances[vertex]:
					destination = vertex
					min_distance = distances[vertex]

			if destination is None:
				self.terminated = True
				return "TERMINATED"
			else:
				vertex_in_path = destination
				while vertex_in_path is not self.current_vertex:
					self.sequence.insert(0, vertex_in_path)
					vertex_in_path = prevs[vertex_in_path]
				return save_description + "," + self.move(graph)

		elif self.in_edge_progress > 0:
			self.in_edge_progress = self.in_edge_progress - 1
			return "IN EDGE PROGRESS: " + str(self.in_edge_progress)

		else:
			move_description = self.move(graph)
			save_description = ''
			if len(self.sequence) is 0:
				save_description = self.save()
			return save_description + ","+ move_description