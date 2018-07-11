from jschema2py.constraints.numeric_constraint import NumericConstraint


class NumberConstraint(NumericConstraint):
    def __init__(self, schema=None):
        NumericConstraint.__init__(self, float, schema)

    def check_type(self, value):
        if type(value) == int:
            value = float(value)
        NumericConstraint.check_type(self, value)
