from table import Table


class Node:

    def __init__(self, name: str, table: Table):
        self.name = name
        self.table = table

    def __str__(self):
        s = ""
        s += "Node Name: " + self.name + "\n"
        s += "Probability Table: " + "\n"
        s += "-------------------------------"
        for table_entry in self.table.table_dict.keys():
            s += "P(" + self.name + "= True |  " + str(table_entry) + ")= " + str(self.table.table_dict.get(table_entry)) + "\n"
            s += "P(" + self.name + "= False |  " + str(table_entry) + ")= " + str(1 - self.table.table_dict.get(table_entry)) + "\n"
        s += "-------------------------------\n"
        return s


        s += str(self.table)

        return s
