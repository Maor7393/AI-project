import agent

class Greedy(agent.Agent):

	def __init__(self, vertex):
		super().__init__(vertex)
		self.sequence = []
		self.progress = 0
		