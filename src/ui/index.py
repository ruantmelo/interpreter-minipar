import tkinter as tk
from tkinter import messagebox


class InterpretadorMiniParApp:
    def __init__(self, root):
        # Configuração da janela principal
        self.root = root
        self.root.title("Interpretador MiniPar")
        self.root.geometry("600x600")

        # Configuração do título
        self.label_programa = tk.Label(root, text="Interpretador de Linguagem MINIPAR", font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#333")
        self.label_programa.pack(pady=10)

        self.txt_programa = tk.Text(root, height=10, width=70)
        self.txt_programa.pack(pady=10)

        # Quadrado para saída
        self.label_saida = tk.Label(root, text="SAÍDA", font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#333")
        self.label_saida.pack(pady=10)

        self.txt_saida = tk.Text(root, height=10, width=70)
        self.txt_saida.pack(pady=10)

        # Botão de execução
        self.btn_execucao = tk.Button(root, text="Executar", font=("Arial", 14), command=self.executar_programa, bg="#4CAF50", fg="white", bd=0, relief="raised", padx=20, pady=10)
        self.btn_execucao.pack(pady=20)

    # Função que será chamada quando o botão "Execução" for pressionado
    def executar_programa(self):
        programa = self.txt_programa.get("1.0", tk.END).strip()  # Pega o conteúdo da emtrada
        
        if programa:
            # Aqui envia a entrada pro programa MiniPar e pega a saída
            saida = "teste de retorno do programa : " + programa 
            
            self.txt_saida.delete(1.0, tk.END)  # Limpa a saída anterior
            self.txt_saida.insert(tk.END, saida)  # Insere o resultado da execução na área de saída
        else:
            messagebox.showwarning("Aviso", "Por favor, insira uma entrada não vazia.")


class Main:
    def __init__(self):
        # Inicializa a aplicação
        self.root = tk.Tk()
        self.app = InterpretadorMiniParApp(self.root)

    def run(self):
        # Executa a interface gráfica
        self.root.mainloop()

# Criando e executando a aplicação
if __name__ == "__main__":
    main_app = Main() 
    main_app.run() 