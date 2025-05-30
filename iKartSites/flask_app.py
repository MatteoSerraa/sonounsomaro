from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'x'

def get_db():
    db = sqlite3.connect('sonounsomaro/iKartSites/ikart.db')
    db.row_factory = sqlite3.Row
    return db

def init_db():
    if not os.path.exists('ikart.db'):
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        db.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db()
        user = db.execute('SELECT * FROM UTENTI WHERE username = ? AND password_hash = ?',
                         (username, password)).fetchone()
        db.close()
        
        if user:
            session['username'] = username
            session['user_id'] = user['ID']
            return redirect('/tempi')
        else:
            return render_template('login.html', errore='Credenziali non valide')

    return render_template('login.html')

@app.route('/tempi')
def tempi():
    if 'username' not in session:
        return redirect('/login')

    db = get_db()
    tempi_utente = db.execute('''
        SELECT tempo, data 
        FROM TEMPI 
        WHERE utente_id = (SELECT ID FROM UTENTI WHERE username = ?)
        ORDER BY data DESC
    ''', (session['username'],)).fetchall()
    db.close()

    return render_template('tempi.html', tempi=tempi_utente)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect('/login')

@app.template_filter('format_date')
def format_date(value):
    try:
        data = datetime.strptime(value, "%Y-%m-%d")
        mesi = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno",
                "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"]
        return f"{data.day} {mesi[data.month - 1]} {data.year}"
    except:
        return value  # Se il formato è errato, restituisce il valore originale

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
