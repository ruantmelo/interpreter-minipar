import ply.lex as lex

class MyLexer():
    lexer = None
    
    program = ""
    
    reserved = {
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
    }
    
    # List of token names.   This is always required
    tokens = (
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
    ) + tuple(reserved.values())

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


    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value,'ID')    # Check for reserved words
        return t

    # A regular expression rule with some action code
    # Note addition of self parameter since we're in a class
    def t_DIGIT(self,t):
        r'\d+'
        t.value = int(t.value)    
        return t
    
    def t_STRING_VALUE(self,t):
        r'"[^"]*"'
        t.value = t.value[1:-1]    
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
    
    # Test it output
    def test(self,data):
        self.program = data
        self.lexer.input(data)
        while True:
             tok = self.lexer.token()
             if not tok: 
                 break
             print(tok)


if __name__ == '__main__':
  file_path = 'examples/test.mp'
  with open(file_path, 'r') as file:
    program = file.read()
    m = MyLexer()
    m.build()           # Build the lexer
    m.test(program) 
  