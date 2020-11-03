import vertex as v
import graph as g
import state as s
import priority_queue as pq


def generate_sequence(world: g.Graph, vertex_wrapper):
	if vertex_wrapper.parent is None:
		return [vertex_wrapper.state.current_vertex]
	edge_weight = world.get_edge_weight(vertex_wrapper.state.vertex, vertex_wrapper.parent.state.vertex)
	current_move = []
	for i in range(edge_weight):
		current_move.append(vertex_wrapper.vertex)
	return generate_sequence(world, vertex_wrapper.parent).extend(current_move)


def g(vertex_wrapper: v.VertexWrapper):
	return vertex_wrapper.acc_weight


def goal_test(state):
	return state.amount_to_save() == 0


class Agent:

	def __init__(self, state, h):
		self.state = state
		self.h = h
		self.score = 0
		self.terminated = False
		self.act_sequence = []

	def do_search(self, world, fringe):
		counter = 0
		fringe.insert(v.VertexWrapper(self.state, None, 0))
		while not fringe.is_empty:
			current_vertex_wrapper = fringe.pop()
			current_vertex = current_vertex_wrapper.state.current_vertex
			acc_weight = current_vertex_wrapper.acc_weight
			current_vertex_wrapper.state.save_current_vertex()
			if goal_test(current_vertex_wrapper.state):
				self.act_sequence = generate_sequence(world, current_vertex_wrapper)
				return counter, True
			counter += 1
			for neighbor_tup in world.expand(current_vertex):
				neighbor_state = s.State(world, neighbor_tup[0], current_vertex_wrapper.state.vertices_status)
				neighbor_vertex_wrapper = v.VertexWrapper(neighbor_state, current_vertex_wrapper, acc_weight + neighbor_tup[1])
				fringe.insert(neighbor_vertex_wrapper)
		return counter, False


class GreedyAgent(Agent):

	def __init__(self, state, h):
		super().__init__(state, h)

	def search(self):
		fringe = pq.PriorityQueue(self.h)
		return self.do_search(self.state.world, fringe)


class AStarAgent(Agent):

	def __int__(self, state, h):
		super().__init__(state, h)

	def search(self):
		fringe = pq.PriorityQueue(lambda x: self.h(x) + g(x))
		return self.do_search(self.state.world, fringe)

# def move(self, graph):
# 	next_vertex = self.sequence[0]
# 	edge_weight = graph.edge_weight(self.current_vertex, next_vertex)
# 	move_description = "MOVING
# 	FROM " + self.current_vertex.name + "TO " + next_vertex.name + " : " + str(
# 		edge_weight)
# 	self.in_edge_progress = edge_weight
# 	self.current_vertex = next_vertex
# 	self.sequence = self.sequence[1:]
# 	return move_description
#
# def save(self):
# 	amount_of_people = self.current_vertex.num_of_people
# 	self.score = self.score + amount_of_people
# 	self.current_vertex.num_of_people = 0
# 	move_description = "saved " + str(amount_of_people) + " people from " + self.current_vertex.name
# 	return move_description
#
# def act(self, graph):
# 	if self.terminated:
# 		return "TERMINATED"
#
# 	if self.in_edge_progress > 0:
# 		self.in_edge_progress = self.in_edge_progress - 1
# 		return "IN EDGE PROGRESS: " + str(self.in_edge_progress)
#
# 	elif len(self.sequence) > 0:
# 		save_description = self.save()
# 		move_description = self.move(graph)
# 		return save_description + "," + move_description
#
# 	if len(self.sequence) == 0:
# 		distances, prevs = g.run_dijkstra(graph, self.current_vertex)
# 		min_distance = sys.maxsize
# 		destination = None
# 		for vertex in distances.keys():
# 			if vertex.num_of_people > 0 and min_distance > distances[vertex] and vertex is not self.current_vertex:
# 				destination = vertex
# 				min_distance = distances[vertex]
# 		if destination is None:
# 			self.terminated = True
# 			return self.save() + ", " + "TERMINATED"
# 		else:
# 			vertex_in_path = destination
# 			while vertex_in_path is not self.current_vertex:
# 				self.sequence.insert(0, vertex_in_path)
# 				vertex_in_path = prevs[vertex_in_path]
# 			return "expanded"
