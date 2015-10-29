__author__ = 'Dave and Alex'

from math import pow

#Builds a Node with a value, and a position in the sentence
class Node:
    def __init__(self,value, pos):
        self.value = value
        self.pos = pos

    def __repr__(self):
        return 'Nodo({}, Caracteres={})'.format(self.value, self.pos)


#Parent of all the parsers
class Parser:

    def __call__(self, tokens, pos):
        return None

    def __add__(self, other):
        return Sum(self, other)

    def __xor__(self, other):
        return Process(self, other)

    def __mul__(self, other):
        return Exp(self, other)

    def __or__(self, other):
        return Compare(self, other)


#Validates a RESERVED word
class Reserved(Parser):
    def __init__(self, value, tag):
        self.value = value
        self.tag = tag

    def __call__(self, tokens, pos):
        #tokens[pos][0] == value, tokens[pos][1] == tag
        #tokens[pos][1] == value, tokens[pos][0] == tag
        if pos < len(tokens) and tokens[pos][0] == self.value and tokens[pos][1] == self.tag:
            #the token can be parsed
            return Node(tokens[pos][0], pos + 1) #send the next position of token
        else:
            return None


#Validates a tag (INT, RESERVED WORD, OR VARIABLE)
class Tag(Parser):
    def __init__(self, tag):
        self.tag = tag

    def __call__(self, tokens, pos):
        if pos < len(tokens) and tokens[pos][1] is self.tag:
            #the tag is equal
            return Node(tokens[pos][0], pos + 1)
        else:
            return None


#Concatenates 2 or more expressions
class Sum(Parser):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, tokens, pos):
        left = self.left(tokens, pos)
        if left:
            right = self.right(tokens, left.pos)
            if right:
                value = (left.value, right.value)
                return Node(value, right.pos) #move the position to the end of the right result
        return None


#Process a sentence, and then returns the result
class Process(Parser):
    def __init__(self, parser, func):
        self.parser = parser
        self.func = func

    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos) # process the lexed sentence
        if result:
            result.value = self.func(result.value)
            return result


#Converts a parser to a Node
class Result(Parser):
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens, pos):
        results = []
        result = self.parser(tokens,pos)
        while result:
            results.append(result.value)
            pos = result.pos
            result = self.parser(tokens,pos)
        return Node(results, pos)


#Builds recursive expressions
class Recursive(Parser):
    def __init__(self, func):
        self.parser = None
        self.func = func

    def __call__(self, tokens, pos):
        if not self.parser:
            self.parser = self.func() # call the function passed as a parameter
        return self.parser(tokens, pos)


#Validates the body of a sentence
class Validator(Parser):
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)
        if result and result.pos == len(tokens): #check the end of the tokened sentence
            return result
        else:
            return None


#Compares 2 parsers, if left doesn't exist, applies the right one
class Compare(Parser):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, tokens, pos):
        left = self.left(tokens, pos)
        if left:
            return left
        else:
            right = self.right(tokens, pos)
            return right


#Evaluates a list of expressions separated by ;
class Exp(Parser):
    def __init__(self, parser, separator):
        self.parser = parser
        self.separator = separator

    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)

        def process_next(parsed_sentence):
            (func, right) = parsed_sentence
            return func(result.value, right)
        next_parser = self.separator + self.parser ^ process_next

        next_sentence = result
        while next_sentence:
            next_sentence = next_parser(tokens, result.pos)
            if next_sentence:
                result = next_sentence
        return result


class Opt(Parser):
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)
        if result:
            return result
        else:
            return Node(None, pos)

class IntExp:
    def __init__(self, num):
        self.num = num

    def __repr__(self):
        return 'Numero(%s)' % self.num

    def evaluation(self, env):
        return self.num

class VarExp:
    def __init__(self, variable):
        self.variable = variable

    def __repr__(self):
        return 'Variable(%s)' % self.variable

    def evaluation(self, env):
        if self.variable in env:
            return env[self.variable]

