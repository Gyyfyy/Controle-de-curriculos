import sqlite3
import os
import shutil
from datetime import datetime

def init_db():
    conn = sqlite3.connect("Banco.db")
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS Curriculo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL,
        telefone TEXT NOT NULL,
        data_importacao TEXT NOT NULL,
        pdf_path TEXT NOT NULL,
        vaga_id INTEGER,
        FOREIGN KEY(vaga_id) REFERENCES Vaga(id)
    )
''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS Vaga (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            resumo TEXT NOT NULL,
            local TEXT NOT NULL,
            requisitos TEXT NOT NULL,
            remuneracao TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS Usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    
    c.execute("INSERT OR IGNORE INTO Usuario (username, password) VALUES (?, ?)", ("admin", "1234"))
    conn.commit()
    conn.close()

def validar_login(username, password):
    conn = sqlite3.connect("Banco.db")
    c = conn.cursor()
    c.execute("SELECT * FROM Usuario WHERE username=? AND password=?", (username, password))
    resultado = c.fetchone()
    conn.close()
    return resultado is not None

def listar_curriculos():
    conn = sqlite3.connect("Banco.db")
    c = conn.cursor()
    c.execute("SELECT * FROM Curriculo")
    rows = c.fetchall()
    conn.close()
    return rows

def get_curriculo_por_id(id_):
    conn = sqlite3.connect("Banco.db")
    c = conn.cursor()
    c.execute("SELECT nome, email, telefone FROM Curriculo WHERE id = ?", (id_,))
    resultado = c.fetchone()
    conn.close()
    return resultado

def editar_curriculo(id_, nome, email, telefone):
    conn = sqlite3.connect("Banco.db")
    c = conn.cursor()
    c.execute("UPDATE Curriculo SET nome=?, email=?, telefone=? WHERE id=?", (nome, email, telefone, id_))
    conn.commit()
    conn.close()

def remover_curriculo(id_):
    conn = sqlite3.connect("Banco.db")
    c = conn.cursor()
    c.execute("DELETE FROM Curriculo WHERE id=?", (id_,))
    conn.commit()
    conn.close()

def inserir_curriculo(nome, email, telefone, caminho_pdf_original, vaga_id):
    pasta_destino = "pdfs"
    os.makedirs(pasta_destino, exist_ok=True)

    nome_arquivo = os.path.basename(caminho_pdf_original)
    destino_final = os.path.join(pasta_destino, nome_arquivo)

    if os.path.exists(destino_final):
        base, ext = os.path.splitext(nome_arquivo)
        count = 1
        while os.path.exists(os.path.join(pasta_destino, f"{base}_{count}{ext}")):
            count += 1
        destino_final = os.path.join(pasta_destino, f"{base}_{count}{ext}")

    shutil.copy2(caminho_pdf_original, destino_final)

    conn = sqlite3.connect('Banco.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO Curriculo (nome, email, telefone, data_importacao, pdf_path, vaga_id)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (nome, email, telefone, datetime.now().isoformat(), destino_final, vaga_id))

    conn.commit()
    conn.close()

def abrir_pdf_do_curriculo(id_curriculo):
    conn = sqlite3.connect('Banco.db')
    cursor = conn.cursor()

    cursor.execute('SELECT pdf_path FROM Curriculo WHERE id = ?', (id_curriculo,))
    resultado = cursor.fetchone()
    conn.close()

    if resultado and os.path.exists(resultado[0]):
        os.startfile(resultado[0])  
    else:
        print("Arquivo não encontrado.")

def inserir_vagas_iniciais():
    conn = sqlite3.connect("Banco.db")
    c = conn.cursor()

    vagas = [
        ("Desenvolvedor Python Júnior", 
         "Atuar com desenvolvimento backend em Python e integração de APIs.", 
         "São Paulo - SP", 
         "Conhecimento em Python, SQLite, Git. Desejável: Django.", 
         "R$ 4.000,00"),
        
        ("Analista de Dados", 
         "Responsável por modelagem de dados e visualização com Power BI.", 
         "Belo Horizonte - MG", 
         "SQL avançado, Excel, Power BI, ETL. Desejável: Python.", 
         "R$ 5.500,00"),
        
        ("Estágio em Suporte Técnico", 
         "Prestar suporte a usuários internos e manutenção de sistemas.", 
         "Curitiba - PR", 
         "Cursando TI ou áreas afins. Boa comunicação e proatividade.", 
         "R$ 1.200,00 + VT + VR")
    ]

    for vaga in vagas:
        c.execute("INSERT INTO Vaga (titulo, resumo, local, requisitos, remuneracao) VALUES (?, ?, ?, ?, ?)", vaga)

    conn.commit()
    conn.close()


def listar_vagas():
    conn = sqlite3.connect("Banco.db")
    c = conn.cursor()
    c.execute("SELECT id, titulo, resumo, local, requisitos, remuneracao FROM Vaga")
    rows = c.fetchall()
    conn.close()
    return rows

def listar_curriculos_por_vaga(vaga_id):
    conn = sqlite3.connect("Banco.db")
    c = conn.cursor()
    c.execute("SELECT id, nome, email, telefone FROM Curriculo WHERE vaga_id=?", (vaga_id,))
    rows = c.fetchall()
    conn.close()
    return rows

def get_vaga_id_por_titulo(titulo):
    conn = sqlite3.connect("Banco.db")
    c = conn.cursor()
    c.execute("SELECT id FROM Vaga WHERE titulo = ?", (titulo,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None