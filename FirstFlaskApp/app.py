from flask import Flask, render_template, request; import random; from datetime import datetime; import time

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
    return render_template("404.html", err=e.code, page_name=request.path)

@app.route("/date")
def date():
    return str(datetime.now())

@app.route("/posts/<int:post_id>")
def post(post_id):
    return str(post_id)

@app.route("/times/<int:number>") 
def times_table(number): 
    output = "<h1>The " + str(number) + " times table</h1>" 
    for i in range(1, 13): 
        answer = str(i * number) 
        sum = str(i) + " x " + str(number) 
        output += "<p>" + sum + " = " + answer + "</p>" 
    return output

@app.route("/add/<x>/<y>")
def add(x, y):
    return str(int(x) + int(y))

@app.route("/dice/<int:sides>")
def dice(sides):
    return str(random.randint(1, sides))

app.run(debug=True)