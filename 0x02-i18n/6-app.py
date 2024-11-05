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

Task 5:
Define a get_user function that returns a user dictionary or None if the ID
cannot be found or if login_as was not passed.
Define a before_request function and use the app.before_request decorator
to make it be executed before all other functions. before_request should use
get_user to find a user if any, and set it as a global on flask.g.user.

Task 6:
Change your get_locale function to use a user’s preferred local if it is
supported.
The order of priority should be
 - Locale from URL parameters
 - Locale from user settings
 - Locale from request header
 - Default locale
Test by logging in as different users
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


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user():
    """
    Returns a user dictionary or None if the ID cannot be found or
    if login_as was not passed.
    """
    user_id = request.args.get('login_as')
    if user_id is None:
        return None

    try:
        user_id = int(user_id)
    except ValueError:
        return None

    return users.get(user_id)


@app.before_request
def before_request():
    """Function to run before each request."""
    g.user = get_user()  # Set the global user object in Flask's g


@babel.localeselector
def get_locale():
    """Automatically detect and return the best match with supported locales"""
    locale_param = requests.args.get("locale")
    if locale_param in app.cofig["LANGUAGES"]:
        return locale_param

    # Check if the user is logged in and has a preferred locale
    if g.user and g.user.get('locale') in app.config["LANGUAGES"]:
        return g.user['locale']

    # Fallback to the default behavior
    best_match = request.accept_languages.best_match(app.config["LANGUAGES"])
    if best_match:
        return best_match

    # Default locale if none of the above match
    return app.config["BABEL_DEFAULT_LOCALE"]


@app.route('/')
def index_page():
    """Returns a welcome page"""
    home_title = gettext("Welcome to Holberton")
    home_header = gettext("Hello world")
    render_template('index.html', title=home_title, header=home_header)


if __name__ == "__main__":
    app.run(debug=True)
