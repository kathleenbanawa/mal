from mal_types import *

class MalKeyException(Exception):
    pass

class MalEOFException(Exception):
    pass

class MalIndexOutOfBoundsException(Exception):
    pass

class MalThrowException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        s = self.value
        if isinstance(self.value, MalString):
            s = self.value.string
        return s
