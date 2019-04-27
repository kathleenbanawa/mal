#!/usr/local/bin/python3
from mal_types import *

def pr_str(ast, print_readably=False):
    if isinstance(ast, int):
        return str(ast)
    elif isinstance(ast, str):
        return ast
    elif isinstance(ast, MalNil):
        return str(ast)
    elif isinstance(ast, MalTrue):
        return str(ast)
    elif isinstance(ast, MalFalse):
        return str(ast)
    elif isinstance(ast, MalSymbol):
        return str(ast)
    elif isinstance(ast, list):
        result = []
        for e in ast:
            result.append(pr_str(e))
        return "(" + " ".join(result) + ")"
    elif isinstance(ast, MalVector):
        result = []
        for e in ast.elements:
            result.append(pr_str(e))
        return "[" + " ".join(result) + "]"
