#!/usr/bin/env python3
"""Get locale from request"""


from flask import Flask, render_template, request
from flask_babel import Babel


class Config:
    """Configuration for babel"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)

babel = Babel(app)

def get_locale() -> str:
    """Select the best language match"""
    return request.accept_languages.best_match(app.config["LANGUAGES"])

babel.init_app(app, locale_selector=get_locale)


@app.route('/')
def index():
    """Render index page"""
    return render_template('1-index.html')


if __name__ == '__main__':
    app.run()
