__author__ = 'Dave and Alex'

from lexer import *
from nodes import *
import sys
import math

# Parser for reserved words
def reserved(var):
    return Reserved(var, RESERVED)

var_name = Tag(VAR)
number = Process(Tag(INT), (lambda i: int(i)))
floatnum = Process(Tag(FLOAT), (lambda f: float(f)))

# calls parser with position 0, and the tokens as a parameter, returns the AST
def parse(tokens):
    tree = parser()(tokens, 0)
    return tree

# before calling parse, validates the expressions from the grammar
def parser():
    return Validator(list_expressions())

# separates the expressions with the reserved ;
def list_expressions():
    separator = reserved(';') ^ (lambda x: lambda l, r: Statement(l, r))
    return Exp(statement(), separator)

#evaluates all of the possibles statmeents
def statement():
    return parse_assign() | parse_call() | parse_if() | parse_while() | parse_function() | parse_call() | parse_for() | parse_print()

#gets the name of the variable and the operation
def parse_assign():
    def process(parsed):
        ((name, _), exp) = parsed
        return Assign(name, exp)
    return var_name + reserved('=') + aexp() ^ process

# gets the condition, the true operation, and the false operation (optional)
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

# gets the condition, and the body of expressions
def parse_while():
    def process(parsed):
        ((((_, condition), _), body), _) = parsed
        return WhileExp(condition, body)
    return reserved('while') + bexp() + reserved(':') + Recursive(list_expressions) + reserved('end') ^ process

# gets the name of the function, and the expresion that it calls
def parse_function():
    def process(parsed):
        ((((_, name), _), exp), _) = parsed
        return FuncExp(name, exp)
    return reserved('function') + var_name + reserved(':') + Recursive(list_expressions) + reserved('end') ^ process

# calls the function, with the defined name
def parse_call():
    def process(parsed):
        (_, name) = parsed
        return CallExp(name)
    return reserved('call') + var_name ^ process

# gets the first number, second number (stop), and the expressions
def parse_for():
    def process(parsed):
        ((((((_, first) ,_),second),_), exp), _) = parsed
        return ForExp(first, second, exp)
    return reserved('for') + floatnum + reserved('to') + floatnum + reserved(':') + Recursive(list_expressions) + reserved('end') ^ process

# gets the variable that will print
def parse_print():
    def process(parsed):
        (_, var) = parsed
        return PrintExp(var)
    return reserved('show') + var_name ^ process

# evaluates all of the possible boolean comparations
def bexp():
    return bool_exp()

# evaluates the operators that applies to boolean expressions
def bool_exp():
    operators = ['<', '<=', '>', '>=', 'equal', 'not equal']
    return aexp() + op_reducer(operators) + aexp() ^ process_bool

# apply operators precedence to the expressions
def aexp():
    return apply_precedence(assign_exp(), precedence_levels, process_operation)

# assigns the value, or gets the expression between parentheses
def assign_exp():
    #print "Assign Exp -> CALLED"
    return assign_value() | exp_parentheses()

# gets the expression between parentheses
def exp_parentheses():
    #print "Exp Parentheses -> CALLED"
    return reserved('(') + Recursive(aexp) + reserved(')') ^ process_parentheses

# assigns value
def assign_value():
    #print "Assign Value -> Called"
    # Using Compare node, tries to get number, if it's not an integer, it evaluates the variable, or float number
    return (number ^ (lambda i: IntExp(i))) | (var_name ^ (lambda v: VarExp(v))) | (floatnum ^ (lambda f: IntExp(f)))

# applies precedence, to the expression, with the levels defined below, and processing them with the function of the parser
def apply_precedence(value_parser, precedence_levels, combine):
    #print "Apply_Precedence -> CALLED"
    def operation_parse(p_level):
        return op_reducer(p_level) ^ combine
    parser = value_parser * operation_parse(precedence_levels[0])
    for precedence_level in precedence_levels[1:]:
        parser = parser * operation_parse(precedence_level)
    return parser

# process an arithmetic operation
def process_operation(operation):
    #print "Process Operation -> CALLED"
    return lambda left, right: Operation(operation, left, right)

# process a bollean operation
def process_bool(sentence):
    #print "Process_bool CALLED"
    ((left, operation), right) = sentence
    return RelExp(operation, left, right)

# process parentheses, and gets the sentence between them
def process_parentheses(sentence):
    #print "Process Parentheses -> CALLED"
    ((_, p), _) = sentence
    return p

# reduces the tree to get the values of the nodes
def op_reducer(operations):
    #print "Op Reducer -> CALLED"
    oper_parse = [reserved(operation) for operation in operations]
    reduced = reduce(lambda left, right: left | right, oper_parse)  # do operations from tree parsing grammar
    return reduced

# levels of precedence
precedence_levels = [
    ['^'],
    ['*', '/', '%'],
    ['+', '-'],
]

