#!/usr/local/bin/python3
import sys
import reader
import printer
import core
from mal_types import *
from mal_errors import *
from env import *
import inspect

def READ(s):
    return reader.read_str(s)

def eval_ast(ast, env):
    if isinstance(ast, MalSymbol):
        v = env.get(ast.name)
        if v is not None:
            return v
        else:
            #print(ast.name, "not found.")
            raise(MalKeyException(f"'{ast.name}' not found"))
    elif isinstance(ast, list):
        return [EVAL(e, env) for e in ast]
    elif isinstance(ast, MalVector):
        rn = MalVector()
        for e in ast.elements:
            rn.elements.append(EVAL(e, env))
        return rn
    elif isinstance(ast, str):
        raise(MalKeyException())
    else:
        return ast

def EVAL(input_ast, env):
    def is_macro_call(ast, env):
        if isinstance(ast, list) and len(ast) > 0:
            first = ast[0]
            if isinstance(first, MalSymbol):
                fn = env.get(first.name)
                if fn is not None and isinstance(fn, MalFunction) and fn.is_macro:
                    return True
        return False
    def macroexpand(input_ast, env):
        ast = input_ast
        while is_macro_call(ast, env):
            first = ast[0]
            fn = env.get(first.name)
            ast = fn.fn(ast[1:])
        return ast

    while True:
        ast = macroexpand(input_ast, env)
        if isinstance(ast, list):
            if len(ast) == 0:
                return ast
            else:
                first = ast[0]
                symbols = ["def!", "defmacro!", "let*", "do", "if", "fn*", "quote", "quasiquote", "macroexpand", "try*"]
                if isinstance(first, MalSymbol) and first.name in symbols:
                    if first.name == "def!":
                        return env.set(ast[1].name, EVAL(ast[2], env))
                    elif first.name == "defmacro!":
                        fn = EVAL(ast[2], env)
                        fn.is_macro = True
                        return env.set(ast[1].name, fn)
                    elif first.name == "let*":
                        let_env = Env(env)
                        second = ast[1]
                        if isinstance(second, list):
                            for a, b in zip(second[::2], second[1::2]):
                                let_env.set(a.name, EVAL(b, let_env))
                        elif isinstance(second, MalVector):
                            for a, b in zip(second.elements[::2], second.elements[1::2]):
                                let_env.set(a.name, EVAL(b, let_env))
                        env = let_env
                        input_ast = ast[2]
                    elif first.name == "do":
                        rest = [ast[1]] if len(ast) == 2 else ast[1:-1]
                        eval_ast(rest, env)
                        input_ast = ast[-1]
                    elif first.name == "if":
                        eval_first = EVAL(ast[1], env)
                        if not isinstance(eval_first, MalFalse) and not isinstance(eval_first, MalNil):
                            input_ast = ast[2]
                        else:
                            if len(ast) > 3:
                                input_ast = ast[3]
                            else:
                                return MalNil()
                    elif first.name == "fn*":
                        return MalFunction(ast[2], ast[1], env, (lambda *args: EVAL(ast[2], Env(env, ast[1], *args))))
                    elif first.name == "quote":
                        return ast[1]
                    elif first.name == "quasiquote":
                        def is_pair(x):
                            return isinstance(x, list) and len(x) > 0
                        def quasiquote(ast):
                            if not is_pair(ast):
                                return [MalSymbol("quote"), ast]
                            elif isinstance(ast[0], MalSymbol) and ast[0].name == "unquote":
                                return ast[1]
                            elif is_pair(ast[0]) and isinstance(ast[0], list) and isinstance(ast[0][0], MalSymbol) and ast[0][0].name == "splice-unquote":
                                return [MalSymbol("concat"), ast[0][1], quasiquote(ast[1:])]
                            else:
                                return [MalSymbol("cons"), quasiquote(ast[0]), quasiquote(ast[1:])]
                        param = ast[1].elements if isinstance(ast[1], MalVector) else ast[1]
                        input_ast = quasiquote(param)
                    elif first.name == "macroexpand":
                        return macroexpand(ast[1], env)
                    elif first.name == "try*":
                        result = None
                        try:
                            input_ast = EVAL(ast[1], env)
                        except Exception as e:
                            exception_env = Env(env, [ast[2][1]], [str(e)])
                            input_ast = ast[2][2]
                            env = exception_env
                else:
                    rn = eval_ast(ast, env)
                    if isinstance(rn[0], MalFunction):
                        f = rn[0]
                        input_ast = f.ast
                        env = Env(f.env, f.params, rn[1:])
                    elif inspect.isfunction(rn[0]):
                        return rn[0](*rn[1:])
                    else:
                        raise(Exception("Unexpected type"))
        else:
            return eval_ast(ast, env)

def PRINT(exp):
    return printer.pr_str(exp, True)

def rep(s):
    return PRINT(EVAL(READ(s), repl_env))
    
repl_env = Env()
for a, b in core.ns.items():
    repl_env.set(a, b)

repl_env.set("eval", (lambda ast: EVAL(ast, repl_env)))

EVAL(READ("(def! not (fn* (a) (if a false true)))"), repl_env)
EVAL(READ("(def! load-file (fn* (f) (eval (read-string (str \"(do \" (slurp f) \")\")))))"), repl_env)
EVAL(READ("(defmacro! cond (fn* (& xs) (if (> (count xs) 0) (list 'if (first xs) (if (> (count xs) 1) (nth xs 1) (throw \"odd number of forms to cond\")) (cons 'cond (rest (rest xs)))))))"), repl_env)

while True:
    try:
        i = input("user> ")
        print(rep(i))
    except (EOFError, KeyboardInterrupt):
        sys.exit(1)
    except MalKeyException:
        pass
    except RecursionError:
        pass
    except MalThrowException as e:
        print("Error: " + str(e))
