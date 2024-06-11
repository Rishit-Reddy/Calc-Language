from Lexer import TokenType, Token, tokenize

class AST:
    pass

class Num(AST):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Num({self.value})"

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"BinOp({self.left}, {self.op}, {self.right})"

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = tokens[self.current_token_index]
        self.paren_stack = []

    def eat(self, token_type):
        if self.current_token.type == token_type:
            if token_type == TokenType.LPAREN:
                self.paren_stack.append(token_type)
            elif token_type == TokenType.RPAREN:
                if not self.paren_stack:
                    self.error("Mismatched parentheses: unexpected ')'")
                self.paren_stack.pop()
            self.current_token_index += 1
            if self.current_token_index < len(self.tokens):
                self.current_token = self.tokens[self.current_token_index]
            else:
                self.current_token = Token(TokenType.EOF)
        else:
            self.error(f"Expected token {token_type}, got {self.current_token.type}")

    def error(self, message):
        raise Exception(f"Syntax error: {message}")

    def factor(self):
        """factor : INTEGER | LPAREN expr RPAREN"""
        token = self.current_token
        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return Num(token.value)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            if self.current_token.type != TokenType.RPAREN:
                self.error("Mismatched parentheses")
            self.eat(TokenType.RPAREN)
            return node
        self.error('Invalid syntax in factor')

    def term(self):
        """term : factor ((MUL | DIV) factor)*"""
        node = self.factor()
        while self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            token = self.current_token
            if token.type == TokenType.MULTIPLY:
                self.eat(TokenType.MULTIPLY)
            elif token.type == TokenType.DIVIDE:
                self.eat(TokenType.DIVIDE)
            node = BinOp(left=node, op=token, right=self.factor())
        return node

    def expr(self):
        """expr : term ((PLUS | MINUS) term)*"""
        node = self.term()
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
            node = BinOp(left=node, op=token, right=self.term())
        return node

    def parse(self):
        ast = self.expr()
        if self.current_token.type != TokenType.EOF:
            self.error(f"Unexpected token {self.current_token.type}")
        if self.paren_stack:
            self.error("Mismatched parentheses: missing ')'")
        return ast

if __name__ == "__main__":
    # Test cases
    test_cases = [
        "(3 + 7)",
        "(3 + 7))",
        "(3 + 7",
        "((3 + 7))"
    ]

    for text in test_cases:
        print(f"Testing: {text}")
        tokens = tokenize(text)
        parser = Parser(tokens)
        try:
            ast = parser.parse()
            print("AST:", ast)
        except Exception as e:
            print("Error:", e)
        print()
