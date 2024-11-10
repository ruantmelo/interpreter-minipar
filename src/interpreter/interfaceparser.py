from abc import ABC, abstractmethod

class IParser(ABC):
    
    @abstractmethod
    def parsing(self, program):
        """Recebe o código fonte e inicia o processo de parsing, retornando o resultado da análise sintática."""
        pass

    @abstractmethod
    def p_stmt_block(self, p):
        """Define uma regra de produção para blocos de instruções."""
        pass
    
    @abstractmethod
    def p_seq_stmts(self, p):
        """Define uma regra de produção para instruções sequenciais."""
        pass
    
    @abstractmethod
    def p_par_block(self, p):
        """Define uma regra de produção para instruções paralelas."""
        pass
    
    @abstractmethod
    def p_stmts(self, p):
        """Define uma regra de produção para uma lista de instruções."""
        pass
    
    @abstractmethod
    def p_stmt(self, p):
        """Define uma regra de produção para uma única instrução."""
        pass
    
    @abstractmethod
    def p_func(self, p):
        """Define uma regra de produção para funções, como INPUT e OUTPUT."""
        pass

    @abstractmethod
    def p_declaration(self, p):
        """Define uma regra de produção para declarações de variáveis."""
        pass

    @abstractmethod
    def p_condition(self, p):
        """Define uma regra de produção para condições."""
        pass

    @abstractmethod
    def p_bool_val(self, p):
        """Define uma regra de produção para valores booleanos."""
        pass

    @abstractmethod
    def p_assignment(self, p):
        """Define uma regra de produção para atribuições."""
        pass

    @abstractmethod
    def p_expr(self, p):
        """Define uma regra de produção para expressões."""
        pass

    @abstractmethod
    def p_term(self, p):
        """Define uma regra de produção para termos."""
        pass

    @abstractmethod
    def p_factor(self, p):
        """Define uma regra de produção para fatores."""
        pass

    @abstractmethod
    def p_empty(self, p):
        """Define uma regra de produção para valores vazios."""
        pass

    @abstractmethod
    def p_c_channel(self, p):
        """Define uma regra de produção para a declaração de canais."""
        pass

    @abstractmethod
    def p_b_declaration(self, p):
        """Define uma regra de produção para declarações booleanas."""
        pass

    @abstractmethod
    def p_s_declaration(self, p):
        """Define uma regra de produção para declarações de strings."""
        pass

    @abstractmethod
    def p_i_declaration(self, p):
        """Define uma regra de produção para declarações de inteiros."""
        pass

    @abstractmethod
    def p_error(self, p):
        """Define uma regra de tratamento de erros sintáticos."""
        pass
