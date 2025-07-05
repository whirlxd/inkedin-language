from language.enviroment import Environment
from language.ast_1 import FuncDecl

class Function:
    def __init__(self, declaration: FuncDecl, closure: Environment):
        self.declaration = declaration  
        self.closure = closure       # defined env