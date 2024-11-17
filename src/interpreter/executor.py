import logging
import socket
from symbol_table import Symbol_Table
import threading
from interfaces.interface_execute import ExecutorInterface

PORT_A = 8000
PORT_B = 8001

class Executor(ExecutorInterface):
    def __init__(self):
       
        self.symbol_table = Symbol_Table()

    def execute(self, parse_tree):
        print('executing', parse_tree)

        if (type(parse_tree) != tuple):
            if (type(parse_tree) == str):
                return parse_tree[1:-1]
            return parse_tree

    
        if (type(parse_tree[0]) == tuple):
            for s in parse_tree:
                self.execute(s)
            return

        match parse_tree[0]:
            case 'seqBlock':
                for s in parse_tree[1]:
                    self.execute(s)
            
            case 'parBlock':
                thread = threading.Thread(target= lambda : [self.execute(s) for s in parse_tree[1]])  
                thread.start()   
                    
            case 'if' : # ('if', ('condition', <ID>, <operator>, <id>)
                if (self.execute_condition(parse_tree[1])):
                        self.execute(parse_tree[2])
            
            case 'if-else': # ('if-else', ('condition', <ID>, <operator>, <id>), <stmt>, <stmt>)
                if (self.execute_condition(parse_tree[1])):
                    for s in parse_tree[2]:
                        self.execute(s)
                else:
                    for s in parse_tree[3]:
                        self.execute(s)
            case 'declaration': # ('declaration', <type>, <ID>)('declaration', 'int', 'variavel')
                # Verifica se p2 existe na tabela de simbolos
                
                value = self.symbol_table.get(parse_tree[2])
            
               

                # Se sim, lança erro
                if (value != None):
                    raise Exception("Symbol already declared")
                
                if (parse_tree[1] == 'chan'):
                    #Pega o endereço
                    host_address = self.execute(parse_tree[3])
                    target_address = self.execute(parse_tree[4])
                    #tupla com o endereço
                    myAddress = host_address
                    server_address = target_address
                    #armazena na tabela de simbolos o endereço
                    self.symbol_table.insert(parse_tree[2], parse_tree[1])
                    self.symbol_table.update(parse_tree[2], (myAddress, server_address))

                # Se não, cria uma nova entrada na tabela de simbolos
                else: self.symbol_table.insert(parse_tree[2], parse_tree[1])

                # send_stmt : SEND LPAREN expr RPAREN
                #     | SEND LPAREN expr COMMA expr COMMA expr RPAREN

            
            case 'channelMethod':
                addresses = self.symbol_table.get(parse_tree[1])
                addresses = addresses[1]
                host_address = addresses[0]
                target_address = addresses[1]

                print("channelMethod", parse_tree)
                
                #se for send
                if (parse_tree[2][0] == 'send'):
                    print('Enviando dados', parse_tree)
                    if (len(parse_tree[2]) == 2):
                        print("SERVIDOR ENVIANDO RESULTADO")
                        self.send_data(str(self.execute(parse_tree[2][1])),(target_address, PORT_A))
                    else:
                        print("CLIENTE ENVIANDO OPERAÇÃO")
                        operador = self.execute(parse_tree[2][1])
                        operandoA = parse_tree[2][2]
                        operandoB = parse_tree[2][3]
                        result = str(operador) + " " + str(operandoA) + " " + str(operandoB)
                        self.send_data(result, (target_address, PORT_B))
                    #se for receive    
                else:
                    print("Recebendo dados")

                    if (len(parse_tree[2]) == 2):
                        print("CLIENTE RECEBENDO DADOS")
                        value = self.receive_data((host_address, PORT_A))
                        self.symbol_table.update(parse_tree[2][1], value)
                    else:
                        print("SERVIDOR RECEBENDO A OPERAÇÃO")
                        print("addresses: ", addresses)
                        value = self.receive_data((host_address, PORT_B))
                        ops = value.split(" ")

                        print('ops ', ops)

                        operador = ops[0]
                        operandoA = int(ops[1])
                        operandoB = int(ops[2])
                        self.symbol_table.update(parse_tree[2][1], operador)
                        self.symbol_table.update(parse_tree[2][2], operandoA)
                        self.symbol_table.update(parse_tree[2][3], operandoB)

            case 'while':
                while(self.execute_condition(parse_tree[1])):
                    self.execute(parse_tree[2])
                return None
            case 'expr':
                return self.execute_expr(parse_tree)
            case 'term':
                return self.execute_term(parse_tree)
            case 'assign':
                # ('assign', 'variavel', 10)
                # ('assign', 'variavel', 'string')
                # ('assign', 'variavel', ('expr', 1, '+', 2))
                key = parse_tree[1]

                print('assign', parse_tree)
                if type(parse_tree[2]) == tuple:
                        value = self.execute(parse_tree[2])
                else:
                        value = parse_tree[2]
                self.symbol_table.update(key, value)
            case 'output':
                if type(parse_tree[1]) == tuple:
                    value = self.execute(parse_tree[1])
                    value =  value[1] if type(value) == tuple else value

                    print('=============== output: ', value)
                else:
                    print(parse_tree[1])
            case 'input':
                value = input("enter value: ")
                return value
            case 'ID':
                print('gettind id', parse_tree[1], self.symbol_table.get(parse_tree[1]))
                return self.symbol_table.get(parse_tree[1])[1]
            case 'STRING': 
                return self.execute(parse_tree[1])
            
            case _:
                print('not implemented yet', parse_tree)
                return 0
            
    def send_data(self, data, address):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print("Connecting to server ", address[0], " at port ", address[1])
            sock.connect(address)
            sock.sendall(data.encode())
        finally:
            sock.close()
    
    def receive_data(self, address):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            print("Listening to ", address[0], " at port ", address[1])
            sock.bind(address)

            sock.listen(2)

            while True:
                clientSock, clientAddress = sock.accept()
                data = clientSock.recv(1024)
                if not data:
                    break

                return data.decode()
                clientSock.close()            
        finally:

            sock.close()

    def execute_condition(self, parse_tree):

        
        value_a = None
        value_b = None 

        # TODO: Existem outros casos além desse?
        if len(parse_tree) == 4:
            if type(parse_tree[1] == tuple):
                value_a = self.execute(parse_tree[1])

                # if (type(value_a) == tuple):
                #     value_a = value_a[1]

            if type(parse_tree[3] == tuple):
                value_b = self.execute(parse_tree[3])

                # if (type(value_b) == tuple):
                #     value_b = value_b[1]

        print('values ', value_a, value_b)

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
        print("executing expr ", parse_tree)
        if type(parse_tree) == int:
            return parse_tree
        if type(parse_tree) == str: # TODO: Como fica pra variável e pra string?
            return self.symbol_table.get(parse_tree)
        if type(parse_tree) == tuple:
            print('TUPLAZINHA', parse_tree)
            if len(parse_tree) == 4:
                a = self.execute(parse_tree[1]) if type(parse_tree[1]) == tuple else parse_tree[1] 
                b = self.execute(parse_tree[3]) if type(parse_tree[3]) == tuple else parse_tree[3] 

                print('tup values ', a, b)
                match parse_tree[2]:
                    case '+':
                        return a + b
                    case '-':
                        return a - b
                    case '*':
                        return a * b
                    case '/':
                        return a / b
            if len(parse_tree) == 3:
                return self.symbol_table.get(parse_tree[2])
            
            return parse_tree
            

    def execute_term(self, parse_tree):
        a = self.execute(parse_tree[1]) if type(parse_tree[1]) == tuple else parse_tree[1] 
        b = self.execute(parse_tree[3]) if type(parse_tree[3]) == tuple else parse_tree[3] 

        match parse_tree[2]:
            case '*':
                return a * b
            case '/':
                return a / b
        pass