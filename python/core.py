from mal_types import *
import printer

def lt(*args):
    return MalTrue() if args[0] < args[1] else MalFalse()

def lte(*args):
    return MalTrue() if args[0] <= args[1] else MalFalse()

def gt(*args):
    return MalTrue() if args[0] > args[1] else MalFalse()

def gte(*args):
    return MalTrue() if args[0] >= args[1] else MalFalse()

def eq(*args):
    assert(len(args) == 2)
    if type(args[0]) != type(args[1]):
        return MalFalse()
    if type(args[0]) in [MalFalse, MalTrue, MalNil]:
        return MalTrue()
    if isinstance(args[0], list):
        if len(args[0]) != len(args[1]):
            return MalFalse()
    return MalTrue() if args[0] == args[1] else MalFalse()

def prn(*args):
    assert(args)
    print(printer.pr_str(args[0], True))
    return MalNil()

ns = {'+': (lambda *args: args[0]+args[1]),
      '-': (lambda *args: args[0]-args[1]),
      '*': (lambda *args: args[0]*args[1]),
      '/': (lambda *args: int(args[0]/args[1])),
      '<': (lambda *args: lt(*args)),
      '<=': (lambda *args: lte(*args)),
      '>': (lambda *args: gt(*args)),
      '>=': (lambda *args: gte(*args)),
      '=': (lambda *args: eq(*args)),
      'list?': (lambda a: MalTrue() if isinstance(a, list) else MalFalse()),
      'list': (lambda *a: list(a)),
      'empty?': (lambda a: MalTrue() if len(a) == 0 else MalFalse()),
      'count': (lambda a: len(a) if isinstance(a, list) else 0),
      'prn': (lambda *args: prn(*args))
}
