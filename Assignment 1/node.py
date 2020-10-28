class Node (object) :
    def __init__(self,name,number_of_people):
        self.name = name
        self.number_of_people = number_of_people

    def __str__(self):
        print((self.name,self.number_of_people));