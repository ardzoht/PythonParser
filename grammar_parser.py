__author__ = 'Dave and Alex'

from lexer import *
from nodes import *
import sys


# Parser for reserved words
def reserved(var):
    return Reserved(var, RESERVED)

var_name = Tag(VAR)
number = Process(Tag(INT), (lambda i: int(i)))

def parse(tokens):
    tree = parser()(tokens, 0)
    return tree

def parser():
    return Validator(list_expressions())

def list_expressions():
    separator = reserved(';') ^ (lambda x: lambda l, r: Statement(l, r))
    return Exp(statement(), separator)

def statement():
    return parse_assign() | parse_call() | parse_if() | parse_while() | parse_function() | parse_call() | parse_for()

def parse_assign():
    def process(parsed):
        ((name, _), exp) = parsed
        return Assign(name, exp)
    return var_name + reserved('=') + aexp() ^ process

def parse_if():
    def process(parsed):
        (((((_, condition), _), true_stmt), false_parsed), _) = parsed
        if false_parsed:
            (_, f_stmt) = false_parsed
        else:
            f_stmt = None
        return IfExp(condition, true_stmt, f_stmt)
    return reserved('if') + bexp() + reserved(':') + Recursive(list_expressions) + \
           Opt(reserved('else:') + Recursive(list_expressions)) + reserved('end') ^ process

def parse_while():
    def process(parsed):
        ((((_, condition), _), body), _) = parsed
        return WhileExp(condition, body)
    return reserved('while') + bexp() + reserved(':') + Recursive(list_expressions) + reserved('end') ^ process

def parse_function():
    def process(parsed):
        ((((_, name), _), exp), _) = parsed
        return FuncExp(name, exp)
    return reserved('def') + var_name + reserved(':') + Recursive(list_expressions) + reserved('end') ^ process

def parse_call():
    def process(parsed):
        (_, name) = parsed
        return CallExp(name)
    return reserved('call') + var_name ^ process

def parse_for():
    def process(parsed):
        print parsed
        ((((((_, first) ,_),second),_), exp), _) = parsed
        return ForExp(first, second, exp)
    return reserved('for') + number + reserved('to') + number + reserved(':') + Recursive(list_expressions) + reserved('end') ^ process


def bexp():
    return bool_exp()

def bool_exp():
    operators = ['<', '<=', '>', '>=', '=', '!=']
    return aexp() + op_reducer(operators) + aexp() ^ process_bool

def aexp():
    return apply_precedence(assign_exp(), precedence_levels, process_operation)

def assign_exp():
    #print "Assign Exp -> CALLED"
    return assign_value() | exp_parentheses()

def exp_parentheses():
    #print "Exp Parentheses -> CALLED"
    return reserved('(') + Recursive(aexp) + reserved(')') ^ process_parentheses

def assign_value():
    #print "Assign Value -> Called"
    # Using Compare node, tries to get number, if it's not an integer, it evaluates the variable
    return (number ^ (lambda i: IntExp(i))) | (var_name ^ (lambda v: VarExp(v)))

def apply_precedence(value_parser, precedence_levels, combine):
    #print "Apply_Precedence -> CALLED"
    def operation_parse(p_level):
        return op_reducer(p_level) ^ combine
    parser = value_parser * operation_parse(precedence_levels[0])
    for precedence_level in precedence_levels[1:]:
        parser = parser * operation_parse(precedence_level)
    return parser

def process_operation(operation):
    #print "Process Operation -> CALLED"
    return lambda left, right: Operation(operation, left, right)

def process_bool(sentence):
    #print "Process_bool CALLED"
    ((left, operation), right) = sentence
    return RelExp(operation, left, right)

def process_parentheses(sentence):
    #print "Process Parentheses -> CALLED"
    ((_, p), _) = sentence
    return p

def op_reducer(operations):
    #print "Op Reducer -> CALLED"
    oper_parse = [reserved(operation) for operation in operations]
    reduced = reduce(lambda left, right: left | right, oper_parse)  # do operations from tree parsing grammar
    return reduced

precedence_levels = [
    ['^'],
    ['*', '/', '%'],
    ['+', '-'],
]

vars = ['a', 'b', 'c', 'd']
index_vars = []

if __name__ == '__main__':
    filename = sys.argv[1]
    file = open(filename)
    characters = file.read()
    file.close()
    tokens = do_lex(characters)
    parser = globals()[sys.argv[2]]()
    result = parser(tokens, 0)
    print result