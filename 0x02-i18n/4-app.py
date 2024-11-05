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
In order to configure available languages in our app, you will create a Config
class that has a LANGUAGES class attribute equal to ["en", "fr"].
Use Config to set Babel’s default locale ("en") and timezone ("UTC").
Use that class as config for your Flask app.

Task 2:
Create a get_locale function with the babel.localeselector decorator. Use
request.accept_languages to determine the best match with our supported
languages.

Task 3:
Use the _ or gettext function to parametrize your templates. Use the message
IDs home_title and home_header.
Create a babel.cfg file containing

Task 4:
In this task, you will implement a way to force a particular locale by
passing the locale=fr parameter to your app’s URLs.

In your get_locale function, detect if the incoming request contains locale
argument and ifs value is a supported locale, return it. If not or if the
parameter is not present, resort to the previous default behavior.
"""
from flask_babel import Babel
from flask import Flask, render_template, request


class Config:
    """APPlication configuration class."""
    LANGUAGES = ["en", "es", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)

babel = Babel(app)


@babel.localeselector
def get_locale():
    """Automatically detect and return the best match with supported locales"""
    locale_param = requests.args.get("locale")

    if locale_param in app.cofig["LANGUAGES"]:
        return locale_param

    # Fallback to the default behavior
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route('/')
def index_page():
    """Returns a welcome page"""
    home_title = gettext("Welcome to Holberton")
    home_header = gettext("Hello world")
    render_template('index.html', title=home_title, header=home_header)


if __name__ == "__main__":
    app.run(debug=True)
