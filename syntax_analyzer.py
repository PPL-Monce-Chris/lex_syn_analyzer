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


# all char classes
class CharClass(Enum):
    EOF = 1
    LETTER = 2
    DIGIT = 3
    OPERATOR_1 = 4
    OPERATOR_2 = 5
    PUNCTUATOR = 6
    QUOTE = 7
    BLANK = 8
    OTHER = 9


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
    if c in ['+', '-', '*', '/']:
        return (c, CharClass.OPERATOR_1)
    if c in ['=', '>', '<', '<=', '>=']:
        return (c, CharClass.OPERATOR_2)
    if c in ['.', ':', ',', ';']:
        return (c, CharClass.PUNCTUATOR)
    if c in [' ', '\n', '\t']:
        return (c, CharClass.BLANK)
    return (c, CharClass.OTHER)


# calls getChar and getChar until it returns a non-blank
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


# all tokens
class Token(Enum):
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
    MULTIPLICATION = 19
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


# lexeme to token conversion

# Special Words

special = {
    "integer": Token.INTEGER_TYPE,
    "boolean": Token.BOOLEAN_TYPE,
    "program": Token.PROGRAM,
    "var": Token.VAR,
    "begin": Token.BEGIN,
    "while": Token.WHILE,
    "do": Token.DO,
    "if": Token.IF,
    "else": Token.ELSE,
    "end": Token.END,
    "false": Token.FALSE,
    "true": Token.TRUE,
    "read": Token.READ,
    "write": Token.WRITE,
    "then": Token.THEN

}

# Punctuation

punct = {
    ":=": Token.ASSIGNMENT,
    ":": Token.COLON,
    ";": Token.SEMICOLON,
    ".": Token.PERIOD
}

# Operations

ops = {
    "+": Token.ADDITION,
    "-": Token.SUBTRACTION,
    "*": Token.MULTIPLICATION
}

# Equivalence

equal = {
    "=": Token.EQUAL,
    ">": Token.GREATER,
    ">=": Token.GREATER_EQUAL,
    "<": Token.LESS,
    "<=": Token.LESS_EQUAL
}


# returns the next (lexeme, token) pair or None if EOF is reached
def lex(input):
    input = getNonBlank(input)

    c, charClass = getChar(input)
    lexeme = ""

    # check EOF first
    if charClass == CharClass.EOF:
        return (input, None, None)

    # Reading letters
    if charClass == CharClass.LETTER:
        while True:
            input, lexeme = addChar(input, lexeme)
            c, charClass = getChar(input)
            if charClass == CharClass.DIGIT:
                continue
            elif lexeme in special:
                return (input, lexeme, special[lexeme])
            elif charClass != CharClass.LETTER and charClass != CharClass.DIGIT:
                break

        return (input, lexeme, Token.IDENTIFIER)

    # Reading digits
    if charClass == CharClass.DIGIT:
        while True:
            input, lexeme = addChar(input, lexeme)
            c, charClass = getChar(input)
            if charClass != CharClass.DIGIT:
                break
        return (input, lexeme, Token.INTEGER_LITERAL)

    # Reading an operator
    if charClass == CharClass.OPERATOR_1:
        input, lexeme = addChar(input, lexeme)
        if lexeme in ops:
            return (input, lexeme, ops[lexeme])

    if charClass == CharClass.OPERATOR_2:
        while True:
            input, lexeme = addChar(input, lexeme)
            c, charClass = getChar(input)
            if charClass != CharClass.OPERATOR_2:
                break
        return (input, lexeme, equal[lexeme])

    # Reading a punctuation
    if charClass == CharClass.PUNCTUATOR:
        while True:
            input, lexeme = addChar(input, lexeme)
            c, charClass = getChar(input)
            if charClass == CharClass.OPERATOR_2:
                input, lexeme = addChar(input, lexeme)
                return (input, lexeme, Token.ASSIGNMENT)
            elif charClass != CharClass.PUNCTUATOR:
                break
        return (input, lexeme, punct[lexeme])

    # TODO: anything else, raise an exception
    raise Exception("Lexical Analyzer Error: unrecognized operator found")











############@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@########################################

















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

###########################################################################################

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
#   Following methods used to print grammar, gotos, actions.

# returns the LHS (left hand side) of a given production
def getLHS(production):
    return production.split("->")[0].strip()

