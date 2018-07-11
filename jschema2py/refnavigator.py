import json
import os.path as osp


def _memoize(fun):
    def dec(self, *args, **kwargs):
        path = args[0]
        if path in self.cache:
            return self.cache[path]
        ret = fun(self, *args, **kwargs)
        if ret is not None:
            self.cache[path] = ret
        return ret

    return dec


class RefNavigator:
    def __init__(self, jdata, basepath=None):
        self.schema = jdata
        self.basepath = basepath and basepath or ''
        self.cache = dict()

    @_memoize
    def navigate(self, path):
        split = path.split("#")
        if len(split) == 1:
            ret = self.loaduri(split[0])
        else:
            data = self.schema
            if split[0] is not '':
                data = self.loaduri(split[0])
            ret = RefNavigator.extractnode(data, split[1])

        return ret

    @_memoize
    def loaduri(self, path):
        if path.find("://") < 0:
            file = path[len("file://"):] if path.startswith("file://") else path
            path = osp.join(self.basepath, file)
            with open(path) as f:
                return json.loads(f.read())
        else:
            raise NotImplementedError("Not implemented yet! Call me in future ;)")

    @staticmethod
    def extractnode(obj, path):
        for itm in path.split('/'):
            if itm is not '':
                obj = obj[itm]
        return obj
