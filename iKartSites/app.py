from flask import Flask, render_template, request, redirect, url_for, session
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'x'  # Necessaria per usare le sessioni

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with open('utenti.json') as f:
            utenti = json.load(f)

        if username in utenti and utenti    [username] == password:
            session['username'] = username
            return redirect('/tempi')
        else:
            return 'Login fallito'

    return render_template('login.html')

@app.route('/tempi')
def tempi():
    if 'username' not in session:
        return redirect('/login')

    username = session['username']

    try:
        with open('tempi.json', 'r') as f:
            tutti_i_tempi = json.load(f)
            tempi_utente = tutti_i_tempi.get(username, [])
    except Exception as e:
        print(f"Errore nel caricamento di tempi.json: {e}")
        tempi_utente = []

    return render_template('tempi.html', tempi=tempi_utente)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')
##
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
    app.run(debug=True)
