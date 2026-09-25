import sqlite3 as sql
from pathlib import Path
from flask import Flask, render_template, redirect

app = Flask(__name__)

folder = Path(__file__).resolve().parent
db = "pokemon.db"

def get_db():
    conn = sql.connect(folder/db)
    conn.row_factory = sql.Row
    return conn

@app.route("/pokedex")
def pokedex():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""select * from pokemon""")
    pokemon = cursor.fetchall()
    conn.close()

    return render_template("pokedex.html", pokemon=pokemon)

if __name__ == "__main__":
    app.run(debug=True)