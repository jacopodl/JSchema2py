import json
from os.path import dirname

from jschema2py.cfactory import ConstraintFactory
from jschema2py.jspymeta import JSPYMeta
from jschema2py.refnavigator import RefNavigator


def from_file(path):
    with open(path, "r") as file:
        schema = json.loads(file.read())
    return build_class(schema, dirname(path))


def build_class(schema, base_path=None):
    if isinstance(schema, str):
        schema = json.loads(schema)
    if not isinstance(schema, dict):
        raise TypeError("build_class require str or dict")
    return __build_class(RefNavigator(schema, base_path), schema, {}, {})


def __build_class(refn, schema, properties, namespace):
    if "title" in schema:
        properties, namespace = __extract_properties(refn, schema["properties"], properties, namespace)
    elif "$ref" in schema:
        pass
    elif "anyOf" in schema or "oneOf" in schema:
        pass
    else:
        raise AttributeError("missing title or $ref or anyOf or oneOf keywords")
    return JSPYMeta(schema["title"], (), {}, properties)


def __extract_properties(refn, current, properties, namespace):
    for prop, value in current.items():
        tp = value["type"]
        if tp == "object":
            pass
        elif tp == "array":
            pass
        else:
            properties[prop] = ConstraintFactory.get_constraint(tp, value)
    return properties, namespace
