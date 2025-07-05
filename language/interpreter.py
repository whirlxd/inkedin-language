import os
from typing import List, Any, Dict
from language.tokentype import TokenType
from language.errors import RuntimeError
from language.enviroment import Environment
from language.exceptions import BreakException, ContinueException, ReturnException
from language.function import Function
from language.ast_1 import ASTNode, Program, VarDecl, FuncDecl, If, While, For, Return, Break, Continue, Try, Assignment, BinaryOp, UnaryOp, FuncCall, Identifier, Literal, Import

class Interpreter:
    def __init__(self):
        self.globals = Environment()    
        self.environment = self.globals  
        self.imported_modules: Dict[str, Environment] = {} 
        
     
        self.globals.define("announce", self.builtin_print) 
        self.globals.define("input", self.builtin_input)     
        self.globals.define("str", self.builtin_str)        
        self.globals.define("num", self.builtin_num)        
        self.globals.define("len", self.builtin_len)        
   
    def builtin_print(self, *args):
       
        output = " ".join(str(arg) for arg in args)
        print(output)
        return None
    
    def builtin_input(self, prompt=""):
    
        return input(str(prompt))
    
    def builtin_str(self, value):
      
        return str(value)
    
    def builtin_num(self, value):
       
        try:
            if isinstance(value, str):
                if '.' in value:
                    return float(value)
                return int(value)
            return float(value)
        except (ValueError, TypeError):
            raise RuntimeError(f"Cannot convert {value} to number")
    
    def builtin_len(self, value):
     
        if isinstance(value, str):
            return len(value)
        raise RuntimeError(f"Cannot get length of {type(value)}")
    
    def interpret(self, program: Program):
       
        try:
            for statement in program.statements:
                self.execute(statement)
        except ReturnException:
            pass 
    
    def execute(self, node: ASTNode) -> Any:
     
        if isinstance(node, Import):
          
            return self.execute_import(node)
        elif isinstance(node, Program):
      
            for statement in node.statements:
                self.execute(statement)
        
        elif isinstance(node, VarDecl):
           
            value = self.evaluate(node.value)
            self.environment.define(node.name, value)
        
        elif isinstance(node, FuncDecl):
      
            function = Function(node, self.environment)
            self.environment.define(node.name, function)
        
        elif isinstance(node, If):
            
            condition = self.evaluate(node.condition)
            if self.is_truthy(condition):
                for stmt in node.then_branch:
                    self.execute(stmt)
            elif node.else_branch:
                for stmt in node.else_branch:
                    self.execute(stmt)
        
        elif isinstance(node, While):
           
            try:
                while self.is_truthy(self.evaluate(node.condition)):
                    try:
                        for stmt in node.body:
                            self.execute(stmt)
                    except ContinueException:
                        continue 
                    except BreakException:
                        break  
            except BreakException:
                pass  
        
        elif isinstance(node, For):
        
            try:
                if node.init:
                    self.execute(node.init)  
                
                while True:
                    if not self.is_truthy(self.evaluate(node.condition)):
                        break 
                    
                    try:
                        for stmt in node.body:
                            self.execute(stmt) 
                    except ContinueException:
                        pass  
                    except BreakException:
                        break 
                    
                    if node.update:
                        self.evaluate(node.update)  
            except BreakException:
                pass  
        
        elif isinstance(node, Return):
        
            value = None
            if node.value:
                value = self.evaluate(node.value)
            raise ReturnException(value) 
        
        elif isinstance(node, Break):
        
            raise BreakException()
        
        elif isinstance(node, Continue):
          
            raise ContinueException()
        
        elif isinstance(node, Try):
      
            try:
                for stmt in node.try_block:
                    self.execute(stmt)
            except Exception:
           
                for stmt in node.catch_block:
                    self.execute(stmt)
        
        elif isinstance(node, Assignment):
           
            value = self.evaluate(node.value)
            self.environment.assign(node.name, value)
        
        else:
         
            return self.evaluate(node)
    
    def evaluate(self, node: ASTNode) -> Any:
     
        if isinstance(node, Literal):
          
            return node.value
        
        elif isinstance(node, Identifier):
          
            return self.environment.get(node.name)
        
        elif isinstance(node, BinaryOp):
          
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
     
            if node.operator == TokenType.PLUS:
                return left + right
            elif node.operator == TokenType.MINUS:
                return left - right
            elif node.operator == TokenType.MULTIPLY:
                return left * right
            elif node.operator == TokenType.DIVIDE:
                if right == 0:
                    raise RuntimeError("Division by zero")  
                return left / right
            elif node.operator == TokenType.MODULO:
                return left % right
            elif node.operator == TokenType.EQUALS:
                return left == right
            elif node.operator == TokenType.NOT_EQUALS:
                return left != right
            elif node.operator == TokenType.LESS:
                return left < right
            elif node.operator == TokenType.GREATER:
                return left > right
            elif node.operator == TokenType.LESS_EQUAL:
                return left <= right
            elif node.operator == TokenType.GREATER_EQUAL:
                return left >= right
            elif node.operator == TokenType.AND:
                return self.is_truthy(left) and self.is_truthy(right)
            elif node.operator == TokenType.OR:
                return self.is_truthy(left) or self.is_truthy(right)
        
        elif isinstance(node, UnaryOp):
        
            operand = self.evaluate(node.operand)
            
            if node.operator == TokenType.MINUS:
                return -operand 
            elif node.operator == TokenType.NOT:
                return not self.is_truthy(operand)  # NOT
        
        elif isinstance(node, FuncCall):
           
            function = self.environment.get(node.name)
            args = [self.evaluate(arg) for arg in node.args]
            
            if callable(function): 
                return function(*args)
            elif isinstance(function, Function):
                return self.call_function(function, args)
            else:
                raise RuntimeError(f"{node.name} is not a function")
        
        elif isinstance(node, Assignment):
   
            value = self.evaluate(node.value)
            self.environment.assign(node.name, value)
            return value
        
        return None
    
    def call_function(self, function: Function, args: List[Any]) -> Any:
  
        if len(args) != len(function.declaration.params):
            raise RuntimeError(f"Expected {len(function.declaration.params)} arguments but got {len(args)}")
        
      
        env = Environment(function.closure)
      
        for param, arg in zip(function.declaration.params, args):
            env.define(param, arg)
        
       
        previous = self.environment
        try:
            self.environment = env
            
            for stmt in function.declaration.body:
                self.execute(stmt)
        except ReturnException as ret:
            return ret.value  
        finally:
            self.environment = previous  
        
        return None 
    
    def is_truthy(self, value: Any) -> bool:

        if value is None or value is False:
            return False
        if isinstance(value, (int, float)) and value == 0:
            return False  
        if isinstance(value, str) and value == "":
            return False 
        return True 
    
    def execute_import(self, node: Import) -> None:
      
        filepath = node.filepath
        
      
        if filepath in self.imported_modules:
        
            imported_env = self.imported_modules[filepath]
            for name, value in imported_env.variables.items():
                self.environment.define(name, value)
            return
        
        # Resolve file path
        if not filepath.endswith('.lnk'):
           raise RuntimeError("Import file must have .lnk extension")
        
        if not os.path.isabs(filepath):
         
            filepath = os.path.abspath(filepath)
        
        if not os.path.exists(filepath):
            raise RuntimeError(f"Cannot find file to import: {filepath}")
        
 
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
         
            from language.lexer import Lexer
            from language.parser import Parser
            
          
            lexer = Lexer(source_code)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            ast = parser.parse()
            
           
            module_env = Environment(self.globals)
            
          
            previous_env = self.environment
            self.environment = module_env
            
            try:
               
                for statement in ast.statements:
                    self.execute(statement)
                
              # cache module to avoid recursive issues
                self.imported_modules[node.filepath] = module_env
                
               # load from cache
                for name, value in module_env.variables.items():
                    previous_env.define(name, value)
                
            finally:
                self.environment = previous_env
                
        except Exception as e:
            raise RuntimeError(f"Error importing {filepath}: {str(e)}")
