from abc import ABC, abstractmethod

class ExecutorInterface(ABC):
    @abstractmethod
    def execute(self, parse_tree):
        """Executa a árvore de análise sintática."""
        pass

    @abstractmethod
    def execute_condition(self, parse_tree):
        """Avalia uma condição lógica."""
        pass

    @abstractmethod
    def execute_expr(self, parse_tree):
        """Executa uma expressão."""
        pass

    @abstractmethod
    def execute_term(self, parse_tree):
        """Executa um termo."""
        pass
