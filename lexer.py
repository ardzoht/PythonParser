__author__ = 'Dave and Alex'

import re
import sys


RESERVED = 'RESERVED'
INT = 'INT'
VAR = 'VAR'

lex = [
    (r'[ \n\t]+', None), #matches all whitespaces
    (r'#[^\n]*', None),
    (r'\=', RESERVED),
    (r'\(', RESERVED),
    (r'\)', RESERVED),
    (r'\+', RESERVED),
    (r'-',  RESERVED),
    (r'\*', RESERVED),
    (r'/',  RESERVED),
    (r'\%', RESERVED),
    (r'\^', RESERVED),
    (r'<=', RESERVED),
    (r'<', RESERVED),
    (r'>=', RESERVED),
    (r'<', RESERVED),
    (r'==', RESERVED),
    (r'!=', RESERVED),
    (r'if', RESERVED),
    (r'else', RESERVED),
    (r'{', RESERVED),
    (r'}', RESERVED),
    (r'while', RESERVED),
    (r'[0-9]+',                INT), # matches all integers
    (r'[A-Za-z][A-Za-z0-9_]*', VAR), # matches var names

]


def lexer(chars, sentence):
    pos = 0 #Begins in position 0 of the sentence
    tokens = []
    while pos < len(chars):
        match = None # Lexer matching starts with no match
        for token_exp in sentence:
            pattern, tag = token_exp
            regex = re.compile(pattern)
            match = regex.match(chars, pos)
            if match:
                text = match.group(0)
                if tag:
                    token_exp = (text, tag)
                    tokens.append(token_exp)
                break
        if not match:
            sys.stderr.write('Illegal character: %s\n' % characters[pos])
            sys.exit(1)
        else:
            pos = match.end(0)
    return tokens


def do_lex(characters):
        return lexer(characters, lex)

if __name__ == '__main__':
    filename = sys.argv[1]
    file = open(filename)
    characters = file.read()
    file.close()
    tokens = do_lex(characters)
    for token in tokens:
        print token
