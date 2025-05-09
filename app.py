# app.py
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# --- db setup ---
def init_db():
    with sqlite3.connect('data.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS personas (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nombre TEXT NOT NULL,
                            edad INTEGER NOT NULL
                        );''')

# --- routes ---
@app.route('/')
def index():
    conn = sqlite3.connect('data.db')
    personas = conn.execute('SELECT * FROM personas').fetchall()
    conn.close()
    return render_template('index.html', personas=personas)

@app.route('/persona/<int:id>')
def persona(id):
    conn = sqlite3.connect('data.db')
    persona = conn.execute('SELECT * FROM personas WHERE id=?', (id,)).fetchone()
    conn.close()
    return render_template('persona.html', persona=persona)

@app.route('/agregar', methods=['POST'])
def agregar():
    nombre = request.form['nombre']
    edad = request.form['edad']
    conn = sqlite3.connect('data.db')
    conn.execute('INSERT INTO personas (nombre, edad) VALUES (?, ?)', (nombre, edad))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    conn = sqlite3.connect('data.db')
    if request.method == 'POST':
        nombre = request.form['nombre']
        edad = request.form['edad']
        conn.execute('UPDATE personas SET nombre=?, edad=? WHERE id=?', (nombre, edad, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        persona = conn.execute('SELECT * FROM personas WHERE id=?', (id,)).fetchone()
        conn.close()
        return render_template('editar.html', persona=persona)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    conn = sqlite3.connect('data.db')
    conn.execute('DELETE FROM personas WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)