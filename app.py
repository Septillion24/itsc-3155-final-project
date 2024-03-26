from flask import Flask, abort, redirect, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/test1')
def test1():
    return render_template("index.html", test1=True)

@app.route('/test2')
def test2():
    return render_template("index.html", test2=True)

@app.route('/test3')
def test3():
    return render_template("index.html", test3=True)

@app.route('/signup')
def signup():
    return render_template("signup.html")