__author__ = 'Dave and Alex'

import re


class Lexer:

    RESERVED = 'RESERVED'
    INT = 'INT'
    VAR = 'VAR'

    lex = [
        (r'[ \\n\\t]+', None), #matches all whitespaces
        (r'\=', RESERVED),
        (r'\(', RESERVED),
        (r'\)', RESERVED),
        (r'\+', RESERVED),
        (r'-',  RESERVED),
        (r'\*', RESERVED),
        (r'/',  RESERVED),
        (r'[0-9]+',                INT), # matches all integers
        (r'[A-Za-z][A-Za-z0-9_]*', VAR), # matches var names

    ]

    def lexer(self, chars, sentence):
        pos = 0 #Begins in position 0 of the sentence
        tokens = []
        while pos < len(chars):
            match = None #Lexer matching starts with no match
            for token in sentence:
                pattern, tag = token
                regex = re.compile(pattern)
                match = regex.match(chars, pos)
                if match:
                    text = match.group(0)
                    if tag:
                        token = (text, tag)
                        tokens.append(token)
                    break
            if not match:
                print "No match found on the sentence"
            else:
                pos = match.end(0)
        return tokens

    def do_lex(self, characters):
        return self.lexer(characters, self.lex)
