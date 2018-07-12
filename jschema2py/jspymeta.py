from jschema2py.constraints import ArrayConstraint


class JSPYMeta(type):
    def __init__(cls, name, bases, dct, props=None, cinfo=None):
        type.__init__(cls, name, bases, dct)

    def __new__(mcs, name, bases, dct, props=None, cinfo=None):
        dct["__jprop__"] = props
        dct["__setattr__"] = _jspy_setattr
        dct["getclass"] = _jspy_getclass
        JSPYMeta.__parse_cinfo(dct, cinfo)
        clazz = type.__new__(mcs, name, bases, dct)
        return clazz

    def __call__(cls, *args, **kwargs):
        props = cls.__dict__["__jprop__"]
        instance = type.__call__(cls, *args, **kwargs)
        for k, v in props.items():
            if v.value is not None:
                object.__setattr__(instance, k, v.value)
        return instance

    @staticmethod
    def __parse_cinfo(dct, cinfo):
        dct["__addprop__"] = False
        if cinfo is not None:
            if "additionalProperties" in cinfo:
                dct["__addprop__"] = cinfo["additionalProperties"]


def _jspy_setattr(cls, key, value):
    dct = object.__getattribute__(cls, "__jprop__")
    if key in dct:
        lvalue = None if key not in cls.__dict__ else cls.__dict__[key]
        if dct[key].validate(lvalue, value):
            object.__setattr__(cls, key, value)
            return
    if not cls.__addprop__:
        raise AttributeError("additional properties not allowed, see JSONSchema")
    object.__setattr__(cls, key, value)


def _jspy_getclass(cls, key):
    dct = object.__getattribute__(cls, "__jprop__")
    if key in dct:
        val = dct[key].constraint
        if isinstance(val, ArrayConstraint):
            return val.constraint.type
        return val.type
    return None
