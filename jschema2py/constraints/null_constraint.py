from jschema2py.constraints.constraint import Constraint


class NullConstraint(Constraint):
    def __init__(self, schema=None):
        Constraint.__init__(self, None)

    def check_type(self, value):
        if value != self.type:
            raise TypeError("required %s, given %s" % (self.type, type(value)))
        return True
