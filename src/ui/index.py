from tkinter import *
from tkinter import messagebox

from interfaces.interface_parser import IParser
from interfaces.interface_execute import ExecutorInterface
from interpreter.tklogger import TkLogger

from interpreter.interpreterc import Interpreter

from interpreter.parser import Parser
from interpreter.executor import Executor

class InterpreterGUI:
    def __init__(self):
        self._root = self._gui_config()
        self._logger = TkLogger(self.txt_output)
        self._interpreter = Interpreter(logger=self._logger, Parser=Parser, Executor=Executor)
        

        self._root.mainloop()

    def execute_source(self):
        source = self.editor.get("1.0", END).strip()  # Pega o conteúdo da entrada
       
        if source:
            self._interpreter.run(source)
            # Exibe o resultado na área de saída
            # self.txt_saida.delete(1.0, END)  # Limpa a saída anterior
            # self.txt_saida.insert(END, resultado)  # Insere o resultado da execução
        else:
            messagebox.showwarning("Aviso", "Por favor, insira uma entrada não vazia.")

    def _gui_config(self):
        root = Tk()
        root.title("Interpretador MiniPar")
        root.geometry("600x600")

        # Configuração do título
        label_app = Label(root, text="Interpretador de Linguagem MINIPAR", font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#333")
        label_app.pack(pady=10)

        self.editor = Text(root, height=10, width=70)
        self.editor.pack(pady=10)

        # Quadrado para saída
        label_output = Label(root, text="SAÍDA", font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#333")
        label_output.pack(pady=10)

        self.txt_output = Text(root, state='disabled', height=10, width=70)
        self.txt_output.pack(pady=10)
 
        # Botão de execução
        btn_execute = Button(root, text="Executar", font=("Arial", 14), command=self.execute_source, bg="#4CAF50", fg="white", bd=0, relief="raised", padx=20, pady=10)
        btn_execute.pack(pady=20)

        return root
# class Main:
#     def __init__(self):

#     def run(self):
#         # Executa a interface gráfica
#         self.root.mainloop()

# # Criando e executando a aplicação
# if __name__ == "__main__":
#     main_app = Main() 
#     main_app.run()