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
        return pr_str(ast.string, print_readably)
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
    elif isinstance(ast, MalHashMap):
        result = []
        for e in ast.elements:
            result.append(pr_str(e, print_readably) + " " + pr_str(ast.elements[e], print_readably))
        return "{" + " ".join(result) + "}"
    elif isinstance(ast, tuple):
        if len(ast) == 0:
            return ""
        elif len(ast) == 1:
            if isinstance(ast[0], MalSymbol):
                return ast[0].name
            elif isinstance(ast[0], MalString):
                return ast[0].string
        return " ".join([pr_str(e, print_readably) for e in ast])
    elif isinstance(ast, MalAtom):
        return "(atom " + str(ast.value) + ")"
    else:
        print(ast)
