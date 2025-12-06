#!/usr/bin/env python3
"""SessionAuth module"""

from typing import TypeVar
from urllib import response
from api.v1.auth.auth import Auth
import uuid
from models.user import User
from flask import jsonify, request
from os import getenv


class SessionAuth(Auth):
    """SessionAuth class that inherits from Auth (empty for now)"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Create a Session ID for a user_id
        Args:
            user_id (str): The user ID"""
        if user_id is None:
            return None
        if type(user_id) is not str:
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retrieve a User ID based on a Session ID"""
        if session_id is None:
            return None
        if type(session_id) is not str:
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Retrieve the User instance based on a cookie value"""
        session_id = self.session_cookie(request)
        if session_id is None:
            return None
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None
        return User.get(user_id)

    @app_views.route(
            '/auth_session/login', methods=['POST'], strict_slashes=False)
    def auth_session_login():
        """
        POST /api/v1/auth_session/login
        Login using email + password, create a session,
        return the user JSON and set the session cookie.
        """
        email = request.form.get("email")
        password = request.form.get("password")
        if email is None or email == "":
            return jsonify({"error": "email missing"}), 400
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
            session_name = "_my_session_id"

        response.set_cookie(session_name, session_id)

        return response
