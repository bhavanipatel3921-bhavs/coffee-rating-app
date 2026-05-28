from flask import Flask, render_template, redirect
import sqlite3

app = Flask(__name__)

# DATABASE CREATE
def init_db():
    conn = sqlite3.connect('coffee.db')
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS coffee (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            votes INTEGER
        )
    ''')

    coffees = [
        ('Cappuccino', 0),
        ('Espresso', 0),
        ('Latte', 0),
        ('Mocha', 0)
    ]

    cur.execute("SELECT COUNT(*) FROM coffee")
    count = cur.fetchone()[0]

    if count == 0:
        cur.executemany(
            "INSERT INTO coffee (name, votes) VALUES (?, ?)",
            coffees
        )

    conn.commit()
    conn.close()

# CALL DATABASE
init_db()

# HOME PAGE
@app.route('/')
def home():

    conn = sqlite3.connect('coffee.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM coffee")
    coffees = cur.fetchall()

    conn.close()

    return render_template('index.html', coffees=coffees)

# VOTE FUNCTION
@app.route('/vote/<int:id>')
def vote(id):

    conn = sqlite3.connect('coffee.db')
    cur = conn.cursor()

    cur.execute(
        "UPDATE coffee SET votes = votes + 1 WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/')

# RUN APP
if __name__ == '__main__':
    app.run(debug=True)