#!/usr/bin/env python3
"""
Setup a basic Flask app in 0-app.py:
 - a single / route and an
 - index.html template that simply outputs “Welcome to Holberton” as page title
  (<title>) and "Hello world" as header (<h1>).
"""
from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def index_page():
    """Returns a welcome page"""
    render_template('index.html', title="Welcome to Holberton", header="Hello world")


if __name__ == "__main__":
    app.run(debug=True)
