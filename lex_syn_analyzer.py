'''
CS3210-001
Program 01
9/24/19
Authors:
Chris Johnson
Monce Romero
'''

from enum import Enum
import sys

# classifying characters
class CharClass(Enum):
    EOF        = 1
    LETTER     = 2
    DIGIT      = 3
    OPERATOR   = 4
    PUNCTUATOR = 5
    QUOTE      = 6
    BLANK      = 7
    PAREN      = 8
    OTHER      = 9
    KEYWORD    = 10


# all tokens
class Token(Enum):
    EOF = -1
    ADDITION = 1
    ASSIGNMENT = 2
    BEGIN = 3
    BOOLEAN_TYPE = 4
    COLON = 5
    DO = 6
    ELSE = 7
    END = 8
    EQUAL = 9
    FALSE = 10
    GREATER = 11
    GREATER_EQUAL = 12
    IDENTIFIER = 13
    IF = 14
    INTEGER_LITERAL = 15
    INTEGER_TYPE = 16
    LESS = 17
    LESS_EQUAL = 18
    MULTIPLICATIONS = 19
    PERIOD = 20
    PROGRAM = 21
    READ = 22
    SEMICOLON = 23
    SUBTRACTION = 24
    THEN = 25
    TRUE = 26
    VAR = 27
    WHILE = 28
    WRITE = 29
    # 30 = blank?
    DIVISION = 31


# lexeme to token conversion
lookup = {
    "+"      : Token.ADDITION,
    "-"      : Token.SUBTRACTION,
    "*"      : Token.MULTIPLICATIONS,
    "/"      : Token.DIVISION,
    "("      : Token.OPEN_PAREN,
    ")"      : Token.CLOSE_PAREN,
    "$"      : Token.EOF,

}
# TODO check for lexical error somehow
# TODO check for EOF expected
# TODO check identifier expected
# TODO check special word missing
# TODO check Data type expected
# TODO check identifier or literal value expected
# TODO check syntax error




# error messages to be used
def errorMessage(code):
    msg = "Error " + str(code).zfill(2) + ": "
    if code == 1:
        return msg + "source file missing"
    if code == 2:
        return msg + "couldn't open source file"
    if code == 3:
        return msg + "lexical error"
    if code == 4:
        return msg + "couldn't open grammar file"
    if code == 5:
        return msg + "couldn't open SLR table file"
    if code == 6:
        return msg + "EOF expected"
    if code == 7:
        return msg + "identifier expected"
    if code == 8:
        return msg + "special word missing"
    if code == 9:
        return msg + "symbol missing"
    if code == 10:
        return msg + "data type expected"
    if code == 11:
        return msg + "identifier or literal value expected"

    # any other errors go between 11 - 99

    if code == 99:
        return msg + "Syntax error"
    return msg + "syntax error"


    # TODO: Token addition
    # TODO: Token assignment
    # TODO: Token Colon
    # TODO: Token equal
    # TODO: Token greater
    # TODO: Token greater equal
    # TODO: Token identifier ?
    # TODO: Token integer_literal
    # TODO: Token ineteger_type
    # TODO: Token Less
    # TODO: Token Less_Equal
    # TODO: Token Multiplication
    # TODO: Token Period? may be char
    # TODO: Token Semicolon
    # TODO: Token Subtraction


# reads the next char from input and returns its class
def getChar(input):
    if len(input) == 0:
        return (None, CharClass.EOF)

    c = input[0].lower()

    if c.isalpha():
        return (c, CharClass.LETTER)

    if c.isdigit():
        return (c, CharClass.DIGIT)

    if c == '"':
        return (c, CharClass.QUOTE)

    if c in ['+', '-', '*', '/', '>', '>=', '=', '<=', '<']:
        return (c, CharClass.OPERATOR)

    if c in ['.', ';']:
        return (c, CharClass.PUNCTUATOR)

    if c in [' ', '\n', '\t']:
        return (c, CharClass.BLANK)

    if c in ['(', ')']:
        return (c, CharClass.DELIMITER)

    if c in ['if', 'while', 'return']:
        return (c, CharClass.KEYWORD)


    return (c, CharClass.OTHER)


####################################################################################################


# calls getChar and addChar until it returns a non-blank
def getNonBlank(input):
    ignore = ""
    while True:
        c, charClass = getChar(input)
        if charClass == CharClass.BLANK:
            input, ignore = addChar(input, ignore)
        else:
            return input


# adds the next char from input to lexeme, advancing the input by one char
def addChar(input, lexeme):
    if len(input) > 0:
        lexeme += input[0]
        input = input[1:]
    return (input, lexeme)


####################################################################################


# Tree class
class Tree:
    TAB = "   "

    def __init__(self):
        self.data = None
        self.children = []

    def add(self, child):
        self.children.append(child)

    def print(self, tab=""):
        if self.data != None:
            print(tab + self.data)
            tab += self.TAB
            for child in self.children:
                if isinstance(child, Tree):
                    child.print(tab)
                else:
                    print(tab + child)


########################################################################################


# returns the LHS (left hand side) of a given production
def getLHS(production):
    return production.split("->")[0].strip()


# returns the RHS (right hand side) of a given production
def getRHS(production):
    return production.split("->")[1].strip().split(" ")


#########################################################################################


# reads the given input containing an SLR parsing table and returns the "actions" and "gotos" as dictionaries
def loadTable(input):
    actions = {}
    gotos = {}
    header = input.readline().strip().split(",")
    end = header.index("$")
    tokens = []
    for field in header[1:end + 1]:
        tokens.append(field)
        # tokens.append(int(field))
    variables = header[end + 1:]
    for line in input:
        row = line.strip().split(",")
        state = int(row[0])
        for i in range(len(tokens)):
            token = tokens[i]
            key = (state, token)
            value = row[i + 1]
            if len(value) == 0:
                value = None
            actions[key] = value
        for i in range(len(variables)):
            variable = variables[i]
            key = (state, variable)
            value = row[i + len(tokens) + 1]
            if len(value) == 0:
                value = None
            gotos[key] = value
    return (actions, gotos)



