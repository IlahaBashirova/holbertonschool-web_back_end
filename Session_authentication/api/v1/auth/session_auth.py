#!/usr/bin/env python3
"""SessionAuth module"""

from typing import TypeVar
from api.v1.auth.auth import Auth
import uuid


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
