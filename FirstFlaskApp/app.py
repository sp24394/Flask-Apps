from flask import Flask; import random; from datetime import datetime; import time

app = Flask(__name__)

@app.route("/")
def home():
    return "i am so cool"

@app.route("/about")
def about():
    return "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"

@app.route("/p")
def p():
    return "<h1>p</h1>\n<ul><li>p</li></ul>"

@app.route("/calc")
def calc():
    return str(6+7 + random.randint(1, 20))

@app.errorhandler(404)
def error404(e):
    return str(e) + "asdf"

@app.route("/date")
def date():
    return str(datetime.now())

@app.route("/posts/<int:post_id>")
def post(post_id):
    return str(post_id)

app.run(debug=True)