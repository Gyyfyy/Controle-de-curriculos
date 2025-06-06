import tkinter as tk
from tkinter import ttk
from bd import *

class ReportWindow:
    def __init__(self):
        self.win = tk.Toplevel()
        self.win.title("Relatório de Vagas")
        self.win.geometry("900x400")
        self.criar_tabela()

    def criar_tabela(self):
        inserir_vagas_iniciais()
        self.tree = ttk.Treeview(self.win, columns=("id", "titulo", "resumo", "local", "requisitos", "remuneracao"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=150)
        self.tree.pack(fill="both", expand=True)

        for vaga in listar_vagas():
            self.tree.insert("", tk.END, values=vaga)

        self.tree.bind("<Double-1>", self.mostrar_candidatos)

    def mostrar_candidatos(self, event):
        item = self.tree.selection()[0]
        vaga = self.tree.item(item, "values")
        vaga_id = vaga[0]

        candidatos = listar_curriculos_por_vaga(vaga_id)

        popup = tk.Toplevel(self.win)
        popup.title(f"Candidatos para: {vaga[1]}")
        popup.geometry("600x300")

        tree = ttk.Treeview(popup, columns=("id", "nome", "email", "telefone"), show="headings")
        for col in tree["columns"]:
            tree.heading(col, text=col.capitalize())
        tree.pack(fill="both", expand=True)

        for c in candidatos:
            tree.insert("", tk.END, values=c)