from Field import Field

class Score:

    def __init__(self):
        self.fields = [
            Field('account_age', 20),
            Field('activity', 30),
            Field('empathy', 50)
        ]

        self.check_for_proper_weights()

    def get_final_result():
        total = 0.0
        for field in self.fields:
            total += (field.weight * field.points)

        return total / 100

    def set_field(self, field_name, points):
        for field in self.fields:
            if field.name == field_name:
                field.points = points

    # Make sure weights all sum to 100
    def check_for_proper_weights(self):
        weight_sum = 0
        for field in self.fields:
            weight_sum += field.weight

        if weight_sum != 100:
            raise Exception('Weights in Score should sum to 100')

    def __str__(self):
        string = "Score ["

        for field in self.fields:
            string += (str(field)) + " "

        string += ("]")
        return string

    def __repr__(self):
        return str(self)
