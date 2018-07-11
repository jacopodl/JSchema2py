class ConstraintError(Exception):
    pass


class Constraint:
    def __init__(self, tp, schema=None):
        self.type = tp

    def check_type(self, value):
        if type(self.type) == list or type(self.type) == tuple:
            for tp in value:
                if type(value) == tp:
                    return True
            raise TypeError("required one of %s, given %s" % (self.type, type(value)))
        if type(value) != self.type:
            raise TypeError("required %s, given %s" % (self.type, type(value)))

    def check_constraint(self, lvalue, rvalue):
        return True
