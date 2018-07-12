from jschema2py.constraints.constraint import Constraint


class VariantConstraint(Constraint):
    def check_type(self, value):
        for tp in self.type:
            if type(value) == tp:
                return True
        raise TypeError("required %s, given %s" % (self.type, type(value)))
