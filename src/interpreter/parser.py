from interfaceparser import IParser
import logging
import ply.yacc as yacc




logging.basicConfig(
    level = logging.DEBUG,
    filename = "parselog.txt",
    filemode = "w",
    format = "%(filename)10s:%(lineno)4d:%(message)s"
)
log = logging.getLogger()

class Parser(IParser):
    
    def __init__(self):
        from lexer import Lexer
        self.lexer = Lexer()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self)

    def parsing(self, program):
        result = self.parser.parse(program, debug=log)
        return result
    
    def p_stmt_block(self, p):
        '''stmt_block : seq_stmts
                    | par_stmts
                    | stmt_block seq_stmts
                    | stmt_block par_stmts'''
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 3:
            p[0] = (p[1], p[2])

    def p_seq_stmts(self, p):
        'seq_stmts : SEQ_BLOCK stmts'
        p[0] = ('seqBlock', p[2])

    def p_par_block(self, p):
        'par_stmts : PAR_BLOCK stmts'
        p[0] = ('parBlock', p[2])

    def p_stmts(self, p):
        '''stmts : stmt
                | stmts stmt'''
        if len(p) == 3:
            p[0] = (p[1], p[2])
        elif len(p) == 2:
            p[0] = p[1]

    def p_stmt(self, p):
        '''stmt : assignment
                | declaration
                | IF LPAREN condition RPAREN stmt
                | IF LPAREN condition RPAREN stmt ELSE stmt
                | WHILE LPAREN condition RPAREN stmt
                | LBRACE stmts RBRACE
                | func
                '''
        
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 4:
            p[0] =  p[2]
        elif len(p) == 6 and p[1]=='if':
            p[0] = ('if', p[3], p[5])
        elif len(p) == 8:
            p[0] = ('if-else', p[3], p[5], p[7])
        elif len(p) == 6 and p[1]=='while':
            p[0] = ('while', p[3], p[5])
            
    def p_func(self, p):
        '''func : INPUT LPAREN RPAREN
                | OUTPUT LPAREN expr RPAREN'''
        if (len(p)==5):
            p[0] = ('output', p[3])
        else:
            p[0] = (p[1])


    def p_declaration(self, p):
        '''declaration  : c_channel
                    | b_declaration
                    | s_declaration
                    | i_declaration'''
        p[0] = p[1]

    def p_condition(self, p):
        '''condition  : condition LE_THAN expr
                    | condition GE_THAN expr
                    | condition L_THAN expr
                    | condition G_THAN expr
                    | condition EQUAL expr
                    | condition NOT_EQUAL expr
                    | bool_val
                    | expr'''
        if len(p)==4:
            p[0] = ('condition', p[1], p[2], p[3])
        else:
            p[0] = p[1]

    def p_bool_val(self, p):
        '''bool_val : TRUE
                | FALSE'''
        p[0] = p[1]

    def p_assignment(self, p):
        '''assignment : ID ASSIGN expr
                    | ID ASSIGN func'''
        p[0] = ('assign', p[1], p[3])

    def p_expr(self, p):
        '''expr : expr PLUS term
                | expr MINUS term
                | term'''
        if len(p) == 4:
            p[0] = ('expr', p[1], p[2], p[3])
        else:
            p[0] = p[1]

    def p_term(self, p):
        '''term : term TIMES factor
                | term DIVIDE factor
                | factor'''
        if len(p) == 4:
            p[0] = ('term', p[1], p[2], p[3])
        else:
            p[0] = p[1]

    def p_factor(self, p):
        '''factor : LPAREN expr RPAREN
                    | DIGIT
                    | ID
                    | STRING_VALUE'''
        if len(p) == 4:
            p[0] = p[2]
        else:
            if(type(p[1]) == int):
                p[0] = p[1]
            elif(p[1][0] == '"'):
                p[0] = ('STRING', p[1])
            else:
                p[0] = ('ID', p[1])

    def p_empty(self, p):
        'empty : '
        pass

    def p_c_channel(self, p):
        'c_channel : CHANNEL ID ID ID'
        p[0] = ('declaration', p[1], p[2], p[3], p[4])

    def p_b_declaration(self, p):
        'b_declaration : BOOL ID'
        p[0] = ('declaration', p[1], p[2])

    def p_s_declaration(self, p):
        's_declaration : STRING ID'
        p[0] = ('declaration', p[1], p[2])

    def p_i_declaration(self, p):
        'i_declaration : INT ID'
        p[0] = ('declaration', p[1], p[2])
    
    # Error rule for syntax errors
    def p_error(self, p):
        print("Syntax error in input!")

# Build the parser
# parser = yacc.yacc(module=Parser)

print("Builded parser")

# if __name__ == '__main__':
#   file_path = 'examples/test.mp'
#   with open(file_path, 'r') as file:
#     program = file.read()
#     parser = Parser().parser
#     result = parser.parse(program, debug=log)
#     print(result) 

# while True:
#    try:
#        s = input('calc > ')
#    except EOFError:
#        break
#    if not s: continue
#    result = parser.parse(s)
#    print(result)