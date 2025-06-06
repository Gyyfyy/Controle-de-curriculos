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

CREATE TABLE IF NOT EXISTS Vaga (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            resumo TEXT NOT NULL,
            local TEXT NOT NULL,
            requisitos TEXT NOT NULL,
            remuneracao TEXT NOT NULL
        )

 CREATE TABLE IF NOT EXISTS Usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )