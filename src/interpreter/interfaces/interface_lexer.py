from abc import ABC, abstractmethod

class ILexer(ABC):
    
    @abstractmethod
    def __init__(self, **kwargs):
        """Construtor."""
        pass
    
    @abstractmethod
    def t_ID(self, t):
        """Reconhece um identificador."""
        pass
    
    @abstractmethod
    def t_DIGIT(self, t):
        """Reconhece um número."""
        pass
    
    @abstractmethod
    def t_STRING_VALUE(self, t):
        """Reconhece uma string."""
        pass
    
    @abstractmethod
    def t_newline(self,t):
        """Reconhece uma nova linha."""
        pass
    
    @abstractmethod
    def t_error(self, t):
        """Reconhece um erro."""
        pass
    
    @abstractmethod
    def find_column(self, input, token):
        """Encontra a coluna de um token."""
        pass
    
    @abstractmethod
    def build(self, **kwargs):
        """Inicializa o lexer."""
        pass
    
    @abstractmethod
    def test(self,data):
        """Testa"""
        pass