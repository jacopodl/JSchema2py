from jschema2py.constraints import *
from jschema2py.property import Property


class ConstraintFactory:
    CONSTRAINTS = {
        "array": ArrayConstraint,
        "boolean": BooleanConstraint,
        "generic": Constraint,
        "integer": IntegerConstraint,
        "null": NullConstraint,
        "number": NumberConstraint,
        "string": StringConstraint,
        "variant": VariantConstraint
    }

    @staticmethod
    def get_constraint(ctype, data, const=None, value=None):
        if ctype not in ConstraintFactory.CONSTRAINTS:
            raise RuntimeError("ConstraintError")

        cns = ConstraintFactory.CONSTRAINTS[ctype]

        if const is not None:
            prop = cns(data, const)
        else:
            prop = cns(data)

        prop = Property(prop, value)
        if isinstance(data, dict) and "default" in data:
            prop.validate(None, data["default"])
            prop.value = data["default"]
        return prop
