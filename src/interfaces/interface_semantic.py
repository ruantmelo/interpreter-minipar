from abc import ABC, abstractmethod

class ISemantic(ABC):
    @abstractmethod
    def check_semantic(self, parse_tree):
        '''Verifica a semântica do código'''
        pass
