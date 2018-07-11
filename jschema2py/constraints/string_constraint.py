import re

from jschema2py.constraints.constraint import Constraint, ConstraintError


class StringConstraint(Constraint):
    def __init__(self, schema):
        Constraint.__init__(self, str)
        self.regex = re.compile(schema["pattern"] if "pattern" in schema else "")
        self.enum = schema["enum"] if "enum" in schema else []

    def check_constraint(self, lvalue, rvalue):
        if self.regex.match(rvalue) is None:
            raise ConstraintError("%s doesn't match pattern: %s" % (rvalue, self.regex.pattern))
        if self.enum:
            for itm in self.enum:
                if itm == rvalue:
                    return True
            raise ConstraintError("%s doesn't match enum: %s" % (rvalue, self.enum))
        return True
