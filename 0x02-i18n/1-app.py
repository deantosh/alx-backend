#!/usr/bin/env python3
"""
Task 0:
Setup a basic Flask app in 0-app.py:
 - a single / route and an
 - index.html template that simply outputs “Welcome to Holberton” as page title
  (<title>) and "Hello world" as header (<h1>).

Task 1:
Then instantiate the Babel object in your app. Store it in a module-level
variable named babel.
In order to configure available languages in our app, you will create a
Config class
that has a LANGUAGES class attribute equal to ["en", "fr"].
Use Config to set Babel’s default locale ("en") and timezone ("UTC").
Use that class as config for your Flask app.
"""
from flask_babel import Babel
from flask import Flask, render_template


class Config:
    """APPlication configuration class."""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@app.route('/')
def index_page():
    """Returns a welcome page"""
    render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
