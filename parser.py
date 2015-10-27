__author__ = 'Dave and Alex'

from lexer import *
from nodes import *

lexer = Lexer()

#Parser for reserved words
def reserved(var):
    return Reserved(var, lexer.RESERVED)

var_name = Tag(lexer.VAR)
number = Process(Tag(lexer.VAR), (lambda i: int(i)))




