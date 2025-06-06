import tkinter as tk
from MainApp import MainApp
from tkinter import messagebox
from bd import validar_login

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("300x200")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Usuário:").pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="Senha:").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        tk.Button(self.root, text="Entrar", command=self.login).pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if validar_login(username, password):
            self.root.destroy()
            main = tk.Tk()
            MainApp(main)
            main.mainloop()
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos")