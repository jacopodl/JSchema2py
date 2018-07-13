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
    return __build_class(RefNavigator(schema, base_path), schema, {})


def __build_class(refn, schema, namespace):
    if "$ref" in schema:
        schema = refn.navigate(schema["$ref"])
        refn = RefNavigator(schema, refn.basepath)
    elif "anyOf" in schema or "oneOf" in schema:
        objs = schema["oneOf"] if "oneOf" in schema else schema["anyOf"]
        objs = [__build_class(refn, clazz, namespace) for clazz in objs]
        namespace.update({itm.__name__: itm for itm in objs if itm.__name__ not in namespace})
        return objs
    elif "title" not in schema:
        raise AttributeError("missing title or $ref or anyOf or oneOf keywords")
    if schema["title"] not in namespace:
        properties = __extract_properties(refn, schema["properties"], namespace)
        namespace[schema["title"]] = JSPYMeta(schema["title"], (), {}, properties, schema)
    return namespace[schema["title"]]


def __build_json_obj(refn, current, namespace):
    obj = __build_class(refn, current, namespace)
    if isinstance(obj, (list, tuple)):
        return ConstraintFactory.get_constraint("variant", obj)
    return ConstraintFactory.get_constraint("generic", obj)


def __extract_properties(refn, current, namespace):
    properties = {}
    for prop, value in current.items():
        tp = value["type"]
        if tp == "object":
            prp = __build_json_obj(refn, value, namespace)
            properties[prop] = prp
        elif tp == "array":
            items = value["items"]
            if isinstance(items, dict):
                if items["type"] == "object":
                    prp = __build_json_obj(refn, items, namespace)
                    properties[prop] = ConstraintFactory.get_constraint(tp, value, prp.constraint, [])
                    continue
                constraint = ConstraintFactory.CONSTRAINTS[items["type"]](items)
                properties[prop] = ConstraintFactory.get_constraint(tp, value, constraint)
            else:
                raise RuntimeError()
        else:
            properties[prop] = ConstraintFactory.get_constraint(tp, value)
    return properties
