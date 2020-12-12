from program_variables import TIME_LIMIT
import state as s
from graph import Graph
from vertex import all_vertex_saved
from vertex import get_vertices_list_as_string


def all_agents_terminated(agent_list):
	all_terminated = True
	for agent in agent_list:
		if not agent.terminated:
			all_terminated = False
			break
	return all_terminated


class Agent:
	num_of_real_movements = 0

	def __init__(self, max_starting_vertex, min_starting_vertex, vertices_status, act_sequence, other_agent, comparator, prune):
		self.state = s.State(s.Location(max_starting_vertex, 0, max_starting_vertex),s.Location(min_starting_vertex, 0, min_starting_vertex), vertices_status, 0, 0, 0)
		self.comparator = comparator
		self.other_agent = other_agent
		self.terminated = False
		self.total_sequence = [act_sequence[2]]
		self.saved_vertices = []
		self.act_sequence = act_sequence
		self.pruning = prune
		self.real_score = 0

	def act(self, WORLD: Graph):
		print("------ " + type(self).__name__ + " ------")
		self.terminated = all_vertex_saved(WORLD.get_vertices())
		self.save_real_vertex(self.act_sequence[0])
		if not self.terminated:
			if self.act_sequence[1] > 0 and Agent.num_of_real_movements < TIME_LIMIT:
				self.move_with_update_location()
			elif Agent.num_of_real_movements >= TIME_LIMIT:
				self.terminated = True
				print("TERMINATED\n")
			elif self.act_sequence[1] == 0:
				self.update_state(WORLD)
				print("MINIMAXING")
				if not self.pruning:
					self.act_sequence = self.minimax(self.state, WORLD)
				else:
					self.act_sequence = self.minimax_alpha_beta(self.state, WORLD)
				self.total_sequence.append(self.act_sequence[2])
				self.set_new_location(self.act_sequence)
				self.move_with_update_location()
		else:
			print("TERMINATED\n")

	def save_real_vertex(self, vertex):
		if vertex.num_of_people > 0:
			self.saved_vertices.append(vertex)
			print("Saving: " + str(vertex))
			self.real_score += vertex.num_of_people
			vertex.num_of_people = 0

	def move_in_edge(self):
		Agent.num_of_real_movements += 1
		print("Current sequence: " + str(self.act_sequence[0]) + ", " + str(self.act_sequence[1]) + ", " + str(
			self.act_sequence[2]))
		self.act_sequence[1] -= 1
		print("Moved, sequence is: " + str(self.act_sequence[0]) + ", " + str(self.act_sequence[1]) + ", " + str(
			self.act_sequence[2]))
		if self.act_sequence[1] == 0:
			self.save_real_vertex(self.act_sequence[2])

	def __str__(self):
		agent_str = "-------------------------\n"
		agent_str += type(self).__name__ + "\n"
		agent_str += "Score: " + str(self.real_score) + "\n"
		agent_str += "Total number of movements: " + str(Agent.num_of_real_movements) + "\n"
		agent_str += "Path: " + get_vertices_list_as_string(self.total_sequence)
		agent_str += "\nSaved: " + get_vertices_list_as_string(self.saved_vertices)
		agent_str += "\n-------------------------\n"
		return agent_str

	def set_new_location(self, location_params):
		pass

	def minimax(self, state: s.State, WORLD: Graph):
		return []

	def minimax_alpha_beta(self, state: s.State,WORLD: Graph):
		return []

	def update_state(self, WORLD: Graph):
		pass

	def move_with_update_location(self):
		pass

	def max_value_alpha_beta(self, state, num_of_plys, WORLD: Graph, alpha, beta):
		if state.terminal_state(num_of_plys):
			return state.evaluate_alpha_beta()
		v = float('-inf')
		for next_state in state.successor("MAX", WORLD):
			v = max(v, self.min_value_alpha_beta(next_state, num_of_plys + 1, WORLD, alpha, beta))
			if v >= beta:
				return v
			alpha = max(alpha, v)
		return v

	def min_value_alpha_beta(self, state: s.State, num_of_plys, WORLD: Graph,alpha, beta):
		if state.terminal_state(num_of_plys):
			return state.evaluate_alpha_beta()
		v = float('inf')
		for next_state in state.successor("MIN", WORLD):
			v = min(v, self.max_value_alpha_beta(next_state, num_of_plys + 1, WORLD, alpha, beta))
			if v <= alpha:
				return v
			beta = min(beta, v)
		return v


