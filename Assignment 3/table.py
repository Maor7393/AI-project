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

    def add_entry(self, tuples: list, value: float):
        if tuples[0] == names.empty:
            self.table_dict[(names.empty)] = value
        else:
            self.table_dict[tuple(tuples)] = value

    def get_entry(self, evidence: list):
        pass
        # TODO: implement dont forget to check opposite

    def __str__(self):
        s = ""
        s += "-------------------------------"
        for table_entry in self.table_dict.keys():
            s += "P(True | " + str(table_entry) + ")= " + str(self.table_dict.get(table_entry)) + "\n"
            s += "P(False | " + str(table_entry) + ")= " + str(1 - self.table_dict.get(table_entry)) + "\n"
        s += "-------------------------------\n"
        return s
