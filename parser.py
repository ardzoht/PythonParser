__author__ = 'Dave and Alex'

from lexer import *
from nodes import *
import sys


# Parser for reserved words
def reserved(var):
    return Reserved(var, RESERVED)

var_name = Tag(VAR)
number = Process(Tag(INT), (lambda i: int(i)))


def assign_value():
    #print "Assign Value -> Called"
    # Using Compare node, tries to get number, if it's not an integer, it evaluates the variable
    return (number ^ (lambda i: IntExp(i))) | (var_name ^ (lambda v: VarExp(v)))


def process_parentheses(sentence):
    #print "Process Parentheses -> CALLED"
    ((_, p), _) = sentence
    return p


def exp_parentheses():
    #print "Exp Parentheses -> CALLED"
    return reserved('(') + Recursive(aexp) + reserved(')') ^ process_parentheses


def assign_exp():
    #print "Assign Exp -> CALLED"
    return assign_value() | exp_parentheses()


def process_operation(operation):
    #print "Process Operation -> CALLED"
    return lambda left, right: Operation(operation, left, right)


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


def apply_precedence(value_parser, precedence_levels, combine):
    #print "Apply_Precedence -> CALLED"
    def operation_parse(p_level):
        return op_reducer(p_level) ^ combine
    parser = value_parser * operation_parse(precedence_levels[0])
    for precedence_level in precedence_levels[1:]:
        parser = parser * operation_parse(precedence_level)
    return parser


def aexp():
    #print "Aexp called"
    return apply_precedence(assign_exp(), precedence_levels, process_operation)


def process_bool(sentence):
    #print "Process_bool CALLED"
    ((left, operation), right) = sentence
    return RelExp(operation, left, right)


def bool_exp():
    operators = ['<', '<=', '>', '>=', '=', '!=']
    return aexp() + op_reducer(operators) + Process(aexp(), process_bool)


def bexp():
    return bool_exp()


def parse_assign():
    def process(parsed):
        ((name, _), exp) = parsed
        return Assign(name, exp)
    return var_name + reserved('=') + aexp() ^ process


def list_expressions():
    separator = reserved(';') ^ (lambda x: lambda l, r: Statement(l, r))
    return Exp(statement(), separator)


def parse_if():
    def process(parsed):
        (((((_, condition), _), true), false), _) = parsed
        if false:
            (_, f_statement) = false
        else:
            f_statement = None
        return IfExp(condition, true, f_statement)
    return reserved('if') + bexp() + reserved('{') + Recursive(list_expressions) + reserved('}') + \
           Opt(reserved('else') + reserved('{') + Recursive(list_expressions) + reserved('}')) ^ process


def parse_while():
    def process(parsed):
        ((((_, condition), _), body), _) = parsed
        return WhileExp(condition, body)
    return reserved('while') + bexp() + reserved('{') + Recursive(list_expressions) + reserved('}') ^ process


def statement():
    return parse_assign() | parse_if() | parse_while()


def parser():
    return Validator(list_expressions())


def parse(tokens):
    tree = parser()(tokens, 0)
    return tree

if __name__ == '__main__':
    filename = sys.argv[1]
    file = open(filename)
    characters = file.read()
    file.close()
    tokens = do_lex(characters)
    parser = globals()[sys.argv[2]]()
    result = parser(tokens, 0)
    print result