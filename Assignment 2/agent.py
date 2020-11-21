import vertex as v
import graph as g
import copy as c
import priority_queue as pq
import program_variables
import state as s


def all_agents_terminated(agent_list):
	all_terminated = True
	for agent in agent_list:
		if not agent.terminated:
			all_terminated = False
			break
	return all_terminated


class Agent: # [V2, 0, V3]

	def __init__(self, max_starting_vertex, min_starting_vertex, vertices_status):
		self.state = s.State(s.Location(max_starting_vertex, 0, max_starting_vertex), s.Location(min_starting_vertex, 0, min_starting_vertex), vertices_status, vertices_status)
		self.my_score = 0
		self.terminated = False
		self.act_sequence = []
		self.num_of_movements = 0

	def act_with_limit(self, world, limit):
		print("------ " + type(self).__name__ + " ------")
		if not self.terminated:
			self.state.update_vertices_status(world)
			if len(self.act_sequence) == 0:
				pass
			if not self.terminated and self.time_passed + 1 < program_variables.TIME_LIMIT:
				self.move()
			else:
				self.terminated = True
				print("TERMINATED\n")
		else:
			print("TERMINATED\n")

	def save_current_vertex(self):
		if self.state.current_vertex.num_of_people > 0:
			print("Saving: " + str(self.state.current_vertex))
			self.score += self.state.current_vertex.num_of_people
			self.state.current_vertex.num_of_people = 0

	def move(self):
		self.num_of_movements += 1
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








