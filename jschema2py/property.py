from jschema2py.constraints import Constraint


class Property:
    __slots__ = ("constraint", "value")

    def __init__(self, constraint, value=None):
        if not isinstance(constraint, Constraint):
            raise TypeError("property constraint requires Constraint object")
        object.__setattr__(self, "constraint", constraint)
        object.__setattr__(self, "value", value)

    def validate(self, lvalue, rvalue):
        self.constraint.check_type(rvalue)
        self.constraint.check_constraint(lvalue, rvalue)
        return True
