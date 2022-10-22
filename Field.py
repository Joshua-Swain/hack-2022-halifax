class Field:

    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
        self.points = 0

    def __str__(self):
        return "Field [" + self.name + ": " + str(self.points) + "]"