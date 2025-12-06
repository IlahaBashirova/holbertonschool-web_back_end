#!/usr/bin/env python3
"""Session authentication views
"""

from os import getenv

from flask import jsonify, request

from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login',
                 methods=['POST'], strict_slashes=False)
def auth_session_login():
    """
    POST /api/v1/auth_session/login
    Login using email + password, create a session,
    return the user JSON and set the session cookie.
    """
    email = request.form.get("email")
    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400

    password = request.form.get("password")
    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400

    users = User.search({"email": email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]

    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth

    session_id = auth.create_session(user.id)

    response = jsonify(user.to_json())

    session_name = getenv("SESSION_NAME")
    if session_name is None:
        session_name = "_my_session_id"  # optional default

    response.set_cookie(session_name, session_id)

    return response
