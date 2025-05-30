CREATE TABLE IF NOT EXISTS UTENTI (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS TEMPI (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data DATE NOT NULL,
    tempo REAL NOT NULL,
    utente_id INTEGER,
    FOREIGN KEY (utente_id) REFERENCES UTENTI(ID)
);

-- Initial data
INSERT INTO UTENTI (username, password_hash) VALUES
    ('matteo', '12345'),
    ('x', 'x'),
    ('utente1', 'password1');

INSERT INTO TEMPI (utente_id, tempo, data) VALUES
    ((SELECT ID FROM UTENTI WHERE username = 'x'), 48.23, '2024-12-01'),
    ((SELECT ID FROM UTENTI WHERE username = 'x'), 47.55, '2024-12-15'),
    ((SELECT ID FROM UTENTI WHERE username = 'matteo'), 46.11, '2024-11-10');
