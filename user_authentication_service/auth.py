#!/usr/bin/env python3
"""Auth module - password hashing with bcrypt.
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hash a password using bcrypt."""
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed
