import ply.lex as lex
import re
from collections import deque
# List of token names.   This is always required

class Stack(object):

    def __init__(self):
        self.stack = deque()

    def is_empty(self):
        return len(self.stack) == 0

    def push(self, data):
        self.stack.append(data)

    def pop(self):
        return self.stack.pop()

    def peek(self):
        return self.stack[-1]

    def size(self):
        return len(self.stack)


class tokenList():
    def __init__(self,lexer):
        toks=[]
        tok = lexer.token()
        while tok:
            toks.append(tok)
            tok = lexer.token()
        toks.append(None)
        self.toks = toks
        self.pointer = 0

    def nowTok(self):
        return self.toks[self.pointer]

    def nextTok(self):
        if self.nowTok():
            tok = self.nowTok()
            self.pointer = self.pointer + 1
            return tok

    def backTok(self):
        self.pointer = self.pointer - 1

    def resetTok(self):
        self.pointer = 0

class node():
    def __init__(self,tok):
        self.tok = tok
        self.reverse = False
        self.lnode = None
        self.rnode = None
    def __str__(self):
        return self.tok.value

firstPE = ['LPAREN','EQ']
firstNE = firstPE[:] + ['NOT']
firstAE = firstNE[:]
firstOE = firstAE[:]
firstExp = firstOE[:]


def lexicalAnalysis(data):
    tokens = (
       'OR',
       'NOT',
       'AND',
       'LPAREN',
       'RPAREN',
       'EQ'
    )
    # Regular expression rules for simple tokens
    t_OR    = r'\+'
    t_NOT   = r'-'
    t_AND   = r'\*'
    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'
    t_EQ = r'((AU|TI|KY|AB|SU|DOI|YE)=)?\'(\d|[a-z]|[A-Z]|\s|\.)+\''

    # A regular expression rule with some action code
    def t_NUMBER(t):
        r'\d+'
        t.value = int(t.value)

    # Define a rule so we can track line numbers
    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)
    # A string containing ignored characters (spaces and tabs)
    t_ignore  = ' \t'

    # Error handling rule
    def t_error(t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer
    lexer = lex.lex()
    # Give the lexer some input
    lexer.input(data)
    #tok = lexer.token()
    tl = tokenList(lexer)
    #print(tl.toks)
    return tl

def CmpUnit(tl):
    Exp(tl)
    tok = tl.nextTok()
    if tok:
        raise Exception('ERROR')

def Exp(tl):
    OE(tl)

def OE(tl):
    AE(tl)
    tok = tl.nextTok()
    if tok is None:
        return
    else:
        while tok.type == 'OR':
            #print('+')
            AE(tl)
            tok = tl.nextTok()
            if not tok:
                return
        tl.backTok()

def AE(tl):
    NE(tl)
    tok = tl.nextTok()
    if tok is None:
        return
    else:
        while tok.type == 'AND':
            #print('*')
            NE(tl)
            tok = tl.nextTok()
            if not tok:
                return
        tl.backTok()

def NE(tl):
    tok = tl.nextTok()
    if tok.type == 'NOT':
        #print('-')
        NE(tl)
    elif tok.type in firstPE:
        tl.backTok()
        PE(tl)
    else:
        raise Exception('ERROR')

def PE(tl):
    tok = tl.nextTok()
    if tok.type == 'LPAREN':
        #print('(')
        Exp(tl)
        tok = tl.nextTok()
        if tok.type == 'RPAREN':
            #print(')')
            return
        else:
            raise Exception('ERROR')
    elif tok.type == 'EQ':
        #(tok.value)
        return
    else:
        raise Exception('ERROR')


def opWeight(tok):
    if tok.type == 'NOT':
        return 3
    if tok.type == 'AND':
        return 2
    if tok.type == 'OR':
        return 1
    if tok.type == 'LPAREN':
        return 0



def syntaxAnalysis(tl):
    opStack = Stack()
    nodeStack = Stack()
    tmpStack = Stack()
    treeStack = Stack()

    CmpUnit(tl)

    tl.resetTok()
    while True:
        tok = tl.nextTok()
        if tok is None:
            break
        else:
            if tok.type == 'EQ':
                nodeStack.push(node(tok))
            else:
                if tok.type == 'LPAREN':
                    opStack.push(node(tok))
                elif tok.type == 'RPAREN':
                    while opStack.peek().tok.type != 'LPAREN':
                        nodeStack.push(opStack.pop())
                    opStack.pop()
                else:
                    if not opStack.is_empty():
                        while (opWeight(tok) < opWeight(opStack.peek().tok)):
                            nodeStack.push(opStack.pop())
                            if opStack.is_empty():
                                break
                    opStack.push(node(tok))

    while not opStack.is_empty():
        nodeStack.push(opStack.pop())

    while not nodeStack.is_empty():
        tmpStack.push(nodeStack.pop())

    while not tmpStack.is_empty():
        topType = tmpStack.peek().tok.type
        if topType == 'EQ':
            treeStack.push(tmpStack.pop())
        elif topType == 'NOT':
            treeStack.peek().reverse = not treeStack.peek().reverse
            tmpStack.pop()
        else:
            r = treeStack.pop()
            l = treeStack.pop()
            tmpStack.peek().lnode = l
            tmpStack.peek().rnode = r
            treeStack.push(tmpStack.pop())
    return treeStack.peek()

keymap = ('doi','title','authors','keywords','year','abstract','fields')

def searchTransfer(tree,type):
    if tree is None:
        return
    nodeType = tree.tok.type
    reverse = tree.reverse
    if nodeType != 'EQ':
        list = []
        dict = {}
        list.append(searchTransfer(tree.lnode,type))
        list.append(searchTransfer(tree.rnode,type))
        if nodeType == 'OR':
            if reverse == True:
                dict['bool'] = {'must_not':{'bool': {'should': list}}}
            else:
                dict['bool'] = {'should': list}

        elif nodeType == 'AND':
            if reverse == True:
                dict['bool'] = {'must_not': list}
            else:
                dict['bool'] = {'must': list}
        return dict
    else:
        dict = {'match':{keymap[type]: tree.tok.value[1:-1]}}
        if reverse == True:
            return {'bool':{'must_not':dict}}
        else:
            return dict

