#!/usr/bin/env python3
"""Session authentication views
"""

from os import getenv

from flask import jsonify, request, abort

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
    # 1) Get email
    email = request.form.get("email")
    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400

    # 2) Get password
    password = request.form.get("password")
    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400

    # 3) Find user by email
    users = User.search({"email": email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]

    # 4) Check password
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # 5) Create session (import here to avoid circular import)
    from api.v1.app import auth

    session_id = auth.create_session(user.id)

    # 6) Build response with user JSON
    response = jsonify(user.to_json())

    # 7) Set cookie with session id
    session_name = getenv("SESSION_NAME")
    response.set_cookie(session_name, session_id)

    return response


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def auth_session_logout():
    """
    DELETE /api/v1/auth_session/logout
    Destroy the user session (logout).
    """
    # Import here to avoid circular import
    from api.v1.app import auth

    if not auth.destroy_session(request):
        abort(404)

    return jsonify({}), 200
