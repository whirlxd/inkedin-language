from typing import List, Union
from language.tokentype import TokenType
from language.tokn import Token
from language.errors import LexerError

class Lexer:
    def __init__(self, text: str):
        self.text = text  
        self.pos = 0
        self.line = 1
        self.tokens = []
        
        self.keywords = {
            'connect': TokenType.CONNECT, 
            'thoughts': TokenType.THOUGHTS,
            'network': TokenType.NETWORK, 
            'pivot': TokenType.PIVOT,
            'circle_back': TokenType.CIRCLE_BACK,
            'synergy': TokenType.SYNERGY,
            'leverage': TokenType.LEVERAGE,
            'disrupt': TokenType.DISRUPT,
            'scale': TokenType.SCALE,
            'reach_out': TokenType.REACH_OUT,
            'game_changer': TokenType.GAME_CHANGER,
            'lessons_learned': TokenType.LESSONS_LEARNED,
            'true': TokenType.BOOLEAN,
            'false': TokenType.BOOLEAN,
        }
    
    def error(self, message: str):
        raise LexerError(f"Line {self.line}: {message}")
    
    def peek(self, offset: int = 0) -> str:  
        pos = self.pos + offset
        if pos >= len(self.text):
            return '\0'
        return self.text[pos]
    
    def advance(self) -> str:
        if self.pos < len(self.text):
            char = self.text[self.pos]
            self.pos += 1
            if char == '\n':
                self.line += 1
            return char
        return '\0'
    
    def skip_whitespace(self):
        while self.peek() in ' \t\r':
            self.advance()
    
    def read_string(self) -> str:
        value = ""
        self.advance()  
        
        while self.peek() != '"' and self.peek() != '\0':
            if self.peek() == '\\':
                self.advance()
                next_char = self.advance()
                if next_char == 'n':
                    value += '\n'
                elif next_char == 't':
                    value += '\t'
                elif next_char == 'r':
                    value += '\r'
                elif next_char == '\\':
                    value += '\\'
                elif next_char == '"':
                    value += '"'
                else:
                    value += next_char
            else:
                value += self.advance()
        
        if self.peek() == '\0':
            self.error("Unterminated string")
        
        self.advance() 
        return value
    
    def read_number(self) -> Union[int, float]:
        value = ""
        has_dot = False
        
        while self.peek().isdigit() or self.peek() == '.':
            if self.peek() == '.':
                if has_dot:
                    break
                has_dot = True
            value += self.advance()
        
        return float(value) if has_dot else int(value)
    
    def read_identifier(self) -> str:
        value = ""
        while self.peek().isalnum() or self.peek() == '_':
            value += self.advance()
        return value
    
    def tokenize(self) -> List[Token]:
        while self.pos < len(self.text):
            self.skip_whitespace()
            
            if self.peek() == '\0':
                break
            
            # Comments
            if self.peek() == '/' and self.peek(1) == '/':
                while self.peek() != '\n' and self.peek() != '\0':
                    self.advance()
                continue
            
            # Newlines
            if self.peek() == '\n':
                self.tokens.append(Token(TokenType.NEWLINE, '\n', self.line))
                self.advance()
                continue
            
            # Strings
            if self.peek() == '"':
                value = self.read_string()
                self.tokens.append(Token(TokenType.STRING, value, self.line))
                continue
            
            # Numbers
            if self.peek().isdigit():
                value = self.read_number()
                self.tokens.append(Token(TokenType.NUMBER, value, self.line))
                continue
            
            # Identifiers and keywords
            if self.peek().isalpha() or self.peek() == '_':
                value = self.read_identifier()
                token_type = self.keywords.get(value, TokenType.IDENTIFIER)
                self.tokens.append(Token(token_type, value, self.line))
                continue
            
            # Two-character operators
            if self.peek() == '=' and self.peek(1) == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.EQUALS, '==', self.line))
                continue
            
            if self.peek() == '!' and self.peek(1) == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.NOT_EQUALS, '!=', self.line))
                continue
            
            if self.peek() == '<' and self.peek(1) == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.LESS_EQUAL, '<=', self.line))
                continue
            
            if self.peek() == '>' and self.peek(1) == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.GREATER_EQUAL, '>=', self.line))
                continue
            
            if self.peek() == '&' and self.peek(1) == '&':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.AND, '&&', self.line))
                continue
            
            if self.peek() == '|' and self.peek(1) == '|':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.OR, '||', self.line))
                continue
            
            # Single-character tokens
            char = self.peek()
            if char == '=':
                self.tokens.append(Token(TokenType.ASSIGN, self.advance(), self.line))
            elif char == '+':
                self.tokens.append(Token(TokenType.PLUS, self.advance(), self.line))
            elif char == '-':
                self.tokens.append(Token(TokenType.MINUS, self.advance(), self.line))
            elif char == '*':
                self.tokens.append(Token(TokenType.MULTIPLY, self.advance(), self.line))
            elif char == '/':
                self.tokens.append(Token(TokenType.DIVIDE, self.advance(), self.line))
            elif char == '%':
                self.tokens.append(Token(TokenType.MODULO, self.advance(), self.line))
            elif char == '<':
                self.tokens.append(Token(TokenType.LESS, self.advance(), self.line))
            elif char == '>':
                self.tokens.append(Token(TokenType.GREATER, self.advance(), self.line))
            elif char == '!':
                self.tokens.append(Token(TokenType.NOT, self.advance(), self.line))
            elif char == '(':
                self.tokens.append(Token(TokenType.LPAREN, self.advance(), self.line))
            elif char == ')':
                self.tokens.append(Token(TokenType.RPAREN, self.advance(), self.line))
            elif char == '{':
                self.tokens.append(Token(TokenType.LBRACE, self.advance(), self.line))
            elif char == '}':
                self.tokens.append(Token(TokenType.RBRACE, self.advance(), self.line))
            elif char == ';':
                self.tokens.append(Token(TokenType.SEMICOLON, self.advance(), self.line))
            elif char == ',':
                self.tokens.append(Token(TokenType.COMMA, self.advance(), self.line))
            else:
                self.error(f"Unexpected character: {char}")
        
        self.tokens.append(Token(TokenType.EOF, None, self.line))
        return self.tokens