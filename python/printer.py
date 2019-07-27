#!/usr/local/bin/python3
from mal_types import *

def pr_str(ast, print_readably=False):
    if isinstance(ast, int):
        return str(ast)
    elif isinstance(ast, str):
        if print_readably:
            rn = ast.split("\n")
            rn = ["\\n" if e == '' else e for e in rn]
            rn = ''.join(rn)
            return "\"" + rn + "\""
        return ast
    elif isinstance(ast, MalNil):
        return str(ast)
    elif isinstance(ast, MalTrue):
        return str(ast)
    elif isinstance(ast, MalFalse):
        return str(ast)
    elif isinstance(ast, MalSymbol):
        return str(ast)
    elif isinstance(ast, MalString):
        if print_readably:
            return "\"" + ast.string + "\""
        return ast.string
    elif isinstance(ast, list):
        result = []
        for e in ast:
            result.append(pr_str(e, print_readably))
        return "(" + " ".join(result) + ")"
    elif isinstance(ast, MalVector):
        result = []
        for e in ast.elements:
            result.append(pr_str(e, print_readably))
        return "[" + " ".join(result) + "]"
    elif isinstance(ast, tuple):
        if len(ast) == 1 and isinstance(ast[0], MalSymbol):
            return ast[0].name
        else:
            assert(len(ast) == 3 and isinstance(ast[0], MalString) and isinstance(ast[1], str) and isinstance(ast[2], MalString))
            return ast[0].string + ast[1] + ast[2].string
        raise(Exception("Invalid tuple"%ast))
    elif isinstance(ast, MalAtom):
        return "(atom " + str(ast.value) + ")"
    else:
        print(ast)
