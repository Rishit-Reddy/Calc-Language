from Lexer import TokenType, Token, tokenize
from SyntaxAnalyser import AST, Num, BinOp, Parser

class Interpreter:
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')

    def visit_Num(self, node):
        return node.value

    def visit_BinOp(self, node):
        if node.op.type == TokenType.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == TokenType.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == TokenType.MULTIPLY:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == TokenType.DIVIDE:
            return self.visit(node.left) / self.visit(node.right)
        else:
            raise Exception(f"Unsupported binary operator: {node.op.type}")

# Integrating lexer, parser, and interpreter
if __name__ == "__main__":
    test_cases = [
        "3 + 7",
        "3 + 7 * 2",
        "10 / (2 + 3)",
        "(10 - 4) * 2)"
    ]

    for text in test_cases:
        print(f"Testing: {text}")
        tokens = tokenize(text)
        parser = Parser(tokens)
        try:
            ast = parser.parse()
            interpreter = Interpreter()
            result = interpreter.visit(ast)
            print("Result:", result)
        except Exception as e:
            print("Error:", e)
        print()