def loadGrammar(input):
    grammar = []
    for line in input:
        grammar.append(line.strip())
    return grammar


####################################################################################


# given an input (source program), grammar, actions, and gotos, returns true/false depending whether the input should be accepted or not
def parse(input, grammar, actions, gotos):

    # TODOd #1: create a list of trees
    trees = []

    stack = []
    stack.append(0)
    while True:
        print("stack: ", end = "")
        print(stack, end = " ")
        print("input: ", end = "")
        print(input, end = " ")
        state = stack[-1]
        token = input[0]
        action = actions[(state, token)]
        print("action: ", end = "")
        print(action)

        if action is None:
            return None  # tree building update

        # shift operation
        if action[0] == 's':
            input.pop(0)
            stack.append(token)
            state = int(action[1])
            stack.append(state)

            # TODOd #2: create a new tree, set data to token, and append it to the list of trees
            tree = Tree()
            tree.data = token
            trees.append(tree)

        # reduce operation
        elif action[0] == 'r':
            production = grammar[int(action[1])]
            lhs = getLHS(production)
            rhs = getRHS(production)
            for i in range(len(rhs) * 2):
                stack.pop()
            state = stack[-1]
            stack.append(lhs)
            stack.append(int(gotos[(state, lhs)]))

            # TODOd #3: create a new tree and set data to lhs
            newTree = Tree()
            newTree.data = lhs

            # TODOd #4: get "len(rhs)" trees from the right of the list of trees and add each of them as child of the new tree you created, preserving the left-right order
            for tree in trees[-len(rhs):]:
                newTree.add(tree)

            # TODOd #5: remove "len(rhs)" trees from the right of the list of trees
            trees = trees[:-len(rhs)]

            # TODOd #6: append the new tree to the list of trees
            trees.append(newTree)

        # not a shift or reduce operation, must be an "accept" operation
        else:
            production = grammar[0]
            lhs = getLHS(production)
            rhs = getRHS(production)

            # TODOd #7: same as reduce but using the 1st rule of the grammar
            root = Tree()
            root.data = lhs
            for tree in trees:
                root.add(tree)

            # TODOd #8: return the new tree
            return root



# returns the next (lexeme, token) pair or None if EOF is reached
def lex(input):
    input = getNonBlank(input)

    c, charClass = getChar(input)
    lexeme = ""

    # check EOF first
    if charClass == CharClass.EOF:
        return (input, None, None)


    # TODO: reading If
    # TODO: reading Begin
    # TODO: reading Boolean_type
    # TODO: reading DO
    # TODO: reading Else
    # TODO: reading End.
    # TODO: reading False
    # TODO: reading Integer Type
    # TODO: reading period   idk if this is char?
    # TODO: reading Program
    # TODO: reading Read
    # TODO: reading Then
    # TODO: reading True
    # TODO: reading Var
    # TODO: reading While
    # TODO: reading Write
    # TODO: reading "  " aka blank





    # TODO: reading letters + digits
    if charClass == CharClass.LETTER:
        while True:
            input, lexeme = addChar(input, lexeme)
            c, charClass = getChar(input)

            if charClass == CharClass.DIGIT:
                continue
            elif charClass != CharClass.LETTER:
                break

        return (input, lexeme, Token.IDENTIFIER)

    # TODO: reading digits
    if charClass == CharClass.DIGIT:
        while True:
            input, lexeme = addChar(input, lexeme)
            c, charClass = getChar(input)
            if charClass != CharClass.DIGIT:
                break
        return (input, lexeme, Token.LITERAL)

    # TODO: reading an operator
    if charClass == CharClass.OPERATOR:
        input, lexeme = addChar(input, lexeme)
        if lexeme in lookup:
            return (input, lexeme, lookup[lexeme])

    # TODO: Open/Close parenthases
    if charClass == CharClass.PAREN:
        input, lexeme = addChar(input, lexeme)
        if lexeme in lookup:
            return(input, lexeme, lookup[lexeme])

    # TODO: anything else, raise an exception
   # raise Exception("Lexical Analyzer Error: unrecognized symbol was found!")









#########################################################################################

# main
if __name__ == "__main__":

    if len(sys.argv) != 2:
        raise Exception(errorMessage(1))
    source = open(sys.argv[1], "rt")
    if not source:
        raise Exception(errorMessage(2))
    user_input = source.read()
    source.close()
    output = []

    # main loop
    while True:
        input, lexeme, token = lex(input)
        if lexeme == None:
            break
        output.append((lexeme, token))

    # prints the output
    for (lexeme, token) in output:
        print(lexeme, " -- ", token)



    input = open("grammar.txt", "rt")
    grammar = loadGrammar(input)
    # printGrammar(grammar)
    input.close()

    input = open("slr_table.csv", "rt")
    actions, gotos = loadTable(input)
    # printActions(actions)
    # printGotos(gotos)
    input.close()

    # in the beginning we will write the input as a sequence of terminal symbols, ending by $
    # later we will integrate this code with the lexical analyzer
    input = [ 'l', '+', 'i', '/', 'l', '*', 'l', '$' ]

    # tree building update
    tree = parse(input, grammar, actions, gotos)
    if tree:
        print("Input is syntactically correct!")
        print("Parse Tree:")
        tree.print()
    else:
        raise Exception(errorMessage(99))

