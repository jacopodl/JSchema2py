from jschema2py.constraints.numeric_constraint import NumericConstraint


class IntegerConstraint(NumericConstraint):
    def __init__(self, schema=None):
        NumericConstraint.__init__(self, int, schema)
