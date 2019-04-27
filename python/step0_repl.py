#!/usr/local/bin/python3

import sys

def READ(arg):
    return arg

def EVAL(arg):
    return arg

def PRINT(arg):
    return arg

def rep(arg):
    return PRINT(EVAL(READ(arg)))

while True:
    try:
        print(rep(input("user> ")))
    except (EOFError, KeyboardInterrupt):
        sys.exit(1)
