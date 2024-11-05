#!/usr/bin/env python3
"""
Based on the inferred time zone, display the current time on the home page in
the default format. For example:
  - Jan 21, 2020, 5:55:39 AM or 21 janv. 2020 à 05:56:28
"""
from flask import render_template, g
from datetime import datetime
import pytz
from babel.dates import format_datetime


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
