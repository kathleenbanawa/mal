class Env:
    def __init__(self, outer=None):
        self.outer = outer
        self.data = {}
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
