class JSPYMeta(type):
    def __init__(cls, name, bases, dct, props=None, cinfo=None):
        type.__init__(cls, name, bases, dct)

    def __new__(mcs, name, bases, dct, props=None, cinfo=None):
        dct["__jprop__"] = props
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
