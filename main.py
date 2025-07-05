

from language.errors import LexerError, ParseError, RuntimeError
from language.interpreter import Interpreter
from language.lexer import Lexer
from language.parser import Parser

def interpret(source_code: str):
    """
 tokenize , parse and execute
    """
    try:
    #   lexing
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        
    #    token to tree
        parser = Parser(tokens)
        ast = parser.parse()
        
    #     interpretation
        interpreter = Interpreter()
        interpreter.interpret(ast)
        
    except (LexerError, ParseError, RuntimeError) as e:
        print(f"An Error Occurred: {e}")


