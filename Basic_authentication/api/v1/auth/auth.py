#!/usr/bin/env python3
"""Authentication module
"""
from typing import List, TypeVar


try:
    from flask import request
except ImportError:
    request = None


User = TypeVar('User')


class Auth:
    """Authentication class to manage the API authentication.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determine if a given path requires authentication.
        Returns True if authentication is required, False otherwise.
        """
        # If path is None -> require authentication
        if path is None:
            return True

        # If excluded_paths is None or empty -> require authentication
        if not excluded_paths:
            return True

        # Make path slash-tolerant: always end with '/'
        if not path.endswith('/'):
            path += '/'

        # Compare against each excluded path (also normalize if needed)
        for ex in excluded_paths:
            if ex is None:
                continue

            # Ensure excluded path also ends with '/'
            if not ex.endswith('/'):
                ex += '/'

            if path == ex:
                # Path is excluded -> no auth required
                return False

        # If no match -> auth required
        return True


    def authorization_header(self, request=None) -> str:
        """Return the authorization header."""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Return the current user."""
        return None
