from mal_types import *

class Env:
    def __init__(self, outer=None, binds=None, exprs=None):
        self.outer = outer
        self.data = {}
        if binds:
            if isinstance(binds, MalVector):
                binds = binds.elements
            if not isinstance(exprs, list) and not isinstance(exprs, tuple):
                exprs = [exprs]
            for i in range(0, len(binds)):
                if binds[i].name == "&":
                    assert(binds[i] != binds[-1] and binds[i+1])
                    name = binds[i+1].name
                    self.data[name] = list(exprs[i:])
                    break
                else:
                    self.data[binds[i].name] = exprs[i] if exprs else None
    def __str__(self):
        return str(self.data)
    def set(self, k, v):
        self.data[k] = v
        return v
    def find(self, k):
        if k in self.data:
            return self.data[k]
        if self.outer:
            return self.outer.find(k)
        return None
    def get(self, k):
        return self.find(k)
