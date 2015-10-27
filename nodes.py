__author__ = 'Dave and Alex'


class Node:
    def __init__(self,value, pos):
        self.value = value
        self.pos = pos

    def __repr__(self):
        return 'Parse({}, {})'.format(self.value, self.pos)


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


class Reserved(Parser):
    def __init__(self, value, tag):
        self.value = value
        self.tag = tag

    def __call__(self, tokens, pos):
        #tokens[pos][1] == value, tokens[pos][0] == tag
        if pos < len(tokens) and tokens[pos][1] == self.value and tokens[pos][1] == self.tag:
            #the token can be parsed
            return Node(tokens[pos][0], pos + 1) #send the next position of token
        else:
            return None


class Tag(Parser):
    def __init__(self, tag):
        self.tag = tag

    def __call__(self, tokens, pos):
        if pos < len(tokens) and tokens[pos][1] is self.tag:
            #the tag is equal
            return Node(tokens[pos][0], pos + 1)
        else:
            return None


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


class Process(Parser):
    def __init__(self, parser, func):
        self.parser = parser
        self.func = func

    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos) # process the lexed sentence
        if result:
            result.value = self.func(result.value)
            return result

class Recursive(Parser):
    def __init__(self, func):
        self.parser = None
        self.func = func

    def __call__(self, tokens, pos):
        if not self.parser:
            self.parser = self.func() # call the function passed as a parameter
        return self.parser(tokens, pos)


class Validator(Parser):
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)
        if result and result.pos == len(tokens): #check the end of the tokened sentence
            return result
        else:
            return None


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


class IntExp():
    def __init__(self, num):
        self.num = num


class VarExp():
    def __init__(self, variable):
        self.variable = variable


class Operation():
    def __init__(self, operation, left, right):
        self.operation = operation
        self.left = left
        self.right = right



