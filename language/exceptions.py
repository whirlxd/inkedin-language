from typing import Any
class BreakException(Exception):
    pass  

class ContinueException(Exception):
    pass  
class ReturnException(Exception):
    def __init__(self, value: Any):
        self.value = value  