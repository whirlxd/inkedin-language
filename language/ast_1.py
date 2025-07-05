from typing import List, Any, Optional
from language.tokentype import TokenType



class ASTNode:
    pass  


class Program(ASTNode): # root
    def __init__(self, statements: List[ASTNode]):
        self.statements = statements  


class VarDecl(ASTNode):
    def __init__(self, name: str, value: ASTNode):
        self.name = name     
        self.value = value   


class FuncDecl(ASTNode):
    def __init__(self, name: str, params: List[str], body: List[ASTNode]):
        self.name = name    
        self.params = params  
        self.body = body     


class If(ASTNode):
    def __init__(self, condition: ASTNode, then_branch: List[ASTNode], else_branch: Optional[List[ASTNode]] = None):
        self.condition = condition   
        self.then_branch = then_branch 
        self.else_branch = else_branch 


class While(ASTNode):
    def __init__(self, condition: ASTNode, body: List[ASTNode]):
        self.condition = condition 
        self.body = body          
class For(ASTNode):
    def __init__(self, init: ASTNode, condition: ASTNode, update: ASTNode, body: List[ASTNode]):
        self.init = init           
        self.condition = condition 
        self.update = update                    
        self.body = body                  

class Return(ASTNode):
    def __init__(self, value: Optional[ASTNode] = None):
        self.value = value 


class Break(ASTNode):
    pass  


class Continue(ASTNode):
    pass 


class Try(ASTNode):
    def __init__(self, try_block: List[ASTNode], catch_block: List[ASTNode]):
        self.try_block = try_block     
        self.catch_block = catch_block


class Assignment(ASTNode):
    def __init__(self, name: str, value: ASTNode):
        self.name = name    
        self.value = value  

class BinaryOp(ASTNode):
    def __init__(self, left: ASTNode, operator: TokenType, right: ASTNode):
        self.left = left        
        self.operator = operator 
        self.right = right      

# Unary operations: "-x", "!condition"
class UnaryOp(ASTNode):
    def __init__(self, operator: TokenType, operand: ASTNode):
        self.operator = operator #
        self.operand = operand   


class FuncCall(ASTNode):
    def __init__(self, name: str, args: List[ASTNode]):
        self.name = name  
        self.args = args  

class Identifier(ASTNode):
    def __init__(self, name: str):
        self.name = name  

class Literal(ASTNode):
    def __init__(self, value: Any):
        self.value = value 

class Import(ASTNode):
    def __init__(self, filepath: str):
        self.filepath = filepath  