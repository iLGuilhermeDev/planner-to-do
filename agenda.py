"""
Lista de Tarefas (To-Do List) com Interface Gráfica
Nível: Estudante / Iniciante
Biblioteca: Tkinter (nativa do Python)
Funcionalidades: Adicionar, listar, marcar concluída, remover e persistência em JSON.
"""

import json
import os
import tkinter as tk
from tkinter import messagebox, Listbox, MULTIPLE, END

ARQUIVO = "tarefas.json"

def carregar_tarefas():
    """Carrega as tarefas do arquivo JSON."""
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_tarefas(tarefas):
    """Salva as tarefas no arquivo JSON."""
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(tarefas, f, indent=4, ensure_ascii=False)

class AppTarefas:
    def __init__(self, root):
        self.root = root
        self.root.title("📝 Minha Lista de Tarefas")
        self.root.geometry("500x500")
        self.root.resizable(False, False)

        # Dados
        self.tarefas = carregar_tarefas()

        # Widgets
        self.criar_widgets()

        # Atualizar a lista
        self.atualizar_lista()

    def criar_widgets(self):
        """Cria todos os elementos da interface."""
        # Frame de entrada
        frame_entrada = tk.Frame(self.root)
        frame_entrada.pack(pady=10)

        tk.Label(frame_entrada, text="Nova tarefa:").pack(side=tk.LEFT, padx=5)
        self.entry_tarefa = tk.Entry(frame_entrada, width=40)
        self.entry_tarefa.pack(side=tk.LEFT, padx=5)
        self.entry_tarefa.bind("<Return>", lambda event: self.adicionar())

        btn_adicionar = tk.Button(frame_entrada, text="➕ Adicionar", command=self.adicionar, bg="#4CAF50", fg="white")
        btn_adicionar.pack(side=tk.LEFT, padx=5)

        # Lista de tarefas (com scrollbar)
        frame_lista = tk.Frame(self.root)
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        scrollbar = tk.Scrollbar(frame_lista)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.lista_tarefas = Listbox(frame_lista, yscrollcommand=scrollbar.set, font=("Arial", 10), height=15)
        self.lista_tarefas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.lista_tarefas.yview)

        # Frame de botões de ação
        frame_botoes = tk.Frame(self.root)
        frame_botoes.pack(pady=10)

        btn_concluir = tk.Button(frame_botoes, text="✅ Marcar concluída", command=self.marcar_concluida, bg="#2196F3", fg="white", width=15)
        btn_concluir.pack(side=tk.LEFT, padx=5)

        btn_remover = tk.Button(frame_botoes, text="🗑️ Remover tarefa", command=self.remover, bg="#f44336", fg="white", width=15)
        btn_remover.pack(side=tk.LEFT, padx=5)

        btn_sair = tk.Button(frame_botoes, text="Sair", command=self.root.quit, bg="#555", fg="white", width=10)
        btn_sair.pack(side=tk.RIGHT, padx=5)

    def atualizar_lista(self):
        """Atualiza a exibição da lista de tarefas."""
        self.lista_tarefas.delete(0, END)
        for tarefa in self.tarefas:
            status = "✅" if tarefa["concluida"] else "❌"
            descricao = tarefa["descricao"]
            self.lista_tarefas.insert(END, f"{status}  {descricao}")

    def adicionar(self):
        """Adiciona uma nova tarefa."""
        descricao = self.entry_tarefa.get().strip()
        if not descricao:
            messagebox.showwarning("Aviso", "Digite uma descrição para a tarefa.")
            return
        self.tarefas.append({"descricao": descricao, "concluida": False})
        salvar_tarefas(self.tarefas)
        self.atualizar_lista()
        self.entry_tarefa.delete(0, END)

    def marcar_concluida(self):
        """Marca a(s) tarefa(s) selecionada(s) como concluída(s)."""
        selecionados = self.lista_tarefas.curselection()
        if not selecionados:
            messagebox.showwarning("Aviso", "Selecione pelo menos uma tarefa para marcar como concluída.")
            return
        for indice in selecionados:
            self.tarefas[indice]["concluida"] = True
        salvar_tarefas(self.tarefas)
        self.atualizar_lista()

    def remover(self):
        """Remove a(s) tarefa(s) selecionada(s) definitivamente."""
        selecionados = self.lista_tarefas.curselection()
        if not selecionados:
            messagebox.showwarning("Aviso", "Selecione pelo menos uma tarefa para remover.")
            return
        # Remover do fim para o início para não bagunçar os índices
        for indice in sorted(selecionados, reverse=True):
            self.tarefas.pop(indice)
        salvar_tarefas(self.tarefas)
        self.atualizar_lista()

if __name__ == "__main__":
    root = tk.Tk()
    app = AppTarefas(root)
    root.mainloop()