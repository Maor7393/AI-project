import vertex as v
import graph as g
import state as s
import priority_queue as pq
from enviroment import Limits


def generate_sequence(world: g.Graph, vertex_wrapper):
	if vertex_wrapper.parent_wrapper is None:
		return [vertex_wrapper.state.current_vertex]
	edge_weight = world.get_edge_weight(vertex_wrapper.state.current_vertex,
	                                    vertex_wrapper.parent_wrapper.state.current_vertex)
	print(world)
	print(vertex_wrapper.state.current_vertex, vertex_wrapper.parent_wrapper.state.current_vertex)
	print('edge weight: ' + str(edge_weight))
	current_move = []
	for i in range(edge_weight):
		current_move.append(vertex_wrapper.state.current_vertex)
	current_sequence = generate_sequence(world, vertex_wrapper.parent_wrapper)
	current_sequence.extend(current_move)
	return current_sequence


def g(vertex_wrapper: v.VertexWrapper):
	return vertex_wrapper.acc_weight


def goal_test(state):
	return state.amount_to_save() == 0


def all_agents_terminated(agent_list):
	all_terminated = True
	for agent in agent_list:
		if not agent.terminated:
			all_terminated = False
			break
	return all_terminated


class Agent:

	def __init__(self, starting_vertex, vertices_status, h):
		self.state = s.State(starting_vertex, vertices_status)
		self.h = h
		self.score = 0
		self.terminated = False
		self.act_sequence = []
		self.num_of_expansions = 0
		self.num_of_movements = 0
		self.time_passed = 0

	def search_with_limit(self, world, fringe, limit):
		counter = 0
		fringe.insert(v.VertexWrapper(self.state, None, 0))
		while not fringe.is_empty():
			current_vertex_wrapper = fringe.pop()
			current_vertex = current_vertex_wrapper.state.current_vertex
			acc_weight = current_vertex_wrapper.acc_weight
			current_vertex_wrapper.state.save_current_vertex()
			if counter == limit or goal_test(current_vertex_wrapper.state):
				self.act_sequence = generate_sequence(world, current_vertex_wrapper)
				break
			counter += 1
			for neighbor_tup in world.expand(current_vertex):
				neighbor_state = s.State(world, neighbor_tup[0], current_vertex_wrapper.state.vertices_status)
				neighbor_vertex_wrapper = v.VertexWrapper(neighbor_state, current_vertex_wrapper, acc_weight + neighbor_tup[1])
				fringe.insert(neighbor_vertex_wrapper)
		self.num_of_expansions += counter
		if fringe.is_empty():
			self.terminated = True
		return counter

	def search(self, world, limit):
		pass

	def act_with_limit(self, world, limit):
		if not self.terminated:
			self.state.update_vertices_status(world)
			if len(self.act_sequence) == 0:
				expansions_in_search = self.search(world, limit)
				self.time_passed += Limits.T * expansions_in_search

			if not self.terminated and self.time_passed <= Limits.TIME_LIMIT:
				self.move(world)
			else:
				self.terminated = True

	def move(self, world):
		next_vertex = self.act_sequence[0]
		self.score += next_vertex.num_of_people
		next_vertex.num_of_people = 0
		self.state.current_vertex = next_vertex
		self.time_passed += 1
		self.act_sequence = self.act_sequence[1:]

	def __str__(self):
		print("-------------------------")
		print(type(self).__name__)
		print("Score: " + str(self.score))
		print("Number of expansions: " + str(self.num_of_expansions))
		print("Number of movements" + str(self.num_of_movements))
		print("Total time passed" + str(self.time_passed))
		print("-------------------------")


class GreedyAgent(Agent):

	def __init__(self, starting_vertex, vertices_status, h):
		super().__init__(starting_vertex, vertices_status, h)

	def search(self, world, limit):
		fringe = pq.PriorityQueue(self.h)
		return self.search_with_limit(world, fringe, limit)

	def act(self, world):
		return self.act_with_limit(world, Limits.GREEDY_LIMIT)


class AStarAgent(Agent):

	def __int__(self, starting_vertex, vertices_status, h):
		super().__init__(starting_vertex, vertices_status, h)

	def search(self, world, limit):
		fringe = pq.PriorityQueue(lambda x: self.h(x) + g(x))
		return self.search_with_limit(world, fringe, limit)

	def act(self, world):
		return self.act_with_limit(world, Limits.ASTAR_LIMIT)


class RealTimeAStarAgent(Agent):

	def __int__(self, starting_vertex, vertices_status, h):
		super().__init__(starting_vertex, vertices_status, h)

	def search(self, world, limit):
		fringe = pq.PriorityQueue(lambda x: self.h(x) + g(x))
		return self.search_with_limit(world, fringe, limit)

	def act(self, world):
		return self.act_with_limit(world, Limits.REALTIME_ASTAR_LIMIT)
