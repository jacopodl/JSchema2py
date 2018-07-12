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
        schema = refn.navigate(schema["$ref"])
        properties, namespace = __extract_properties(RefNavigator(schema), schema["properties"], {}, {})
    elif "anyOf" in schema or "oneOf" in schema:
        objs = schema["oneOf"] if "oneOf" in schema else schema["anyOf"]
        return [__build_class(refn, clazz, {}, {}) for clazz in objs]
    else:
        raise AttributeError("missing title or $ref or anyOf or oneOf keywords")
    return JSPYMeta(schema["title"], (), {}, properties, schema)


def __build_json_obj(refn, current):
    namespace = {}
    obj = __build_class(refn, current, {}, {})
    if isinstance(obj, (list, tuple)):
        prop = ConstraintFactory.get_constraint("variant", obj)
        namespace = {itm.__name__: itm for itm in obj}
    else:
        prop = ConstraintFactory.get_constraint("generic", obj)
        namespace[obj.__name__] = obj
    return prop, namespace


def __extract_properties(refn, current, properties, namespace):
    for prop, value in current.items():
        tp = value["type"]
        if tp == "object":
            prp, ns = __build_json_obj(refn, value)
            properties[prop] = prp
            namespace.update(ns)
        elif tp == "array":
            items = value["items"]
            if isinstance(items, dict):
                if items["type"] == "object":
                    prp, ns = __build_json_obj(refn, items)
                    properties[prop] = ConstraintFactory.get_constraint(tp, value, prp.constraint, [])
                    namespace.update(ns)
                    continue
                constraint = ConstraintFactory.CONSTRAINTS[items["type"]](items)
                properties[prop] = ConstraintFactory.get_constraint(tp, value, constraint)
            else:
                raise RuntimeError()
        else:
            properties[prop] = ConstraintFactory.get_constraint(tp, value)
    return properties, namespace
