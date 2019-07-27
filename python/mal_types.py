#!/usr/local/bin/python3

class MalType:
    pass

class MalList:
    pass

class MalSymbol:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name

class MalString:
    def __init__(self, string):
        self.string = string

class MalVector:
    def __init__(self):
        self.elements = []

class MalHashMap:
    def __init__(self):
        self.elements = []

class MalNil:
    def __str__(self):
        return "nil"

class MalTrue:
    def __str__(self):
        return "true"

class MalFalse:
    def __str__(self):
        return "false"

class MalFunction:
    def __init__(self, ast, params, env, fn, is_macro=False):
        self.ast = ast
        self.params = params
        self.env = env
        self.fn = fn
        self.is_macro = is_macro

class MalAtom:
    def __init__(self, value):
        self.value = value
