from jschema2py.constraints.constraint import Constraint, ConstraintError


class NumericConstraint(Constraint):
    def __init__(self, tp, schema=None):
        Constraint.__init__(self, tp)
        self.min = schema["minimum"] if "minimum" in schema else None
        self.max = schema["maximum"] if "maximum" in schema else None

    def check_constraint(self, lvalue, rvalue):
        if self.min is not None and self.max is not None:
            if rvalue < self.min or rvalue > self.max:
                raise ConstraintError("value must be between %d and %d" % (self.min, self.max))

        if self.min is not None and rvalue < self.min:
            raise ConstraintError("minimum acceptable value: %d" % self.min)

        if self.max is not None and rvalue > self.max:
            raise ConstraintError("maximum acceptable value: %d" % self.max)
