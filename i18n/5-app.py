#!/usr/bin/env python3
"""Get locale from request"""

from typing import Optional, Dict, Any
from flask import Flask, render_template, request, g
from flask_babel import Babel


class Config:
    """Configuration for babel"""
    LANGUAGES = ["en", "fr"]
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


@babel.localeselector
def get_locale() -> str:
    """Select the best language match"""
    locale = request.args.get("locale")
    if locale in app.config["LANGUAGES"]:
        return locale
    return request.accept_languages.best_match(app.config["LANGUAGES"])


def get_user() -> Optional[Dict[str,Any]]:
    """Return a user dict"""
    login_as = request.args.get("login_as")
    if login_as is None:
        return None
    try:
        user_id = int(login_as)
    except ValueError:
        return None
    return users.get(user_id)


babel.init_app(app, locale_selector=get_locale)

@app.before_request
def before_request() -> None:
    """Runs before every request, sets g.user"""
    g.user = get_user()


@app.route('/')
def index():
    """Render index page"""
    return render_template('5-index.html')


if __name__ == '__main__':
    app.run()
