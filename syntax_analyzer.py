'''
CS3210-001
Program 01
9/24/19
Authors:
Chris Johnson
Monce Romero
'''

from enum import Enum
from tree import Tree
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

def parse_error1 (input, stack, passed_var, passed_begin, passed_if, passed_else, passed_then, passed_while):
    if stack == "program" and input != "i":
        raise Exception(errorMessage(7))
    if stack == "i" and input != ":":
        raise Exception(errorMessage(99))

def parse_error (input, stack, stack_prev, passed_var, passed_begin, passed_if, passed_else, passed_then, passed_while):

    if stack_prev == "program" and stack == "i" and input != "var":
        raise Exception(errorMessage(8))

    if stack == "program" and input != "i":
        raise Exception(errorMessage(7))

    if stack == "i" and input != ":" and passed_begin == False:
        raise Exception(errorMessage(99))

    if passed_begin == True and passed_var == True and stack_prev == "begin" and input == ";":
        raise Exception(errorMessage(9))

    if passed_begin == False and passed_var == True and stack == ":" and input != "type":
        raise Exception(errorMessage(10))

    if passed_begin == True and passed_var == True and stack_prev == "<=" and stack != "arithmetic_expression":
        raise Exception(errorMessage(99))

    if passed_begin == True and passed_var == True and  stack == ":=" and input != "i":
        raise Exception(errorMessage(11))

    if passed_begin == True and passed_var == True:
        if stack_prev != "<=" or stack_prev != "<" or stack_prev != "=" or stack_prev != ">=" or stack_prev != ">" :
            if stack == "i" and input != "then":
                raise Exception(errorMessage(99))

    if passed_then == True and stack_prev == ":=" and stack == "true" and input != ";":
        raise Exception(errorMessage(99))

    if stack == "." and input != "$":
        raise Exception(errorMessage(6))

    if stack_prev == "while" and stack == "arithmetic_expression" and input == "do":
        raise Exception(errorMessage(9))


###########################################################################################

convert = {
    "ASSIGNMENT" : ":=",
    "COLON" : ":",
    "SEMICOLON" : ";",
    "PERIOD" : ".",
    "ADDITION" : "+",
    "SUBTRACTION" : "-",
    "MULTIPLICATION" : "*",
    "EQUAL" : "=",
    "GREATER" : ">",
    "GREATER_EQUAL" : ">=",
    "LESS" : "<",
    "LESS_EQUAL" : "<=",
    "INTEGER_TYPE" : "Integer",
    "BOOLEAN_TYPE" : "Boolean",
    "PROGRAM" : "program",
    "VAR" : "var",
    "BEGIN" : "begin",
    "WHILE" : "while",
    "DO" : "do",
    "IF" : "if",
    "ELSE" : "else",
    "END" : "end",
    "FALSE" : "false",
    "TRUE" : "true",
    "READ" : "read",
    "WRITE" : "write",
    "THEN" : "then",
    "IDENTIFIER" : "i",
    "INTEGER_LITERAL": "integer_literal",
    }

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
        file.write(str(i))
        file.write(". ")
        file.write(str(getLHS(production)))
        file.write(" -> ")
        file.write(str(getRHS(production)))
        file.write("\n")
        i += 1

# prints the given actions, one per line
def printActions(actions, file):
    for key in actions:
        file.write(str(key))
        file.write(" -> ")
        file.write(str(actions[key]))
        file.write("\n")

# prints the given gotos, one per line
def printGotos(gotos, file):
    for key in gotos:
        file.write(str(key))
        file.write(" -> ")
        file.write(str(gotos[key]))
        file.write("\n")

#################################################################################

# reads the given input and returns the grammar as a list of productions
def loadGrammar(input):
    grammar = []
    for line in input:
        grammar.append(line.strip())
    return grammar

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

# given an input (source program), grammar, actions, and gotos, returns true/false depending whether the input should be accepted or not
def parse(input, grammar, actions, gotos):
    passed_var = False
    passed_begin = False
    passed_while = False
    passed_then = False
    passed_else = False
    passed_if = False

    trees = []
    tree_bool = None

    stack = []
    stack.append(0)
    while True:

        print("stack: ", end = "")
        print(stack, end = " \n")
        print("input: ", end = "")
        print(input, end = " \n")
        state = stack[-1]
        token = input[0]
        action = actions[(state, token)]
        print("action: ", end = "")
        print(action)

        if stack[len(stack) -2] == "var":
            passed_var = True

        if stack[len(stack) -2] == "begin":
            passed_begin = True

        if stack[len(stack) -2] == "while":
            passed_while = True

        if stack[len(stack) -2] == "then":
            passed_then = True

        if stack[len(stack) -2] == "else":
            passed_else = True

        if stack[len(stack) -2] == "if":
            passed_if = True

        if action is None:

            if len(stack) > 4:
                parse_error(input[0], stack[-2], stack[-4], passed_var, passed_begin, passed_if, passed_else, passed_then, passed_while)
            else:
                parse_error1(input[0], stack[-2], passed_var, passed_begin, passed_if, passed_else, passed_then, passed_while)

            return tree, False

        # shift operation
        if action[0] == 's':
            input.pop(0)
            stack.append(token)
            state = int(action[1:])
            stack.append(state)

            tree = Tree()
            tree.data = token
            trees.append(tree)

        # reduce operation
        elif action[0] == 'r':
            production = grammar[int(action[1:])]
            lhs = getLHS(production)
            rhs = getRHS(production)
            for i in range(len(rhs) * 2):
                stack.pop()
            state = stack[-1]
            stack.append(lhs)
            stack.append(int(gotos[(state, lhs)]))

            newTree = Tree()
            newTree.data = lhs

            for tree in trees[-len(rhs):]:
                newTree.add(tree)

            trees = trees[:-len(rhs)]
            trees.append(newTree)

        # not a shift or reduce operation, must be an "accept" operation
        else:
            production = grammar[0]
            lhs = getLHS(production)
            rhs = getRHS(production)

            root = Tree()
            root.data = lhs
            for tree in trees:
                root.add(tree)

            return root, True

# main
if __name__ == "__main__":

    # checks if source file was passed and if it exists
    if len(sys.argv) != 2:
        raise ValueError("Missing source file")
    source = open('sources/' + sys.argv[1], "rt")
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
    tokens = []
    # getting the keys to strip
    for (lexeme, token) in output:
        tokens.append(str(token))

    str_token = []
    for (x) in range(len(tokens)):
        n = convert[tokens[x][6:]]
        str_token.append(n)
    # adding end symbol
    str_token.append("$")

    input = open("grammar/grammar.txt", "rt")
    grammar = loadGrammar(input)
    input.close()

    input = open("slr/slr_table.csv", "rt")
    actions, gotos = loadTable(input)
    input.close()


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

    new_tree , tree_bool= parse(str_token, grammar, actions, gotos)
    if tree_bool:
        print("Input is syntactically correct!")
        print("Parse Tree:")
        new_tree.print()
    else:
        print("syntax incorrect")