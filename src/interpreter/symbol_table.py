class Symbol_Table():
    def __init__(self):
        self.symbol_table = {}


    def update(self, key, value):
        entry = self.get(key)

        if not entry:
            raise Exception(f"Variable {key} not declared")
        
        if type(entry[0]) == 'string' and type(value) != str:
            raise Exception(f"Type mismatch: {entry[0]} and {type(value)}")
        if type(entry[0]) == 'int' and type(value) != int:
            raise Exception(f"Type mismatch: {entry[0]} and {type(value)}")
        if type(entry[0]) == 'bool' and type(value) != bool:
            raise Exception(f"Type mismatch: {entry[0]} and {type(value)}")

        self.symbol_table[key] = (entry[0], value)
    
    def insert(self, key, var_type):
        entry = self.get(key)
        
        if entry:
            return None
        self.symbol_table[key] = (var_type, None)
        
    def get(self, key):
        return self.symbol_table.get(key, None)