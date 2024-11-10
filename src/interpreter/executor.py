import logging
from symbol_table import Symbol_Table


class Executor():
    def __init__(self):
       
        self.symbol_table = Symbol_Table()

    def execute(self, parse_tree):
        print('executing', parse_tree)

        if (type(parse_tree[0]) == tuple):
            print('executing tuple', parse_tree[0])
            for s in parse_tree[0]:
                self.execute(s)
            return

        match parse_tree[0]:
            case 'seqBlock':
                for s in parse_tree[1]:
                    self.execute(s)
            
            case 'parBlock':
                for s in parse_tree[1]:
                    self.execute(s)
            
            case 'if' : # ('if', ('condition', <ID>, <operator>, <id>)
                if (self.execute_condition(parse_tree[1])):
                    for s in parse_tree[2]:
                        self.execute(s)
            
            case 'if-else': # ('if-else', ('condition', <ID>, <operator>, <id>), <stmt>, <stmt>)
                if (self.execute_condition(parse_tree[1])):
                    for s in parse_tree[2]:
                        self.execute(s)
                else:
                    for s in parse_tree[3]:
                        self.execute(s)
            case 'declaration': # ('declaration', <type>, <ID>)('declaration', 'int', 'variavel')
                # Verifica se p2 existe na tabela de simbolos
                print('declaration', parse_tree)
                value = self.symbol_table.get(parse_tree[2])

                print('value', value)

                # Se sim, lança erro
                if (value != None):
                    raise Exception("Symbol already declared")
                
                # Se não, cria uma nova entrada na tabela de simbolos
                self.symbol_table.insert(parse_tree[2], parse_tree[1])
            
            
            case 'assign':
                # ('assign', 'variavel', 10)
                # ('assign', 'variavel', 'string')
                # ('assign', 'variavel', ('expr', 1, '+', 2))
                key = parse_tree[1]

                print('assign', parse_tree)
                if type(parse_tree[2]) == tuple:
                        value = self.execute_expr(parse_tree[2])
                else:
                        value = parse_tree[2]
                self.symbol_table.update(key, value)
            case 'output':
                if type(parse_tree[1]) == tuple:
                    print(self.execute(parse_tree[1]))
                else:
                    print(parse_tree[1])
            case 'input':
                value = input("enter value: ")
                return value
            case 'ID':
                print('gettind id', parse_tree[1], self.symbol_table.get(parse_tree[1]))
                return self.symbol_table.get(parse_tree[1])
            case 'STRING':
                return parse_tree[1]
            case _:
                print('not implemented yet', parse_tree)
                return 0
            
        
    def execute_condition(self, parse_tree) -> int:
        value_a = type(parse_tree[1]) == str and self.symbol_table.get(parse_tree[1])
        value_b = type(parse_tree[3]) == str and self.symbol_table.get(parse_tree[3])

        match parse_tree[2]:
            case '==':
                return value_a == value_b
            case '!=':
                return value_a != value_b
            case '>':
                return value_a > value_b
            case '<':
                return value_a < value_b
            case '>=':
                return value_a >= value_b
            case '<=':
                return value_a <= value_b
        
        return False

    def execute_expr(self, parse_tree): # ('expr', 1, '+', 2)
        if type(parse_tree) == int:
            return parse_tree
        if type(parse_tree) == str:
            return self.symbol_table.get(parse_tree)
        if type(parse_tree) == tuple:
            print('TUPLAZINHA', parse_tree)
            a = self.execute_expr(parse_tree[1])
            b = self.execute_expr(parse_tree[3])
            match parse_tree[2]:
                case '+':
                    return a + b
                case '-':
                    return a - b
                case '*':
                    return a * b
                case '/':
                    return a / b
            