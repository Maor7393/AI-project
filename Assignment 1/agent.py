import vertex as v
import graph as g
import state as s
import priority_queue as pq
from enviroment import Limits


def generate_sequence(world: g.Graph, vertex_wrapper):
	if vertex_wrapper.parent_wrapper is None:
		return [vertex_wrapper.state.current_vertex]
	edge_weight = world.get_edge_weight(vertex_wrapper.state.current_vertex, vertex_wrapper.parent_wrapper.state.current_vertex)
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
				neighbor_state = s.State(neighbor_tup[0], current_vertex_wrapper.state.vertices_status)
				neighbor_vertex_wrapper = v.VertexWrapper(neighbor_state, current_vertex_wrapper, acc_weight + neighbor_tup[1])
				fringe.insert(neighbor_vertex_wrapper)

		self.num_of_expansions += counter
		if fringe.is_empty():
			self.terminated = True
		return counter

	def search(self, world, limit):
		pass

	def act_with_limit(self, world, limit):
		print("------ " + type(self).__name__ + " ------")
		if not self.terminated:
			self.state.update_vertices_status(world)
			if len(self.act_sequence) == 0:
				expansions_in_search = self.search(world, limit)
				print("Searched, output act sequence is: " + v.get_vertices_list_as_string(self.act_sequence))
				self.time_passed += Limits.T * expansions_in_search
			if not self.terminated and self.time_passed + 1 < Limits.TIME_LIMIT:
				self.move()
			else:
				self.terminated = True
				print("TERMINATED\n")
		else:
			print("TERMINATED\n")

	def save_current_vertex(self):
		print("Saving: " + str(self.state.current_vertex))
		self.score += self.state.current_vertex.num_of_people
		self.state.current_vertex.num_of_people = 0

	def move(self):

		print("Current sequence: " + v.get_vertices_list_as_string(self.act_sequence))
		next_vertex = self.act_sequence[0]
		print("Current Vertex: " + str(self.state.current_vertex))
		print("Moving to: " + str(next_vertex))
		if next_vertex != self.state.current_vertex:
			self.save_current_vertex()
		self.state.current_vertex = next_vertex
		self.time_passed += 1
		self.act_sequence = self.act_sequence[1:]
		if len(self.act_sequence) == 0:
			self.save_current_vertex()

	def __str__(self):
		agent_str = "-------------------------\n"
		agent_str += type(self).__name__ + "\n"
		agent_str += "Score: " + str(self.score) + "\n"
		agent_str += "Number of expansions: " + str(self.num_of_expansions) + "\n"
		agent_str += "Number of movements: " + str(self.num_of_movements) + "\n"
		agent_str += "Total time passed: " + str(self.time_passed) + "\n"
		agent_str += "-------------------------\n"
		return agent_str


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
