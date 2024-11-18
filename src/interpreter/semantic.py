from interpreter.symbol_table import Symbol_Table
from interfaces.interface_logger import ILogger
from interfaces.interface_semantic import ISemantic
class Semantic(ISemantic):
    def __init__(self, logger=None):
        self.symbol_table = Symbol_Table()
        self.logger = logger

    def check_semantic(self, parse_tree):
        if (type(parse_tree) != tuple):
            return parse_tree
        
        match parse_tree[0]:
            case 'seqBlock':
                for stmt in parse_tree[1]:
                    self.check_semantic(stmt)
            case 'parBlock':
                for stmt in parse_tree[1]:
                    self.check_semantic(stmt)
            case 'declaration':
                exists = self.symbol_table.get(parse_tree[2])

                if exists:
                    raise Exception(f"Variable {parse_tree[2]} already declared")

                self.symbol_table.insert(parse_tree[2], parse_tree[1])
                return
            
            case 'assign':
                entry = self.symbol_table.get(parse_tree[1])

                if not entry:
                    raise Exception(f"Variable {parse_tree[1]} not declared")
                
                if (type(parse_tree[2]) == tuple):
                    return self.check_semantic(parse_tree[2])
                elif entry[0] == 'int' and type(parse_tree[2]) != int:
                    raise Exception(f"Type mismatch: {entry[0]} and {type(parse_tree[2])}")
                elif entry[0] == 'string' and type(parse_tree[2]) != str:
                    raise Exception(f"Type mismatch: {entry[0]} and {type(parse_tree[2])}")
                elif entry[0] == 'bool' and type(parse_tree[2]) != bool:
                    raise Exception(f"Type mismatch: {entry[0]} and {type(parse_tree[2])}")
                
            case _: 
                for stmt in parse_tree:
                    self.check_semantic(stmt)