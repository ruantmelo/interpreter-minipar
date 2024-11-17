import ply.lex as lex
from interfaces.interface_lexer import ILexer


class Lexer(ILexer):
    def __init__(self):
        
        self.lexer = None
        
        self.program = ""
        
        self.reserved = {
            'if' : 'IF',
            'else' : 'ELSE',
            'while' : 'WHILE',
            'true' : 'TRUE',
            'false' : 'FALSE',
            'int' : 'INT',
            'bool' : 'BOOL',
            'string' : 'STRING',
            'chan' : 'CHANNEL',
            'SEQ' : 'SEQ_BLOCK',
            'PAR' : 'PAR_BLOCK',
            'input' : 'INPUT',
            'output' : 'OUTPUT',
            'send' : 'SEND',
            'receive' : 'RECEIVE'
        }
        
        # List of token names.   This is always required
        self.tokens = (
            'ID',
            'DIGIT',
            'PLUS',
            'STRING_VALUE',
            'MINUS',
            'TIMES',
            'DIVIDE',
            'LPAREN',
            'RPAREN',
            'G_THAN',
            'GE_THAN',
            'L_THAN',
            'LE_THAN',
            'EQUAL',
            'NOT_EQUAL',
            'ASSIGN',
            'LBRACE',
            'RBRACE',
            'DOT',
            'COMMA',
        ) + tuple(self.reserved.values())

    # Regular expression rules for simple tokens
    t_EQUAL = r'=='
    t_NOT_EQUAL = r'!='
    t_LE_THAN = r'<='
    t_GE_THAN = r'>='
    t_PLUS   = r'\+'
    t_MINUS  = r'-'
    t_TIMES  = r'\*'
    t_DIVIDE = r'/'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_G_THAN = r'>'
    t_L_THAN = r'<'
    t_ASSIGN = r'='
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_DOT = r'\.'
    t_COMMA = r','

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
       
        t.type = self.reserved.get(t.value,'ID')    # Check for reserved words
        
        if (t.type == 'TRUE'):
            t.value = True
        elif (t.type == "FALSE"):
            t.value = False
        
        return t

    # A regular expression rule with some action code
    # Note addition of self parameter since we're in a class
    def t_DIGIT(self,t):
        r'\d+'
        t.value = int(t.value)
        t.type = 'DIGIT'
        return t
    
    def t_STRING_VALUE(self,t):
        r'"[^"]*"'  
        return t

    # Define a rule so we can track line numbers
    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore  = ' '

    # Error handling rule
    def t_error(self,t):
        column = self.find_column(input=self.program, token=t)
        print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno} column {column}")
        t.lexer.skip(1)

    def find_column(self, input, token):
      line_start = input.rfind('\n', 0, token.lexpos) + 1
      return (token.lexpos - line_start) + 1

    # Build the lexer
    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
    
    # Test it output
    def test(self,data):
        self.program = data
        self.lexer.input(data)
        while True:
             tok = self.lexer.token()
             if not tok: 
                 break
             print(tok)

m = Lexer()
m.build() 

if __name__ == '__main__':
  file_path = 'examples/test.mp'
  with open(file_path, 'r') as file:
    program = file.read()
    m.test(program) 
  