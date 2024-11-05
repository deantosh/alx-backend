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

Task 7:
Define a get_timezone function and use the babel.timezoneselector decorator.
The logic should be the same as get_locale:
 - Find timezone parameter in URL parameters
 - Find time zone from user settings
 - Default to UTC
Before returning a URL-provided or user time zone, you must validate that it
is a valid time zone. To that, use pytz.timezone and catch the
pytz.exceptions.UnknownTimeZoneError exception.

Task 8:
Based on the inferred time zone, display the current time on the home page in
the default format. For example:
  - Jan 21, 2020, 5:55:39 AM or 21 janv. 2020 à 05:56:28
"""
import pytz
from pytz import timezone
from flask_babel import Babel
from babel.dates import format_datetime
from datetime import datetime
from flask import Flask, render_template, request, g
from pytz.exceptions import UnknownTimeZoneError


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


@babel.timezoneselector
def get_timezone():
    """Automatically detect and return the best match with supported timezones.
    """
    # Check if there's a timezone in the URL parameters
    timezone_param = request.args.get("timezone")

    # Validate timezone from URL parameters
    if timezone_param:
        try:
            tz = timezone(timezone_param)  # Validate the timezone
            return tz.zone  # Return the validated timezone name
        except UnknownTimeZoneError:
            pass  # If it's not valid, fall through to the next option

    # Check if the user is logged in and has a preferred timezone
    if g.user and g.user.get('timezone'):
        try:
            tz = timezone(g.user['timezone'])  # Validate the user's timezone
            return tz.zone  # Return the validated timezone name
        except UnknownTimeZoneError:
            pass  # If it's not valid, fall through to the default

    # Default to UTC if no valid timezone is found
    return 'UTC'


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


@app.route('/')
def home():
    # Get the timezone from the `get_timezone` function
    tzname = get_timezone()
    timezone = pytz.timezone(tzname)

    # Get the current time in the inferred timezone
    current_time = datetime.now(timezone)

    # Format the current time according to the user's locale
    formatted_time = format_datetime(current_time, locale=get_locale())

    return render_template('index.html', current_time=formatted_time)


if __name__ == "__main__":
    app.run(debug=True)
