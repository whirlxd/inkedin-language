from language.tokentype import TokenType
from typing import Any

class Token:
    def __init__(self, type_: TokenType, value: Any, line: int = 0): # type: ignore
        self.type = type_      
        self.value = value   
        self.line = line       
    
    def __repr__(self):
        return f"Token({self.type}, {self.value})"