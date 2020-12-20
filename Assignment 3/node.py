from table import Table


class Node:

    def __init__(self, name: str, table: Table):
        self.name = name
        self.table = table

    def __str__(self):
        s = ""
        s += "Node Name: " + self.name + "\n"
        s += "Probability Table: " + "\n"
        s += "-------------------------------\n"
        for table_entry in self.table.table_dict.keys():
            prob = round(self.table.table_dict.get(table_entry), 3)
            s += "P(" + self.name + "= True |  " + str(table_entry) + ")= " + str(
                prob) + "\n"
        s += "-------------------------------\n\n"
        return s
