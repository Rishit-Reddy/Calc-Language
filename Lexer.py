from enum import Enum, auto

class TokenType(Enum):
    NUMBER = auto()
    PLUS = auto()
    MINUS = auto()
    DIVIDE = auto()
    MULTIPLY = auto()
    LPAREN = auto()
    RPAREN = auto()
    EOF = auto()

class Token:
    def __init__(self, type, value=None) -> None:
        self.value = value
        self.type = type

    def __repr__(self) -> str:
        return f"Token({self.type}, {repr(self.value)})"

class Lexer:
    def __init__(self, text) -> None:
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if text else None

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None 
    
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def number(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return Token(TokenType.NUMBER, int(result))
    
    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
             
            if self.current_char.isdigit():
                return self.number()
            
            if self.current_char == '+':
                self.advance()
                return Token(TokenType.PLUS, '+')
            
            if self.current_char == '-':
                self.advance()
                return Token(TokenType.MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(TokenType.MULTIPLY, '*')
            
            if self.current_char == '/':
                self.advance()
                return Token(TokenType.DIVIDE, '/')
            
            if self.current_char == '(':
                self.advance()
                return Token(TokenType.LPAREN, ')')
            
            if self.current_char == ')':
                self.advance()
                return Token(TokenType.RPAREN, ')')

            raise Exception(f"Unexpected character: {self.current_char}")
        
        return Token(TokenType.EOF)

def tokenize(text):
    lexer = Lexer(text)
    tokens = []
    token = lexer.get_next_token()
    while token.type != TokenType.EOF:
        tokens.append(token)
        token = lexer.get_next_token()
    tokens.append(token)  # Add the EOF token
    return tokens

if __name__ == "__main__":
    text = "3+5"
    tokens = tokenize(text)
    print(tokens)
