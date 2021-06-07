from enum import Enum, auto

from . import lox

class TokenType(Enum):
    # single character tokens

    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()
    SEMICOLON = auto()
    SLASH = auto()
    STAR = auto()

    # one or two character tokens

    BANG = auto()
    EQUAL = auto()
    LESS = auto()
    GREATER = auto()

    BANG_EQUAL = auto()
    EQUAL_EQUAL = auto()
    LESS_EQUAL = auto()
    GREATER_EQUAL = auto()

    # literals
    STRING = auto()
    NUMBER = auto()
    IDENTIFIER = auto()

    # keywords
    AND = auto()
    CLASS = auto()
    ELSE = auto()
    FALSE = auto()
    FUN = auto()
    FOR = auto()
    IF = auto()
    NIL = auto()
    OR = auto()
    PRINT = auto()
    RETURN = auto()
    SUPER = auto()
    THIS = auto()
    TRUE = auto()
    VAR = auto()
    WHILE = auto()

class Token:
    def __init__(self, type, lexeme, literal, line):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return f'Token({self.type.name}, {self.lexeme}, {self.literal}, {self.line})'

class Scanner:
    keywords = {
        'and': TokenType.AND,
        'class': TokenType.CLASS,
        'else': TokenType.ELSE,
        'false': TokenType.FALSE,
        'for': TokenType.FOR,
        'fun': TokenType.FUN,
        'if': TokenType.IF,
        'nil': TokenType.NIL,
        'or': TokenType.OR,
        'print': TokenType.PRINT,
        'return': TokenType.RETURN,
        'super': TokenType.SUPER,
        'this': TokenType.THIS,
        'true': TokenType.TRUE,
        'var': TokenType.VAR,
        'while': TokenType.WHILE,
    }

    def __init__(self, source):
        self.source = source
        self.tokens = []

        self.start = 0
        self.current = 0
        self.line = 1

    def isAtEnd(self):
        return self.current >= len(self.source)

    def advance(self):
        c = self.source[self.current]
        self.current += 1
        return c
    
    def match(self, expected):
        if self.isAtEnd():
            return False

        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def peek(self):
        if self.isAtEnd():
            return '\0'

        return self.source[self.current]

    def peekNext(self):
        if self.current+1 >= len(self.source):
            return '\0'

        return self.source[self.current+1]

    def string(self):
        while self.peek() != '"' and\
            not self.isAtEnd():
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        if self.isAtEnd():
            lox.error(self.line, 'Unterminated string.')
            return
        
        # the closing '"'
        self.advance()

        # trim the surrounding quotes
        value = self.source[self.start+1:self.current-1]
        self.addToken(TokenType.STRING, value)

    def number(self):
        while self.peek().isdigit():
            self.advance()

        # look for a fractional part
        if self.peek() == '.' and self.peekNext().isdigit():
            # consume the '.'
            self.advance()

        while self.peek().isdigit():
            self.advance()

        self.addToken(TokenType.NUMBER,
                      float(self.source[self.start:self.current]))

    def identifier(self):
        while self.peek().isalnum():
            self.advance()

        text = self.source[self.start:self.current]

        type = (
            self.keywords[text]
            if text in self.keywords
            else TokenType.IDENTIFIER
        )

        self.addToken(type)

    def addToken(self, type, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def scanToken(self):
        c = self.advance()
        if c == '(':
            self.addToken(TokenType.LEFT_PAREN)
        elif c == ')':
            self.addToken(TokenType.RIGHT_PAREN)
        elif c == '{':
            self.addToken(TokenType.LEFT_BRACE)
        elif c == '}':
            self.addToken(TokenType.RIGHT_BRACE)
        elif c == ',':
            self.addToken(TokenType.COMMA)
        elif c == '.':
            self.addToken(TokenType.DOT)
        elif c == '-':
            self.addToken(TokenType.MINUS)
        elif c == '+':
            self.addToken(TokenType.PLUS)
        elif c == ';':
            self.addToken(TokenType.SEMICOLON)
        elif c == '*':
            self.addToken(TokenType.STAR)
        elif c == '!':
            self.addToken(TokenType.BANG_EQUAL
                          if self.match('=')
                          else TokenType.BANG)
        elif c == '=':
            self.addToken(TokenType.EQUAL_EQUAL
                          if self.match('=')
                          else TokenType.EQUAL)
        elif c == '<':
            self.addToken(TokenType.LESS_EQUAL
                          if self.match('=')
                          else TokenType.LESS)
        elif c == '>':
            self.addToken(TokenType.GREATER_EQUAL
                          if self.match('=')
                          else TokenType.GREATER)
        elif c == '/':
            if self.match('/'):
                while self.peek() != '\n' and\
                    not self.isAtEnd():
                    self.advance()
            else:
                self.addToken(TokenType.SLASH)
        elif c in [' ', '\r', '\t']:
            # ignore whitespace
            pass
        elif c == '\n':
            self.line += 1
        elif c == '"':
            self.string()
        else:
            if c.isdigit():
                self.number()
            elif c.isalpha():
                self.identifier()
            else:
                lox.error(self.line, 'Unexpected character.')

    def scanTokens(self):
        while not self.isAtEnd():
            self.start = self.current
            self.scanToken()

        return self.tokens