from jschema2py.constraints import *
from jschema2py.property import Property


class ConstraintFactory:
    CONSTRAINTS = {
        "boolean": BooleanConstraint,
        "integer": IntegerConstraint,
        "null": NullConstraint,
        "number": NumberConstraint,
        "string": StringConstraint
    }

    @staticmethod
    def get_constraint(ctype, schema):
        if not ctype in ConstraintFactory.CONSTRAINTS:
            raise RuntimeError("ConstraintError")
        prop = Property(ConstraintFactory.CONSTRAINTS[ctype](schema))
        if "default" in schema:
            prop.validate(None, schema["default"])
            prop.value = schema["default"]
        return prop
