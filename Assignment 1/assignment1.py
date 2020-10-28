import graph

import vertex

if __name__ == "__main__":
	print("hi")
	graph = graph.Graph();

def generateGraph(file_name):
	graph = graph.Graph()
	file = open(file_name)
	lines = file.readlines()
	vertices = {}
	for line in lines:
		type = line[0]
		line = line.split(' ')
		if type == 'V':
			name = line[1]
			number_of_people = line[2]
			v = vertex(name, number_of_people)
			vertices[v.name] = v
			graph.add_vertex(v)          
		elif type == 'E':
			source_name = line[1]
			target_name = line[2]
			edge_weight = line[3] 
			v1 = vertices[source_name]
			v2 = vertices[target_name]
			graph.add_edge(v1, v2, edge_weight)
	