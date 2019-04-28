#!/usr/local/bin/python3
import sys
import reader
import printer
from mal_types import *
from mal_errors import *
from env import *

def READ(s):
    return reader.read_str(s)

def eval_ast(ast, env):
    if isinstance(ast, MalSymbol):
        v = env.get(ast.name)
        if v:
            return v
        else:
            print(ast.name, "not found.")
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
            first = ast[0]
            if isinstance(first, MalSymbol) and first.name in ["def!", "let*"]:
                if first.name == "def!":
                    return env.set(ast[1].name, EVAL(ast[2], env))
                elif first.name == "let*":
                    let_env = Env(env)
                    second = ast[1]
                    if isinstance(second, list):
                        for a, b in zip(second[::2], second[1::2]):
                            let_env.set(a.name, EVAL(b, let_env))
                    elif isinstance(second, MalVector):
                        for a, b in zip(second.elements[::2], second.elements[1::2]):
                            let_env.set(a.name, EVAL(b, let_env))
                    return EVAL(ast[2], let_env)
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
    return PRINT(EVAL(READ(s), repl_env))
    
repl_env = Env()
repl_env.set('+', (lambda a,b: a+b))
repl_env.set('-', (lambda a,b: a-b))
repl_env.set('*', (lambda a,b: a*b))
repl_env.set('/', (lambda a,b: int(a/b)))

while True:
    try:
        i = input("user> ")
        print(rep(i))
    except (EOFError, KeyboardInterrupt):
        sys.exit(1)
    except MalKeyException:
        pass
