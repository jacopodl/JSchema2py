from jschema2py.constraints.constraint import Constraint, ConstraintError


class ArrayConstraint(Constraint):
    def __init__(self, schema, constraint):
        Constraint.__init__(self, list)
        self.maxitems = int(schema["maxItems"]) if "maxItems" in schema else -1
        self.constraint = constraint

    def check_constraint(self, lvalue, rvalue):
        for itm in rvalue:
            self.constraint.check_type(itm)
            self.constraint.check_constraint(None, itm)
        if 0 <= self.maxitems < len(rvalue):
            raise ConstraintError("maxItems imposes a maximum size of %d" % self.maxitems)
