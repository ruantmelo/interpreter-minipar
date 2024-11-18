import socket
from interpreter.symbol_table import Symbol_Table
import threading
from interfaces.interface_execute import ExecutorInterface

PORT_A = 8000
PORT_B = 8001

class Executor(ExecutorInterface):
    def __init__(self, logger=None):
        self.logger = logger
        self.symbol_table = Symbol_Table()

    def reset(self):
        self.symbol_table = Symbol_Table()

    def execute(self, parse_tree):
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
                    # Pega o endereço
                    host_address = self.execute(parse_tree[3])
                    target_address = self.execute(parse_tree[4])

                    # tupla com o endereço
                    myAddress = host_address
                    server_address = target_address

                    #armazena na tabela de simbolos o endereço
                    self.symbol_table.insert(parse_tree[2], parse_tree[1])
                    self.symbol_table.update(parse_tree[2], (myAddress, server_address))

                # Se não, cria uma nova entrada na tabela de simbolos
                else: self.symbol_table.insert(parse_tree[2], parse_tree[1])

                # send_stmt : SEND LPAREN expr RPAREN
                #     | SEND LPAREN expr COMMA expr COMMA expr RPAREN

            case 'func':
                if (parse_tree[1] == 'output'):
                    if type(parse_tree[2]) == tuple:
                        value = self.execute(parse_tree[2])
                        value =  value[1] if type(value) == tuple else value
                        self.logger.log(f'Output: {value}')
                        print('Output: ', value)
                    else:
                        print(parse_tree[1])
                elif (parse_tree[1] == 'input'):
                    value = input("Enter value: ")
                    return value
                else:
                    self.execute_channel_method(parse_tree[1])

               

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

               
                if type(parse_tree[2]) == tuple:
                        value = self.execute(parse_tree[2])
                else:
                        value = parse_tree[2]
                self.symbol_table.update(key, value)
            case 'ID':
              
                return self.symbol_table.get(parse_tree[1])[1]
            case 'STRING': 
                return self.execute(parse_tree[1])
            
            case _:
                return None
    
    def execute_channel_method(self, parse_tree):
        addresses = self.symbol_table.get(parse_tree[1])
        addresses = addresses[1]
        host_address = addresses[0]
        target_address = addresses[1]

        
        #se for send
        if (parse_tree[2][0] == 'send'):
            
            if (len(parse_tree[2]) == 2):
                
                self.send_data(str(self.execute(parse_tree[2][1])),(target_address, PORT_A))
            else:
                
                operador = self.execute(parse_tree[2][1])
                operandoA = parse_tree[2][2]
                operandoB = parse_tree[2][3]
                result = str(operador) + " " + str(operandoA) + " " + str(operandoB)
                self.send_data(result, (target_address, PORT_B))
            #se for receive    
        else:
            if (len(parse_tree[2]) == 2):
                value = self.receive_data((host_address, PORT_A))
                self.symbol_table.update(parse_tree[2][1], value)
            else:
                
                value = self.receive_data((host_address, PORT_B))
                ops = value.split(" ")

                
                operador = ops[0]
                operandoA = int(ops[1])
                operandoB = int(ops[2])
                self.symbol_table.update(parse_tree[2][1], operador)
                self.symbol_table.update(parse_tree[2][2], operandoA)
                self.symbol_table.update(parse_tree[2][3], operandoB)

    def send_data(self, data, address):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.logger.log("Connecting to server " + address[0] + " at port " + str(address[1]))
            print("Connecting to server " , address[0], " at port ", address[1])
            sock.connect(address)
            sock.sendall(data.encode())
        finally:
            sock.close()
    
    def receive_data(self, address):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.logger.log("Listening to server " + address[0] + " at port " + str(address[1]))
            print("Listening to server " , address[0], " at port ", address[1])
            sock.bind(address)

            sock.listen(2)

            while True:
                clientSock, clientAddress = sock.accept()
                data = clientSock.recv(1024)
                if not data:
                    break

                return data.decode()
                        
        finally:

            sock.close()

    def execute_condition(self, parse_tree):
        value_a = None
        value_b = None 

        if len(parse_tree) == 4:
            if type(parse_tree[1] == tuple):
                value_a = self.execute(parse_tree[1])

            if type(parse_tree[3] == tuple):
                value_b = self.execute(parse_tree[3])


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
            if len(parse_tree) == 4:
                a = self.execute(parse_tree[1]) if type(parse_tree[1]) == tuple else parse_tree[1] 
                b = self.execute(parse_tree[3]) if type(parse_tree[3]) == tuple else parse_tree[3] 

                match parse_tree[2]:
                    case '+':
                        return a + b
                    case '-':
                        return a - b
                    case '*':
                        return a * b
                    case '/':
                        if b == 0:
                            raise Exception("Division by zero")
                        return a // b
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
                if b == 0:
                    raise Exception("Division by zero")
                return a // b
        pass