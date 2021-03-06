from mal_types import *
from mal_errors import *
import printer
import reader
import inspect

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
    if isinstance(args[0], MalString) and isinstance(args[1], str):
        return MalTrue() if args[0].string == args[1] else MalFalse()
    if type(args[0]) != type(args[1]):
        return MalFalse()
    if type(args[0]) in [MalFalse, MalTrue, MalNil]:
        return MalTrue()
    if isinstance(args[0], list):
        if len(args[0]) != len(args[1]):
            return MalFalse()
    if type(args[0]) == MalSymbol:
        return MalTrue() if args[0].name == args[1].name else MalFalse()
    return MalTrue() if args[0] == args[1] else MalFalse()

def prn(*args):
    assert(args)
    result = []
    for e in args:
        result.append(printer.pr_str(e, True))
    print(" ".join(result))
    return MalNil()

def println(*args):
    print(" ".join([printer.pr_str(e, False) for e in args]))
    return MalNil()

def slurp(arg):
    with open(arg.string, "r") as fp:
        text = fp.read()
    return text

def mal_str(*args):
    return printer.pr_str(args)

def read_str(arg):
    if isinstance(arg, MalString):
        return reader.read_str(arg.string)
    elif isinstance(arg, str):
        return reader.read_str(arg)
    else:
        raise(Exception("Unexpected type:"%type(arg)))

def reset_atom(*args):
    assert(len(args) == 2)
    args[0].value = args[1]
    return args[1]

def swap_atom(*args):
    assert(isinstance(args[0], MalAtom))
    atom = args[0]
    params = [atom.value]
    if len(args) > 2:
        params.extend(args[2:])
    if isinstance(args[1], MalFunction):
        atom.value = args[1].fn(*params)
    elif inspect.isfunction(args[1]):
        atom.value = args[1](*params)
    else:
        raise(Exception("Unexpected type:"%type(args[1])))
    return atom.value

def concat(*args):
    rt = []
    for e in args:
        if isinstance(e, list):
            rt.extend(e)
        elif isinstance(e, MalVector):
            rt.extend(e.elements)
        else:
            raise(Exception("Unexpected type:"%type(e)))
    return rt

def cons(*args):
    if isinstance(args, tuple):
        if isinstance(args[1], MalVector):
            rt = [args[0]]
            for e in args[1].elements:
                rt.append(e)
            return rt
    return [args[0]] + args[1]

def nth(*args):
    assert(args and len(args) == 2)
    assert(isinstance(args[1], int))
    input_list = args[0]
    index = args[1]
    if isinstance(args[0], MalVector):
        input_list = args[0].elements
    if index >= len(input_list):
        raise(MalIndexOutOfBoundsException("Out of bounds"))
    return input_list[index]

def first(arg):
    if arg is None or isinstance(arg, MalNil):
        return MalNil()
    input_list = arg
    if isinstance(arg, MalVector):
        input_list = arg.elements
    if len(input_list) == 0:
        return MalNil()
    return input_list[0]

def rest(arg):
    if arg is None or isinstance(arg, MalNil):
        return []
    input_list = arg
    if isinstance(arg, MalVector):
        input_list = arg.elements
    return input_list[1:]

def throw(arg):
    raise(MalThrowException(arg))

def mal_map(*args):
    rt = []
    fn = args[0].fn if isinstance(args[0], MalFunction) else args[0]
    input_list = args[1].elements if isinstance(args[1], MalVector) else args[1]
    for e in input_list:
        rt.append(fn(e))
    return rt

def mal_apply(*args):
    fn = args[0].fn if isinstance(args[0], MalFunction) else args[0]
    rest = []
    for e in args[1:]:
        if isinstance(e, list):
            rest.extend(e)
        elif isinstance(e, MalVector):
            rest.extend(e.elements)
        else:
            rest.append(e)
    if isinstance(args[0], MalFunction):
        return fn(rest)
    return fn(*rest)

def readline(arg):
    pass

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
      'prn': (lambda *args: prn(*args)),
      'println': (lambda *args: println(*args)),
      'read-string': (lambda arg: read_str(arg)),
      'slurp': (lambda arg: slurp(arg)),
      'str': (lambda *args: mal_str(*args)),
      'atom': (lambda arg: MalAtom(arg)),
      'atom?': (lambda arg: MalTrue() if isinstance(arg, MalAtom) else MalFalse()),
      'deref': (lambda arg: arg.value),
      'reset!': (lambda *args: reset_atom(*args)),
      'swap!': (lambda *args: swap_atom(*args)),
      'cons': (lambda *args: cons(*args)),
      'concat': (lambda *args: concat(*args)),
      'nth': (lambda *args: nth(*args)),
      'first': (lambda arg: first(arg)),
      'rest': (lambda arg: rest(arg)),
      'throw': (lambda arg: throw(arg)),
      'map': (lambda *args: mal_map(*args)),
      'apply': (lambda *args: mal_apply(*args)),
      'nil?': (lambda arg: MalTrue() if isinstance(arg, MalNil) else MalFalse()),
      'true?': (lambda arg: MalTrue() if isinstance(arg, MalTrue) else MalFalse()),
      'false?': (lambda arg: MalTrue() if isinstance(arg, MalFalse) else MalFalse()),
      'symbol?': (lambda arg: MalTrue() if isinstance(arg, MalSymbol) else MalFalse()),
      'readline': (lambda arg: readline(arg))
}
