__author__ = 'Dave and Alex'

import sys
from grammar_parser import *
from lexer import *


if __name__ == '__main__':
    values = {}
    init_code = 'e='+str(math.e)+';pi='+str(math.pi)
    token_init = do_lex(init_code)
    parse_init = parse(token_init)
    tree  = parse_init.value
    tree.evaluation(values)

    while True:
        code = raw_input('>>>')
        tokens = do_lex(code)
        parsed = parse(tokens)
        if not parsed:
            new_code = "tempvar=" + code
            tokens = do_lex(new_code)
            parsed = parse(tokens)
            tree = parsed.value
            tree.evaluation(values)
            for index, value in enumerate(values):
                if index < 2:
                    pass
                else:
                    sys.stdout.write('%s\n' % (values[value]))
        else:
            try:
                tree = parsed.value
                tree.evaluation(values)
            except Exception:
                print "Error en el parseo"

