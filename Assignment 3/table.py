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

    def get_entry(self, evidence: list):
        pass
        # TODO: implement dont forget to check opposite

