from jschema2py.constraints.constraint import Constraint


class BooleanConstraint(Constraint):
    def __init__(self, schema=None):
        Constraint.__init__(self, bool)
