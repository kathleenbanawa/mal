#!/usr/local/bin/python3
import sys
import reader
import printer
from mal_types import *
from mal_errors import *

def READ(s):
    return reader.read_str(s)

def eval_ast(ast, env):
    if isinstance(ast, MalSymbol):
        if ast.name in env:
            return env[ast.name]
        else:
            raise(MalKeyException())
    elif isinstance(ast, list):
        rn = []
        for e in ast:
            rn.append(EVAL(e, env))
        return rn
    elif isinstance(ast, MalVector):
        rn = MalVector()
        for e in ast.elements:
            rn.elements.append(EVAL(e, env))
        return rn
    elif isinstance(ast, str):
        raise(MalKeyException())
    else:
        return ast

def EVAL(ast, env):
    if isinstance(ast, list):
        if len(ast) == 0:
            return ast
        else:
            rn = eval_ast(ast, env)
            f, a, b = rn[0], rn[1], rn[2]
            result = f(a, b)
            return(result)
    else:
        return eval_ast(ast, env)

def PRINT(exp):
    return printer.pr_str(exp)

def rep(s):
    repl_env = {'+': lambda a,b: a+b,
                '-': lambda a,b: a-b,
                '*': lambda a,b: a*b,
                '/': lambda a,b: int(a/b)}
    return PRINT(EVAL(READ(s), repl_env))

while True:
    try:
        i = input("user> ")
        print(rep(i))
    except (EOFError, KeyboardInterrupt):
        sys.exit(1)
    except MalKeyException:
        print("Error")
