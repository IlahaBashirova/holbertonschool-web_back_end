#!/usr/bin/env python3
"""Auth module - password hashing with bcrypt.
"""
import uuid
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Hash a password using bcrypt."""
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """A new Auth instance with its own DB object"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user"""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user
        else:
            raise ValueError("User {} already exists", format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """Check if a login password matches."""
        try:
            user = self._db.find_user_by(email=email)
            password_bytes = password.encode("utf-8")
            return bcrypt.checkpw(password_bytes, user.hashed_password)
        except Exception:
            return False

    def _generate_uuid() -> str:
        """Generate a new UUID and return its string representation."""
        return str(uuid.uuid4())

    def create_session(self, email: str) -> str:
        """Generate a new UUID."""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id
