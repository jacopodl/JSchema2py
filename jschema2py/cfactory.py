from jschema2py.constraints import *
from jschema2py.property import Property


class ConstraintFactory:
    CONSTRAINTS = {
        "generic": Constraint,
        "boolean": BooleanConstraint,
        "integer": IntegerConstraint,
        "null": NullConstraint,
        "number": NumberConstraint,
        "string": StringConstraint,
        "variant": VariantConstraint
    }

    @staticmethod
    def get_constraint(ctype, data, value=None):
        if ctype not in ConstraintFactory.CONSTRAINTS:
            raise RuntimeError("ConstraintError")

        prop = Property(ConstraintFactory.CONSTRAINTS[ctype](data), value)
        if isinstance(data, dict) and "default" in data:
            prop.validate(None, data["default"])
            prop.value = data["default"]
        return prop
