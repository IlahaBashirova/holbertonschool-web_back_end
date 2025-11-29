#!/usr/bin/env python3
"""Module for hashing passwords using bcrypt."""

import bcrypt


def hash_password(password: str) -> bytes:
    """Return a salted, hashed password as bytes."""
    encoded = password.encode()
    return bcrypt.hashpw(encoded, bcrypt.gensalt())
