__author__ = 'Dave and Alex'

from lexer import *
from nodes import *

lexer = Lexer()

#Parser for reserved words
def reserved(var):
    return Reserved(var, lexer.RESERVED)

var_name = Tag(lexer.VAR)
number = Process(Tag(lexer.VAR), (lambda i: int(i)))

def assign_value():
    #Using Compare node, tries to get number, if it's not an integer, it evaluates the variable
    return (number ^ (lambda i: IntExp(i))) | (var_name ^ (lambda var: VarExp(var)))

def process_parentheses(sentence):
    ((_, p), _) = sentence
    return p

def exp_parentheses():
    return reserved('(') + Recursive(aexp) + reserved(')') ^ process_parentheses

def assign_exp():
    return assign_value() | exp_parentheses()

def process_binary(operation):
    return lambda left, right: BinaryExp(operation, left, right)

def reduce(operations):
    oper_parse = [reserved(operation) for operation in operations]
    reduced = reduce(lambda left, right: left | right, oper_parse) # do operations from tree parsing grammar
    return reduced

precedence_levels = [
    ['*', '/'],
    ['+', '-'],
]

