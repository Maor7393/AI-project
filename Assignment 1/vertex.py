class Vertex (object) :
    def __init__(self,name,number_of_people):
        self.name = name
        self.number_of_people = number_of_people

    def __str__(self):
        return "name: "+self.name + "num of people: "+ str(self.number_of_people)