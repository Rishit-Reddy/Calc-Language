import sys
from Lexer import tokenize
from SyntaxAnalyser import Parser
from Interpreter import Interpreter

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <expression>")
        return

    expression = sys.argv[1]

    # Step 1: Lexical Analysis
    tokens = tokenize(expression)

    # Step 2: Parsing
    parser = Parser(tokens)
    try:
        ast = parser.parse()
    except Exception as e:
        print(f"Syntax Error: {e}")
        return

    # Step 3: Interpretation
    interpreter = Interpreter()
    try:
        result = interpreter.visit(ast)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Runtime Error: {e}")

if __name__ == "__main__":
    main()