class Operation:
    def __init__(self, operation, left, right):
        self.operation = operation
        self.left = left
        self.right = right

    def __repr__(self):
        return 'Operacion( %s, %s, %s)' % (self.operation, self.left, self.right)

    def only_operation(self, env):
        valor_izq = self.left.evaluation(env)
        valor_der = self.right.evaluation(env)
        if self.operation == '+':
            valor = valor_izq + valor_der
        elif self.operation == '-':
            valor = valor_izq - valor_der
        elif self.operation == '*':
            valor = valor_izq * valor_der
        elif self.operation == '/':
            valor = valor_izq / valor_der
        elif self.operation == '^':
            valor = pow(valor_izq, valor_der)
        elif self.operation == '%':
            valor = valor_izq % valor_der
        else:
            raise RuntimeError('Error: Operador desconocido. Operador: ' + self.operation)
        env['Valor'] = valor

    def evaluation(self, env):
        valor_izq = self.left.evaluation(env)
        valor_der = self.right.evaluation(env)
        if self.operation == '+':
            valor = valor_izq + valor_der
        elif self.operation == '-':
            valor = valor_izq - valor_der
        elif self.operation == '*':
            valor = valor_izq * valor_der
        elif self.operation == '/':
            valor = valor_izq / valor_der
        elif self.operation == '^':
            valor = pow(valor_izq, valor_der)
        elif self.operation == '%':
            valor = valor_izq % valor_der
        else:
            raise RuntimeError('Error: Operador desconocido. Operador: ' + self.operation)
        return valor

class RelExp:
    def __init__(self, operation, left, right):
        self.operation = operation
        self.left = left
        self.right = right

    def evaluation(self, env):
        valor_izq = self.left.evaluation(env)
        valor_der = self.right.evaluation(env)
        if self.operation == '<':
            valor = valor_izq < valor_der
        elif self.operation == '>':
            valor = valor_izq > valor_der
        elif self.operation == '<=':
            valor = valor_izq <= valor_der
        elif self.operation == '>=':
            valor = valor_izq >= valor_der
        elif self.operation == '==':
            valor = valor_izq == valor_der
        elif self.operation == '!=':
            valor = valor_izq != valor_der
        else:
            raise RuntimeError('Error: Operador desconocido. Operador: ' + self.operation)
        return valor


class Assign:
    def __init__(self, name, exp):
        self.name = name
        self.exp = exp

    def __repr__(self):
        return 'Asignacion(%s , %s)' % (self.name, self.exp)

    def evaluation(self, env):
        value = self.exp.evaluation(env)
        env[self.name] = value

class Statement:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return 'AsignacionComp(%s, %s)' % (self.left, self.right)

    def evaluation(self, env):
        self.left.evaluation(env)
        self.right.evaluation(env)

class IfExp:
    def __init__(self, condition, true, false):
        self.condition = condition
        self.true = true
        self.false = false

    def __repr__(self):
        return 'AsignacionIf(%s, %s, %s)' % (self.condition, self.true, self.false)

    def evaluation(self, env):
        valor_condicional = self.condition.evaluation(env)
        if valor_condicional:
            self.true.evaluation(env)
        else:
            if self.false:
                self.false.evaluation(env)

class WhileExp:
    def __init__(self, condition, exp):
        self.condition = condition
        self.exp = exp

    def __repr__(self):
        return 'AsignacionWhile(%s, %s)' % (self.condition, self.exp)

    def evaluation(self, env):
        valor_condicional = self.condition.evaluation(env)
        while valor_condicional:
            self.exp.evaluation(env)
            valor_condicional = self.condition.evaluation(env)

class FuncExp:
    def __init__(self, name, exp):
        self.name = name
        self.exp = exp

    def __repr__(self):
        return 'Funcion(%s, %s)' % (self.name, self.exp)

    def evaluation(self, env):
        env[self.name] = self.exp

class CallExp:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'LlamadaFuncion(%s)' % self.name

    def evaluation(self, env):
        exp = env[self.name]
        exp.evaluation(env)

class ForExp:
    def __init__(self, first, second, exp):
        self.first = first
        self.second = second
        self.exp = exp

    def __repr__(self):
        return 'For(%s, %s, %s)' % (self.first, self.second, self.exp)

    def evaluation(self, env):
        for num in range(self.first, self.second):
            self.exp.evaluation(env)
