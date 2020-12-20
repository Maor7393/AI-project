from table import Table


class Node:

    def __init__(self, name: str, table: Table):
        self.name = name
        self.table = table

    def __str__(self):
        s = ""
        s += "Node Name: " + self.name + "\n"
        s += "Probability Table: " + "\n"
        s += str(self.table)

        return s
