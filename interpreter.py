__author__ = 'Dave and Alex'

import sys
from grammar_parser import *
from lexer import *


if __name__ == '__main__':
    # Lee el nombre del archivo, guarda el codigo en code
    filename = sys.argv[1]
    code = open(filename).read()
    # Usando do_lex, separa el codigo en tokens
    tokens = do_lex(code)
    # Usando parse, hace el parseo de todas las expresiones
    parsed = parse(tokens)
    # Para en caso de que la expresion no tenga variable asignada, asigna una variable temporal, que guarda el valor
    if not parsed:
        new_code = ""
        try:
            for index, line in enumerate(code.splitlines()):
                if not line[0].isalpha():
                    new_line = vars[index]+"="
                    new_code += new_line + line
                else:
                    new_code += line
                    index_vars.append(line[0])
        except Exception:
            print "Parse error!"
            sys.exit(1)
        # Parsea el codigo con las variables temporales
        tokens = do_lex(new_code)
        parsed_new = parse(tokens)
        # La expresion no es valida
        if not parsed_new:
            print "Parse error!"
            sys.exit(1)
        # Se crea el arbol que se obtiene del parseo
        tree = parsed_new.value
        values = {}
        # Hace la evaluacion de los valores del arbol
        tree.evaluation(values)
        for value in values:
            if value in index_vars:
                sys.stdout.write('--- Resultado ---\n%s = %s\n' % (value, values[value]))
            else:
                sys.stdout.write('--- Resultado ---\n%s\n' % (values[value]))
        sys.exit(1)
    # Se crea el arbol que se obtiene del parseo, sin errores
    tree = parsed.value
    values = {}
    tree.evaluation(values)
    # Escribe el resultado de las expresiones en la consola
    for value in values:
            sys.stdout.write('--- Resultado ---\n%s: %s\n' % (value, values[value]))
