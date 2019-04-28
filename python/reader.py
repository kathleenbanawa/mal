#!/usr/local/bin/python3
import re
import sys
from mal_types import *
from mal_errors import *

class Reader:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
    def next(self):
        current_position = self.position
        self.position += 1
        if self.position >= len(self.tokens):
            raise(MalEOFException())
        return self.tokens[current_position]
    def peek(self):
        return self.tokens[self.position]

def read_atom(reader):
    token = reader.peek()
    if token.lstrip('-').isdigit():
        return int(token)
    else:
        if token == 'nil':
            return MalNil()
        elif token == 'true':
            return MalTrue()
        elif token == 'false':
            return MalFalse()
        else:
            return MalSymbol(token)

def read_list(reader):
    rn = []
    while True:
        form = read_form(reader)
        if isinstance(form, MalSymbol) and form.name == ')':
            break
        else:
            rn.append(form)
    return rn

def read_vector(reader):
    rn = MalVector()
    while True:
        form = read_form(reader)
        if isinstance(form, MalSymbol) and form.name == ']':
            break
        else:
            rn.elements.append(form)
    return rn

def read_form(reader):
    rn = None
    if reader.peek() == '':
        raise(MalEOFException())
    if reader.peek() == '(':
        reader.next()
        rn = read_list(reader)
    elif reader.peek() == '[':
        reader.next()
        rn = read_vector(reader)
    else:
        rn = read_atom(reader)
        reader.next()
    return rn

def tokenize(s):
    pattern = """[\s,]*(~@|[\[\]{}()'`~^@]|"(?:\\.|[^\\"])*"?|;.*|[^\s\[\]{}('"`,;)]*)"""
    m = re.findall(pattern, s)
    #print("tokens:", m)
    return m

def read_str(s):
    return read_form(Reader(tokenize(s)))