# returns the RHS (right hand side) of a given production
def getRHS(production):
    return production.split("->")[1].strip().split(" ")

# prints the productions of a given grammar, one per line
def printGrammar(grammar, file):
    i = 0
    for production in grammar:
        #file.write(str(i), ". ", getLHS(production), " -> ", str(getRHS(production)))

        file.write(str(i))
        file.write(". ")
        file.write(str(getLHS(production)))
        file.write(" -> ")
        file.write(str(getRHS(production)))
        file.write("\n")


        #print(str(i) + ". " + getLHS(production), end = " -> ")
        #print(getRHS(production))
        i += 1

# prints the given actions, one per line
def printActions(actions, file):
    for key in actions:
        file.write(str(key))
        file.write(" -> ")
        file.write(str(actions[key]))
        file.write("\n")
        #file.write(key, " -> ", actions[key], "\n")


        #file.write(actions[key])
        #print(key, end = " -> ")
        #print(actions[key])

# prints the given gotos, one per line
def printGotos(gotos, file):
    for key in gotos:
        file.write(str(key))
        file.write(" -> ")
        file.write(str(gotos[key]))
        file.write("\n")
        #file.write(str(key, end = " -> ", gotos[key] ))


        #print(key, end = " -> ")
        #print(gotos[key])

#################################################################################

# reads the given input and returns the grammar as a list of productions
def loadGrammar(input):
    grammar = []
    for line in input:
        grammar.append(line.strip())
        #print('grammar to be loaded after strip= ', grammar, '\n')
    return grammar

# reads the given input containing an SLR parsing table and returns the "actions" and "gotos" as dictionaries
def loadTable(input):
    actions = {}
    gotos = {}
    header = input.readline().strip().split(",")
    #print('header *********** = ', header)
    end = header.index("$")
    #print('end = ', end)
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

        print("\n  state  ", state, " ################\n")
        token = input[0]
        print("\n  token  ", token, " ################\n")
        action = actions[(state, token)]
        print("\n  action  ", action, " ################\n")
        print("action: ", end = "")
        print(action)

        if action is None:
            return None  # tree building update

        # shift operation
        if action[0] == 's':
            input.pop(0)
            stack.append(token)
            state = int(action[1:])
            print("\n", "state**************** =  ", state, "\n")
            stack.append(state)

            # TODOd #2: create a new tree, set data to token, and append it to the list of trees
            tree = Tree()
            tree.data = token
            trees.append(tree)

        # reduce operation
        elif action[0] == 'r':
            production = grammar[int(action[1:])]
            lhs = getLHS(production)
            print("\n ^^^^^^^^^^^^ lhs - ", lhs, "\n")
            rhs = getRHS(production)
            for i in range(len(rhs) * 2):
                stack.pop()
            state = stack[-1]
            print("\n &&&&&&&&&& state = ", state, "\n")
            print("\n &&&&&&&&&& lhs = ", lhs, "\n")

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

        elif action == 'acc':
            return True

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

# main
if __name__ == "__main__":

    # checks if source file was passed and if it exists
    if len(sys.argv) != 2:
        raise ValueError("Missing source file")
    source = open(sys.argv[1], "rt")
    if not source:
        raise IOError("Couldn't open source file")
    input = source.read()
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
        print(lexeme, token)













    '''
    input = open("Grammar_new.txt", "rt")
    grammar = loadGrammar(input)
    input.close()

    input = open("slr_table_new.csv", "rt")
    actions, gotos = loadTable(input)
    input.close()
    '''

##############################################################
    # this is to print out grammar actions and gotos to file
    '''
    file = open("read_grammar.txt", "w")
    printGrammar(grammar, file)
    file.close()
    
    file = open("actions.txt", "w")
    printActions(actions, file)
    file.close()

    file = open("gotos.txt", "w")
    printGotos(gotos, file)
    file.close()
    '''

##############################################################


    #input = [ 'integer_literal', 'i', '/', 'l', '*', 'l', '$' ]
    input = ['program', 'i', 'var', 'i', ':',  'types', 'begin', 'read', 'i', ';', 'i', ':=', 'i', '+', 'i', ';', 'write', 'i', 'end', '.' ]


    # tree building update
    '''
    tree = parse(input, grammar, actions, gotos)
    if tree:
        print("Input is syntactically correct!")
        print("Parse Tree:")
        tree.print()
    else:
        print("Code has syntax errors!")
    '''