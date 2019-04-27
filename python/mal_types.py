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
