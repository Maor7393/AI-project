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

    def __str__(self):
        s = ""
        s += "-------------------------------"
        for table_entry in self.table_dict.keys():
            s += "P(True | " + str(table_entry) + ")= " + str(self.table_dict.get(table_entry)) + "\n"
            s += "P(False | " + str(table_entry) + ")= " + str(1 - self.table_dict.get(table_entry)) + "\n"
        s += "-------------------------------\n"
        return s
