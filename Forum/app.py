import sqlite3 as sql
from pathlib import Path
from flask import Flask, render_template, redirect

app = Flask(__name__)

PROJECT_FOLDER = Path(__file__).resolve().parent
DB = "forum.db"

def init_db():
    conn = sql.connect(PROJECT_FOLDER/DB)
    conn.execute("""create table if not exists posts (
    post_id integer primary key,
    author text not null,
    message text not null)""")
    conn.commit()
    conn.close()

init_db()

def get_db():
    conn = sql.connect(PROJECT_FOLDER/DB)
    conn.row_factory = sql.Row
    return conn

@app.route("/")
def to_forum():
    return redirect("/forum")

@app.route("/forum")
def forum():
    conn = get_db()
    posts = conn.execute("select * from posts order by post_id desc").fetchall()
    conn.close()
    return render_template("forum.html", posts=posts)

if __name__ == "__main__":
    app.run(debug=True)