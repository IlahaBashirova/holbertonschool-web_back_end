#!/usr/bin/env python3
"""Use user locale"""

from typing import Optional, Dict, Any
from flask import Flask, render_template, request, g
from flask_babel import Babel
import pytz


class Config:
    """Babel configuration"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)

babel = Babel()

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user() -> Optional[Dict[str, Any]]:
    """Return a user dict or None"""
    login_as = request.args.get("login_as")
    if login_as is None:
        return None
    try:
        user_id = int(login_as)
    except ValueError:
        return None
    return users.get(user_id)


@app.before_request
def before_request() -> None:
    """Set g.user before each request"""
    g.user = get_user()


def get_locale() -> str:
    """Select best locale with priority:
    """
    locale = request.args.get("locale")
    if locale in app.config["LANGUAGES"]:
        return locale

    if g.user:
        user_locale = g.user.get("locale")
        if user_locale in app.config["LANGUAGES"]:
            return user_locale

    header_locale = request.accept_languages.best_match(
        app.config["LANGUAGES"])
    if header_locale:
        return header_locale

    return app.config["BABEL_DEFAULT_LOCALE"]


def get_timezone() -> str:
    """Return best timezone"""
    def is_valid_tz(tz: str) -> bool:
        try:
            pytz.timezone(tz)
            return True
        except pytz.exceptions.UnknownTimeZoneError:
            return False
    tz = request.args.get("timezone")
    if tz and is_valid_tz(tz):
        return tz
    if g.user:
        user_tz = g.user.get("timezone")
        if user_tz and is_valid_tz(user_tz):
            return user_tz

    return "UTC"


babel.init_app(app, locale_selector=get_locale)


@app.route('/')
def index() -> str:
    """Render index page"""
    return render_template('6-index.html')


if __name__ == '__main__':
    app.run()
