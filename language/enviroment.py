from typing import Dict, Any, Optional
from language.errors import RuntimeError

class Environment:
    def __init__(self, parent: Optional['Environment'] = None):
        self.parent = parent       
        self.variables: Dict[str, Any] = {}  # store user vars
    
    def define(self, name: str, value: Any):
     
        self.variables[name] = value
    
    def get(self, name: str) -> Any:
     
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.get(name) 
        raise RuntimeError(f"Undefined variable: {name}")
    
    def assign(self, name: str, value: Any):
        
        if name in self.variables:
            self.variables[name] = value
            return
        if self.parent:
            self.parent.assign(name, value)  # Try parent scope
            return
        raise RuntimeError(f"Undefined variable: {name}")
