import names


def make_table(entries: list, values: list):
	table = Table()
	entries_values = zip(entries, values)
	for entry_value in entries_values:
		entry = entry_value[0]
		value = entry_value[1]
		table.add_entry(entry, value)
	return table


class Table:

	def __init__(self):
		self.table_dict = {}

	# entry is a row in the prob table. for example T T 0.4
	def add_entry(self, tuples: list, value: float):
		if tuples[0] == names.empty:
			self.table_dict[names.empty] = value
		else:
			if len(tuples) > 1:
				self.table_dict[tuple(tuples)] = value
			else:
				self.table_dict[tuples[0]] = value

	def get_probability_given_parents(self, value: bool, parents: list) -> float:
		if len(parents) == 0:
			if value is True:
				return self.table_dict[names.empty]
			else:
				return 1 - self.table_dict[names.empty]
		elif len(parents) == 1:
			parent_tuple = parents[0]
			if value is True:
				return self.table_dict[parent_tuple]
			else:
				return 1-self.table_dict[parent_tuple]
		else:
			parents_tuples = tuple(parents)
			if self.table_dict.get(parents_tuples) is None:
				first = parents_tuples[0]
				second = parents_tuples[1]
				parents_tuples = (second, first)

			if value is True:
				return self.table_dict[parents_tuples]
			else:
				return 1-self.table_dict[parents_tuples]



