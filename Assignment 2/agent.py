from program_variables import WORLD
from program_variables import TIME_LIMIT
import state as s


def all_agents_terminated(agent_list):
	all_terminated = True
	for agent in agent_list:
		if not agent.terminated:
			all_terminated = False
			break
	return all_terminated


class Agent:
	num_of_real_movements = 0

	def __init__(self, max_starting_vertex, min_starting_vertex, vertices_status, other_agent, comparator):
		self.state = s.State(s.Location(max_starting_vertex, 0, max_starting_vertex), s.Location(min_starting_vertex, 0, min_starting_vertex), vertices_status, 0, 0, 0)
		self.comparator = comparator
		self.other_agent = other_agent
		self.terminated = False
		self.act_sequence = []
		self.real_score = 0

	def act(self):
		print("------ " + type(self).__name__ + " ------")
		if not self.terminated:
			if self.act_sequence[1] > 0 and Agent.num_of_real_movements < TIME_LIMIT:
				self.move_with_update_location()
			elif Agent.num_of_real_movements >= TIME_LIMIT:
				self.terminated = True
				print("TERMINATED\n")
			elif self.act_sequence[1] == 0:
				self.save_current_vertex()
				self.update_state()
				self.act_sequence = self.minimax(self.state)
		else:
			print("TERMINATED\n")

	def minimax(self, state: s.State):
		pass

	def update_state(self):
		pass

	def move_with_update_location(self):
		pass

	def save_current_vertex(self):
		current_vertex = self.act_sequence[2]
		if current_vertex.num_of_people > 0:
			print("Saving: " + str(current_vertex))
			self.real_score += current_vertex.num_of_people
			current_vertex.num_of_people = 0

	def move_in_edge(self):
		Agent.num_of_real_movements += 1
		print("Current sequence: " + str(self.act_sequence[0]) + ", " + str(self.act_sequence[1]) + ", " + str(self.act_sequence[2]))
		self.act_sequence[1] -= 1
		print("Moved, sequence is: " + str(self.act_sequence[0]) + ", " + str(self.act_sequence[1]) + ", " + str(self.act_sequence[2]))

	def __str__(self):
		agent_str = "-------------------------\n"
		agent_str += type(self).__name__ + "\n"
		agent_str += "Score: " + str(self.real_score) + "\n"
		agent_str += "Number of movements: " + str(Agent.num_of_real_movements) + "\n"
		agent_str += "Agent State: " + str(self.state) + "\n"
		agent_str += "-------------------------\n"
		return agent_str

	def max_value(self, state, num_of_plys):
		if state.terminal_state(num_of_plys):
			return state.evaluate()
		best_value = None
		for next_state in state.successor("MAX"):
			next_state_min_value = self.min_value(next_state, num_of_plys + 1)
			if not self.comparator(best_value, next_state_min_value):
				best_value = next_state_min_value
		return best_value

	def min_value(self, state: s.State, num_of_plys):
		if state.terminal_state(num_of_plys):
			return state.evaluate()
		best_value = None
		for next_state in state.successor("MIN"):
			next_state_max_value = self.max_value(next_state, num_of_plys + 1)
			if self.comparator(best_value, next_state_max_value):
				best_value = next_state_max_value
		return best_value


class MaxAgent(Agent):

	def __init_(self, max_starting_vertex, min_starting_vertex, vertices_status, min_agent, comparator):
		self.act_sequence = [max_starting_vertex, 0, max_starting_vertex]
		super().__init__(max_starting_vertex, min_starting_vertex, vertices_status, min_agent, comparator)

	def move_with_update_location(self):
		self.move_in_edge()
		self.state.max_agent_current_location.edge_progress -= 1

	def update_state(self):
		self.state.min_agent_current_location = self.other_agent.state.min_agent_current_location
		self.state.update_vertices_status(WORLD)
		self.state.max_agent_score = self.real_score
		self.state.min_agent_score = self.other_agent.real_score
		self.state.total_simulated_movements = Agent.num_of_real_movements

	def minimax(self, state: s.State):
		current_vertex = self.act_sequence[2]
		best_value = None
		best_edge = None
		num_of_plys = 0
		for neighbor_tup in WORLD.expand(current_vertex):
			checked_location = s.Location(current_vertex, neighbor_tup[1] - 1, neighbor_tup[0])
			new_state = state.get_new_state()
			new_state.max_agent_current_location = checked_location
			value_of_new_state = self.min_value(new_state, num_of_plys + 1)
			if best_value is None:
				best_value = value_of_new_state
				best_edge = neighbor_tup
			elif not self.comparator(best_value, value_of_new_state):
				best_value = value_of_new_state
				best_edge = neighbor_tup
		return [current_vertex, best_edge[1], best_edge[0]]


class MinAgent(Agent):

	def __init_(self, max_starting_vertex, min_starting_vertex, vertices_status, min_agent, comparator):
		self.act_sequence = [min_starting_vertex, 0, min_starting_vertex]
		super().__init__(max_starting_vertex, min_starting_vertex, vertices_status, min_agent, comparator)

	def move_with_update_location(self):
		self.move_in_edge()
		self.state.min_agent_current_location.edge_progress -= 1

	def update_state(self):
		self.state.max_agent_current_location = self.other_agent.state.max_agent_current_location
		self.state.update_vertices_status(WORLD)
		self.state.total_simulated_movements = Agent.num_of_real_movements
		self.state.max_agent_score = self.other_agent.real_score
		self.state.min_agent_score = self.real_score

	def minimax(self, state: s.State):
		current_vertex = self.act_sequence[2]
		best_value = None
		best_edge = None
		num_of_plys = 0
		for neighbor_tup in WORLD.expand(current_vertex):
			checked_location = s.Location(current_vertex, neighbor_tup[1] - 1, neighbor_tup[0])
			new_state = state.get_new_state()
			new_state.max_agent_current_location = checked_location
			value_of_new_state = self.max_value(new_state, num_of_plys + 1)
			if self.comparator(best_value, value_of_new_state):
				best_value = value_of_new_state
				best_edge = neighbor_tup
		return [current_vertex, best_edge[1], best_edge[0]]