class MaxAgent(Agent):

	def __init_(self, max_starting_vertex, min_starting_vertex, vertices_status, act_sequence, min_agent, comparator, prune):
		super().__init__(max_starting_vertex, min_starting_vertex, vertices_status, act_sequence, min_agent, comparator, prune)

	def move_with_update_location(self):
		self.move_in_edge()
		self.state.max_agent_current_location.edge_progress -= 1

	def set_new_location(self, location_params):
		self.state.max_agent_current_location.set_location_parameters(location_params[0], location_params[1], location_params[2])

	def update_state(self, WORLD):
		self.state.min_agent_current_location = self.other_agent.state.min_agent_current_location
		self.state.update_vertices_status(WORLD)
		self.state.max_agent_score = self.real_score
		self.state.min_agent_score = self.other_agent.real_score
		self.state.simulated_movements = Agent.num_of_real_movements

	def minimax(self, state: s.State, WORLD: Graph):
		best_value = None
		best_edge = None
		num_of_plys = 0
		for next_state in state.successor("MAX", WORLD):
			value_of_new_state = self.min_value(next_state, num_of_plys + 1, WORLD)
			current_edge = WORLD.get_edge(next_state.max_agent_current_location.prev, next_state.max_agent_current_location.successor)
			if best_value is None:
				best_value = value_of_new_state
				best_edge = current_edge
			elif not (best_value == self.comparator(best_value, value_of_new_state)):
				best_value = value_of_new_state
				best_edge = current_edge
		return [best_edge[0], best_edge[1], best_edge[2]]

	def max_value(self, state, num_of_plys, WORLD: Graph):
		if state.terminal_state(num_of_plys):
			return state.evaluate()
		best_value = None
		for next_state in state.successor("MAX", WORLD):
			next_state_min_value = self.min_value(next_state, num_of_plys + 1, WORLD)
			if best_value is None:
				best_value = next_state_min_value
			best_value = self.comparator(best_value, next_state_min_value)
		return best_value

	def min_value(self, state: s.State, num_of_plys, WORLD: Graph):
		if state.terminal_state(num_of_plys):
			return state.evaluate()
		best_value = None
		for next_state in state.successor("MIN", WORLD):
			next_state_max_value = self.max_value(next_state, num_of_plys + 1, WORLD)
			if best_value is None:
				best_value = next_state_max_value
			best_value = self.other_agent.comparator(best_value, next_state_max_value)
		return best_value

	def minimax_alpha_beta(self, state:s.State, WORLD:Graph):
		best_edge = None
		num_of_plys = 0
		v = float('-inf')
		alpha = float('-inf')
		beta = float('inf')
		for next_state in state.successor("MAX", WORLD):
			value_of_new_state = self.min_value_alpha_beta(next_state, num_of_plys + 1, WORLD, alpha, beta)
			current_edge = WORLD.get_edge(next_state.max_agent_current_location.prev,next_state.max_agent_current_location.successor)
			if v < value_of_new_state:
				v = value_of_new_state
				best_edge = current_edge
			alpha = max(v, alpha)
		return [best_edge[0], best_edge[1], best_edge[2]]


class MinAgent(Agent):

	def __init_(self, max_starting_vertex, min_starting_vertex, vertices_status, act_sequence, min_agent, comparator, prune):
		super().__init__(max_starting_vertex, min_starting_vertex, vertices_status, act_sequence, min_agent, comparator, prune)

	def move_with_update_location(self):
		self.move_in_edge()
		self.state.min_agent_current_location.edge_progress -= 1

	def set_new_location(self, location_params):
		self.state.min_agent_current_location.set_location_parameters(location_params[0], location_params[1], location_params[2])

	def update_state(self, WORLD):
		self.state.max_agent_current_location = self.other_agent.state.max_agent_current_location
		self.state.update_vertices_status(WORLD)
		self.state.simulated_movements = Agent.num_of_real_movements
		self.state.max_agent_score = self.other_agent.real_score
		self.state.min_agent_score = self.real_score

	def max_value(self, state, num_of_plys, WORLD: Graph):
		if state.terminal_state(num_of_plys):
			return state.evaluate()
		best_value = None
		for next_state in state.successor("MAX", WORLD):
			next_state_min_value = self.min_value(next_state, num_of_plys + 1, WORLD)
			if best_value is None:
				best_value = next_state_min_value
			best_value = self.other_agent.comparator(best_value, next_state_min_value)
		return best_value

	def min_value(self, state: s.State, num_of_plys, WORLD: Graph):
		if state.terminal_state(num_of_plys):
			return state.evaluate()
		best_value = None
		for next_state in state.successor("MIN", WORLD):
			next_state_max_value = self.max_value(next_state, num_of_plys + 1, WORLD)
			if best_value is None:
				best_value = next_state_max_value
			best_value = self.comparator(best_value, next_state_max_value)
		return best_value

	def minimax(self, state: s.State, WORLD: Graph):
		best_value = None
		best_edge = None
		num_of_plys = 0
		for next_state in state.successor("MIN", WORLD):
			value_of_new_state = self.max_value(next_state, num_of_plys + 1, WORLD)
			current_edge = WORLD.get_edge(next_state.min_agent_current_location.prev, next_state.min_agent_current_location.successor)
			if best_value is None:
				best_value = value_of_new_state
				best_edge = current_edge
			elif not (best_value == self.comparator(best_value, value_of_new_state)):
				best_value = value_of_new_state
				best_edge = current_edge
		return [best_edge[0], best_edge[1], best_edge[2]]

	def minimax_alpha_beta(self, state: s.State, WORLD: Graph):
		best_edge = None
		num_of_plys = 0
		v = float('inf')
		alpha = float('-inf')
		beta = float('inf')
		for next_state in state.successor("MIN", WORLD):
			value_of_new_state = self.max_value_alpha_beta(next_state, num_of_plys + 1, WORLD, alpha, beta)
			current_edge = WORLD.get_edge(next_state.min_agent_current_location.prev, next_state.min_agent_current_location.successor)
			print(v, value_of_new_state)
			if v > value_of_new_state:
				v = value_of_new_state
				best_edge = current_edge
			beta = min(v, beta)
		return [best_edge[0], best_edge[1], best_edge[2]]
