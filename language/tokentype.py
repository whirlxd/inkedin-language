from enum import Enum, auto

# 📝 LANGUAGE CUSTOMIZATION GUIDE - BY AI for Contributors 📝
# Want to change the LinkedIn buzzwords to something else? Here's your roadmap! 🗺️
#
# 🎯 CHANGING KEYWORDS (like 'connect' to 'declare' or 'pivot' to 'if'):
# 1. Update the enum value name here (e.g., CONNECT -> DECLARE)
# 2. Go to lexer.py and update the keywords dictionary
#    Change: 'connect': TokenType.CONNECT  →  'declare': TokenType.DECLARE
# 3. Update parser.py method names and logic if needed
#    Change: self.match(TokenType.CONNECT)  →  self.match(TokenType.DECLARE)
# 4. No changes needed in interpreter.py (it works with AST nodes, not tokens)
#
# 🎯 CHANGING OPERATORS (like '=' to 'equals' or '+' to 'plus'):
# 1. Keep the enum name the same (ASSIGN, PLUS, etc.) - only change what triggers it
# 2. Go to lexer.py and modify the tokenize() method:
#    - For single chars: change the elif char == '=' condition
#    - For words: add to keywords dictionary and remove from single char section
# 3. Parser.py and interpreter.py will work unchanged (they use TokenType.ASSIGN, not '=')
#
# 🎯 CHANGING BRACKETS/PUNCTUATION (like {} to () for blocks):
# ⚠️  HIGH IMPACT CHANGE - affects multiple files:
# 1. Update token types here (maybe rename LBRACE/RBRACE to LBLOCK/RBLOCK)
# 2. Update lexer.py character recognition
# 3. Update parser.py in ALL block-related methods (block_statement, if_statement, etc.)
# 4. Consider context: do you want () for BOTH function calls AND blocks?
#
# 🎯 CHANGING BOOLEAN VALUES ('true'/'false' to 'yes'/'no'):
# 1. Go to lexer.py keywords dictionary
# 2. Change: 'true': TokenType.BOOLEAN  →  'yes': TokenType.BOOLEAN
# 3. Update parser.py primary() method boolean parsing logic
# 4. Keep interpreter.py truthiness logic the same
#
# 🎯 ADDING NEW KEYWORDS:
# 1. Add new enum value here (e.g., NEW_KEYWORD = auto())
# 2. Add to lexer.py keywords dictionary
# 3. Add parsing logic in parser.py statement() method
# 4. Add execution logic in interpreter.py execute() method
# 5. Create new AST node in ast_1.py if needed
#
# 💡 PRO TIP: Test changes incrementally! Change one thing at a time and run main.py
# 🔧 DIFFICULTY LEVELS:
# Easy: Keywords, boolean values, string operators
# Medium: Math operators, adding new features  
# Hard: Punctuation, brackets, syntax structure changes

class TokenType(Enum):

    CONNECT = auto()        # variable declaration (like "let" or "var" in other languages)
    THOUGHTS = auto()       # function declaration (instead of "function" - very LinkedIn!)
    NETWORK = auto()        # import statement (because we're building our network!)
    PIVOT = auto()          # if statement (because everything is a pivot in business!)
    CIRCLE_BACK = auto()    # else (we'll circle back on this later...)
    SYNERGY = auto()        # while loop (creating synergy through repetition!)
    LEVERAGE = auto()       # for loop (leveraging our iteration power!)
    DISRUPT = auto()        # break (disrupting the status quo of loops!)
    SCALE = auto()          # continue (scaling to the next iteration!)
    REACH_OUT = auto()      # return (reaching out with our result!)
    GAME_CHANGER = auto()   # try (this could be a real game changer!)
    LESSONS_LEARNED = auto() # catch (turning failures into lessons learned!)
    
    # Math and comparison stuff - the bread and butter of programming
    ASSIGN = auto()         # = (giving a value to something)
    PLUS = auto()           # + (adding stuff together)
    MINUS = auto()          # - (taking stuff away)
    MULTIPLY = auto()       # * (making things bigger!)
    DIVIDE = auto()         # / (splitting things up)
    MODULO = auto()         # % (getting the leftover after division)
    EQUALS = auto()         # == (checking if two things are the same)
    NOT_EQUALS = auto()     # != (checking if two things are different)
    LESS = auto()           # < (is this smaller than that?)
    GREATER = auto()        # > (is this bigger than that?)
    LESS_EQUAL = auto()     # <= (smaller or equal)
    GREATER_EQUAL = auto()  # >= (bigger or equal)
    AND = auto()            # && (both things must be true)
    OR = auto()             # || (at least one thing must be true)
    NOT = auto()            # ! (flip true to false or vice versa)
    
    # Punctuation marks - like grammar for our code
    LPAREN = auto()         # ( (left parenthesis)
    RPAREN = auto()         # ) (right parenthesis)
    LBRACE = auto()         # { (left curly brace - starts a block)
    RBRACE = auto()         # } (right curly brace - ends a block)
    SEMICOLON = auto()      # ; (end of a statement - like a period)
    COMMA = auto()          # , (separating things in a list)
    
    # Different types of values our language can handle
    NUMBER = auto()         # 42, 3.14, etc.
    STRING = auto()         # "Hello world", "LinkedIn is amazing", etc.
    BOOLEAN = auto()        # true or false
    IDENTIFIER = auto()     # Variable names, function names, etc.
    
    # Special control characters
    NEWLINE = auto()        # When you hit Enter
    EOF = auto()            # End of file - we're done reading!