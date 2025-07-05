from typing import List, Optional
from language.tokentype import TokenType
from language.tokn import Token
from language.errors import ParseError
from language.ast_1 import ASTNode, Program, VarDecl, FuncDecl, If, While, For, Return, Break, Continue, Try, Assignment, BinaryOp, UnaryOp, FuncCall, Identifier, Literal, Import
# advance is consuming the token and moving to the next one
class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens  # initalize
        self.pos = 0        
    
    def error(self, message: str):
      # handle unexpected token
        current = self.current_token()
        raise ParseError(f"Line {current.line}: {message}")
    
    def current_token(self) -> Token:
        
        if self.pos >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[self.pos]
    
    def advance(self) -> Token:
        # Move to the next token and return the current one
        token = self.current_token()
        if token.type != TokenType.EOF:
            self.pos += 1
        return token
    
    def match(self, *types: TokenType) -> bool:

        return self.current_token().type in types
    
    def consume(self, type_: TokenType, message: str) -> Token:
       
        if self.current_token().type == type_:
            return self.advance()
        self.error(message)
    
    def skip_newlines(self):
   
        while self.match(TokenType.NEWLINE):
            self.advance()
    
    def parse(self) -> Program:
# map to ast
        statements = []
        self.skip_newlines()
        
        while not self.match(TokenType.EOF):
            stmt = self.statement()
            if stmt:
                statements.append(stmt)
            self.skip_newlines()
        
        return Program(statements)
    
    def statement(self) -> Optional[ASTNode]:
     # map to ast
        if self.match(TokenType.NETWORK):
            return self.import_statement()
        elif self.match(TokenType.CONNECT):
            return self.var_declaration()
        elif self.match(TokenType.THOUGHTS):
            return self.func_declaration()
        elif self.match(TokenType.PIVOT):
            return self.if_statement()
        elif self.match(TokenType.SYNERGY):
            return self.while_statement()
        elif self.match(TokenType.LEVERAGE):
            return self.for_statement()
        elif self.match(TokenType.REACH_OUT):
            return self.return_statement()
        elif self.match(TokenType.DISRUPT):
            self.advance()
            self.consume(TokenType.SEMICOLON, "Expected ';' after 'disrupt'")
            return Break()
        elif self.match(TokenType.SCALE):
            self.advance()
            self.consume(TokenType.SEMICOLON, "Expected ';' after 'scale'")
            return Continue()
        elif self.match(TokenType.GAME_CHANGER):
            return self.try_statement()
        elif self.match(TokenType.LBRACE):
            return self.block_statement()
        else:
            return self.expression_statement()
    
    def import_statement(self) -> Import:
        
        self.advance() 
        filepath = self.consume(TokenType.STRING, "Expected file path after 'network'").value
        self.consume(TokenType.SEMICOLON, "Expected ';' after import")
        return Import(filepath)
    
    def var_declaration(self) -> VarDecl:
       
        self.advance()  
        name = self.consume(TokenType.IDENTIFIER, "Expected variable name").value
        self.consume(TokenType.ASSIGN, "Expected '=' after variable name")
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after variable declaration")
        return VarDecl(name, value)
    
    def func_declaration(self) -> FuncDecl:
    
        self.advance() 
        name = self.consume(TokenType.IDENTIFIER, "Expected function name").value
        self.consume(TokenType.LPAREN, "Expected '(' after function name")
        

        params = []
        if not self.match(TokenType.RPAREN):
            params.append(self.consume(TokenType.IDENTIFIER, "Expected parameter name").value)
            while self.match(TokenType.COMMA):
                self.advance()
                params.append(self.consume(TokenType.IDENTIFIER, "Expected parameter name").value)
        
        self.consume(TokenType.RPAREN, "Expected ')' after parameters")
        body = self.block_statement()
        return FuncDecl(name, params, body.statements if hasattr(body, 'statements') else [body])
    
    def if_statement(self) -> If:
 
        self.advance() 
        self.consume(TokenType.LPAREN, "Expected '(' after 'pivot'")
        condition = self.expression()
        self.consume(TokenType.RPAREN, "Expected ')' after condition")
        
        then_branch = self.statement()
        then_statements = then_branch.statements if hasattr(then_branch, 'statements') else [then_branch]
     
        else_statements = None
        if self.match(TokenType.CIRCLE_BACK):
            self.advance()
            else_branch = self.statement()
            else_statements = else_branch.statements if hasattr(else_branch, 'statements') else [else_branch]
        
        return If(condition, then_statements, else_statements)
    
    def while_statement(self) -> While:
        self.advance()  
        self.consume(TokenType.LPAREN, "Expected '(' after 'synergy'")
        condition = self.expression()
        self.consume(TokenType.RPAREN, "Expected ')' after condition")
        body = self.statement()
        body_statements = body.statements if hasattr(body, 'statements') else [body]
        return While(condition, body_statements)
    
    def for_statement(self) -> For:
     
        self.advance() 
        self.consume(TokenType.LPAREN, "Expected '(' after 'leverage'")
        
        init = None
        if self.match(TokenType.CONNECT):
          
            init = self.var_declaration()
        elif not self.match(TokenType.SEMICOLON):
            init = self.expression_statement()
        else:
            self.advance()  # consume ';'
        
        condition = self.expression() if not self.match(TokenType.SEMICOLON) else Literal(True)
        self.consume(TokenType.SEMICOLON, "Expected ';' after for condition")
        
        update = self.expression() if not self.match(TokenType.RPAREN) else None
        self.consume(TokenType.RPAREN, "Expected ')' after for clauses")
        
        body = self.statement()
        body_statements = body.statements if hasattr(body, 'statements') else [body]
        return For(init, condition, update, body_statements)
    
    def return_statement(self) -> Return:
      
        self.advance() 
        value = None
        if not self.match(TokenType.SEMICOLON):
            value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after return")
        return Return(value)
    
    def try_statement(self) -> Try:
  
        self.advance()  
        try_block = self.block_statement()
        self.consume(TokenType.LESSONS_LEARNED, "Expected 'lessons_learned' after try block")
        catch_block = self.block_statement()
        
        try_statements = try_block.statements if hasattr(try_block, 'statements') else [try_block]
        catch_statements = catch_block.statements if hasattr(catch_block, 'statements') else [catch_block]
        return Try(try_statements, catch_statements)
    
    def block_statement(self):
     
        self.consume(TokenType.LBRACE, "Expected '{'")
        statements = []
        self.skip_newlines()
        
        while not self.match(TokenType.RBRACE) and not self.match(TokenType.EOF):
            stmt = self.statement()
            if stmt:
                statements.append(stmt)
            self.skip_newlines()
        
        self.consume(TokenType.RBRACE, "Expected '}'")
        return type('Block', (), {'statements': statements})()
    
    def expression_statement(self) -> Optional[ASTNode]:
  
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after expression")
        return expr
    
 # set order so that weird calcs dont happen. i thought it would be pemdas but alas 
    
    def expression(self) -> ASTNode:
        return self.assignment()
    
    def assignment(self) -> ASTNode:
    
        expr = self.logical_or()
        
        if self.match(TokenType.ASSIGN):
            self.advance()
            value = self.assignment()
            if isinstance(expr, Identifier):
                return Assignment(expr.name, value)
            self.error("Invalid assignment target")
        
        return expr
    
    def logical_or(self) -> ASTNode:
      
        expr = self.logical_and()
        
        while self.match(TokenType.OR):
            operator = self.advance().type
            right = self.logical_and()
            expr = BinaryOp(expr, operator, right)
        
        return expr
    
    def logical_and(self) -> ASTNode:
     
        expr = self.equality()
        
        while self.match(TokenType.AND):
            operator = self.advance().type
            right = self.equality()
            expr = BinaryOp(expr, operator, right)
        
        return expr
    
    def equality(self) -> ASTNode:
     
        expr = self.comparison()
        
        while self.match(TokenType.EQUALS, TokenType.NOT_EQUALS):
            operator = self.advance().type
            right = self.comparison()
            expr = BinaryOp(expr, operator, right)
        
        return expr
    
    def comparison(self) -> ASTNode:

        expr = self.addition()
        
        while self.match(TokenType.LESS, TokenType.GREATER, TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL):
            operator = self.advance().type
            right = self.addition()
            expr = BinaryOp(expr, operator, right)
        
        return expr
    
    def addition(self) -> ASTNode:
        # Handle "+" and "-"
        expr = self.multiplication()
        
        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.advance().type
            right = self.multiplication()
            expr = BinaryOp(expr, operator, right)
        
        return expr
    
    def multiplication(self) -> ASTNode:
   
        expr = self.unary()
        
        while self.match(TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            operator = self.advance().type
            right = self.unary()
            expr = BinaryOp(expr, operator, right)
        
        return expr
    
    def unary(self) -> ASTNode:
   
        if self.match(TokenType.MINUS, TokenType.NOT):
            operator = self.advance().type
            expr = self.unary()
            return UnaryOp(operator, expr)
        
        return self.call()
    
    def call(self) -> ASTNode:

        expr = self.primary()
        
        while self.match(TokenType.LPAREN):
            self.advance()
            args = []
            if not self.match(TokenType.RPAREN):
                args.append(self.expression())
                while self.match(TokenType.COMMA):
                    self.advance()
                    args.append(self.expression())
            
            self.consume(TokenType.RPAREN, "Expected ')' after arguments")
            
            if isinstance(expr, Identifier):
                expr = FuncCall(expr.name, args)
            else:
                self.error("Can only call functions")
        
        return expr
    
    def primary(self) -> ASTNode:
 
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.advance().value)
        
        if self.match(TokenType.BOOLEAN):
            value = self.advance().value == 'true'
            return Literal(value)
        
        if self.match(TokenType.IDENTIFIER):
            return Identifier(self.advance().value)
        
        if self.match(TokenType.LPAREN):
            self.advance()
            expr = self.expression()
            self.consume(TokenType.RPAREN, "Expected ')' after expression")
            return expr
        
        self.error("Expected expression")
