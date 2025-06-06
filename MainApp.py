import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import filedialog
from Relatorio import ReportWindow
import re
import fitz
from bd import *

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciamento de Currículos")
        self.root.geometry("960x400")
        self.create_widgets()
        self.refresh_data()

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Nome:").grid(row=0, column=0)
        self.nome_entry = tk.Entry(frame)
        self.nome_entry.grid(row=0, column=1)

        tk.Label(frame, text="Email:").grid(row=1, column=0)
        self.email_entry = tk.Entry(frame)
        self.email_entry.grid(row=1, column=1)

        tk.Label(frame, text="Telefone:").grid(row=2, column=0)
        self.tel_entry = tk.Entry(frame)
        self.tel_entry.grid(row=2, column=1)

        tk.Button(frame, text="Cadastrar", command=self.importar_pdf).grid(row=3, column=0, pady=10)
        tk.Button(frame, text="Editar", command=self.editar).grid(row=3, column=1)
        tk.Button(frame, text="Remover", command=self.remover).grid(row=3, column=2)

        tk.Button(self.root, text="Gerar Relatório", command=self.abrir_relatorio).pack(pady=5)

        self.tree = ttk.Treeview(self.root, columns=("id", "nome", "email", "telefone", "data"), show="headings")
        for     col in ("id", "nome", "email", "telefone", "data"):
            self.tree.heading(col, text=col.capitalize())
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<ButtonRelease-1>", self.selecionar_item)

    def refresh_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in listar_curriculos():
            self.tree.insert("", tk.END, values=row)

    def selecionar_item(self):
        selected = self.tree.focus()
        if selected:
            values = self.tree.item(selected, "values")
            self.nome_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            self.tel_entry.delete(0, tk.END)
            self.nome_entry.insert(0, values[1])
            self.email_entry.insert(0, values[2])
            self.tel_entry.insert(0, values[3])

    def editar(self):
        selected = self.tree.focus()
        if not selected:
            return

        values = self.tree.item(selected, "values")
        id_ = values[0]

        nome_novo = self.nome_entry.get().strip()
        email_novo = self.email_entry.get().strip()
        tel_novo = self.tel_entry.get().strip()

        if not nome_novo and not email_novo and not tel_novo:
            messagebox.showerror("Erro", "Preencha pelo menos um campo para editar.")
            return

        dados_antigos = get_curriculo_por_id(id_)
        if not dados_antigos:
            messagebox.showerror("Erro", "Registro não encontrado.")
            return

        nome_final = nome_novo if nome_novo else dados_antigos[0]
        email_final = email_novo if email_novo else dados_antigos[1]
        tel_final = tel_novo if tel_novo else dados_antigos[2]

        editar_curriculo(id_, nome_final, email_final, tel_final)
        self.refresh_data()

    def remover(self):
        selected = self.tree.focus()
        if selected:
            values = self.tree.item(selected, "values")
            nome = values[1]
            resposta = messagebox.askyesno("Confirmação", f"Tem certeza de que deseja remover o currículo de {nome}?")
            if resposta:
                remover_curriculo(values[0])
                self.refresh_data()

    def abrir_relatorio(self):
        ReportWindow()

    def importar_pdf(self):
        path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if not path:
            return

        try:
            doc = fitz.open(path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()

            email = re.search(r'\b[\w\.-]+@[\w\.-]+\.\w{2,}\b', text)
            telefone = re.search(r'\(?\d{2}\)?\s*9?\d{4}[-\s]?\d{4}', text)
            nome = re.search(r'(Nome(?: completo)?[:\-]?\s*)([A-ZÁÉÍÓÚÂÊÔÃÕÇ][a-záéíóúâêôãõç]+(?:\s+[A-ZÁÉÍÓÚÂÊÔÃÕÇ]?[a-záéíóúâêôãõç]+)+)', text)

            nome_valor = nome.group(2) if nome else ""
            email_valor = email.group(0) if email else ""
            telefone_valor = telefone.group(0) if telefone else ""

            if not nome_valor:
                for linha in text.splitlines():
                    if linha.strip() and not linha.lower().startswith(("currículo", "resumo", "dados", "informações")):
                        nome_valor = linha.strip()
                        break

            self.abrir_tela_revisao(nome_valor, email_valor, telefone_valor, text, path)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao ler PDF: {e}")
    
    def abrir_tela_revisao(self, nome, email, telefone, texto_pdf, caminho_pdf):
        revisao = tk.Toplevel(self.root)
        revisao.title("Revisar e Confirmar Dados")
        revisao.geometry("600x500")
        revisao.resizable(False, False)

        lbl_pdf = tk.Label(revisao, text="Conteúdo do PDF:")
        lbl_pdf.pack(anchor="w", padx=10, pady=(10, 0))

        txt_pdf = tk.Text(revisao, height=15, wrap="word", bg="#f8f8f8")
        txt_pdf.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        txt_pdf.insert("1.0", texto_pdf)
        txt_pdf.config(state="disabled")

        frm_campos = tk.Frame(revisao)
        frm_campos.pack(padx=10, pady=5)

        tk.Label(frm_campos, text="Nome:").grid(row=0, column=0, sticky="w")
        nome_entry = tk.Entry(frm_campos, width=50)
        nome_entry.grid(row=0, column=1, pady=2)

        tk.Label(frm_campos, text="Email:").grid(row=1, column=0, sticky="w")
        email_entry = tk.Entry(frm_campos, width=50)
        email_entry.grid(row=1, column=1, pady=2)

        tk.Label(frm_campos, text="Telefone:").grid(row=2, column=0, sticky="w")
        tel_entry = tk.Entry(frm_campos, width=50)
        tel_entry.grid(row=2, column=1, pady=2)

        nome_entry.insert(0, nome)
        email_entry.insert(0, email)
        tel_entry.insert(0, telefone)

        frm_botoes = tk.Frame(revisao)
        frm_botoes.pack(pady=10)

        def confirmar():
            nome_final = nome_entry.get()
            email_final = email_entry.get()
            tel_final = tel_entry.get()

            if nome_final and email_final and tel_final:
                try:
                    
                    vaga_titulo = ""
                    for vaga in listar_vagas():  
                        if vaga[1].lower() in texto_pdf.lower():
                            vaga_titulo = vaga[1]
                            break

                    vaga_id = get_vaga_id_por_titulo(vaga_titulo) if vaga_titulo else None

                    inserir_curriculo(nome_final, email_final, tel_final, caminho_pdf, vaga_id)
                    self.refresh_data()
                    messagebox.showinfo("Sucesso", "Currículo importado com sucesso.")
                    revisao.destroy()
                except Exception as e:
                    messagebox.showerror("Erro", f"Falha ao salvar: {e}")
            else:
                messagebox.showerror("Erro", "Preencha todos os campos.")

        tk.Button(frm_botoes, text="Confirmar", command=confirmar).pack(side="left", padx=10)
        tk.Button(frm_botoes, text="Cancelar", command=revisao.destroy).pack(side="left", padx=10)