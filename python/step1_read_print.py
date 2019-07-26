#!/usr/local/bin/python3
import sys
import reader
import printer
from mal_errors import *

def READ(s):
    return reader.read_str(s)

def EVAL(ast, env):
    return ast

def PRINT(exp):
    return printer.pr_str(exp, True)

def rep(s):
    return PRINT(EVAL(READ(s), ""))

while True:
    try:
        i = input("user> ")
        print(rep(i))
    except (EOFError, KeyboardInterrupt):
        sys.exit(1)
    except MalEOFException:
        print("EOF")
