class Table:

    def __init__(self):
        self.table_dict = {}

    def add_entry(self, tuples: list[tuple], value: int):
        if len(tuples) == 0:
            self.table_dict[()] = value
        else:
            self.table_dict[tuple(tuples)] = value

    def get_entry(self, evidence: list[tuple]):
        pass
        # TODO: implement
