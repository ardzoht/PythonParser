__author__ = 'Dave and Alex'

import sys
from grammar_parser import *
from lexer import *


if __name__ == '__main__':
    # first, adds the values of euler, and pi, to the environment
    values = {}
    init_code = 'e='+str(math.e)+';pi='+str(math.pi)
    token_init = do_lex(init_code) # gets the tokens of the values
    parse_init = parse(token_init) # parses them
    tree  = parse_init.value # gets the tree from the parsed sentence
    tree.evaluation(values) # adds the values to the environment

    while True:
        # initiates the user input
        code = raw_input('>>>')
        # parses the input into tokens, and then gets the tree
        tokens = do_lex(code)
        parsed = parse(tokens)
        # if it's not an assign expression, stores the values into a temporal variable
        if not parsed:
            new_code = "tempvar=" + code
            tokens = do_lex(new_code)
            parsed = parse(tokens)
            tree = parsed.value
            tree.evaluation(values)
            for index, value in enumerate(values):
                # don't show the euler, pi values, unless the user calls show
                if index < 2:
                    pass
                else:
                    sys.stdout.write('%s\n' % (values[value]))
        else:
            # in case it's an assign expression, parse the sentence
            try:
                tree = parsed.value
                tree.evaluation(values)
            except Exception:
                print "Error en el parseo"

