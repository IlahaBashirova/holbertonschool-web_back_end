#!/usr/bin/env python3

from flask import request
from typing import List, TypeVar

User= TypeVar('User')

class Auth:
    """Authentication class to manage the API authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determine if a given path requires authentication.

        For now:
            - ignore the values of `path` and `excluded_paths`
            - always return False
        These arguments will be used in later tasks.
        """
        return False
    

    def authorization_header(self, request=None) -> str:
        """
        Return the authorization header from a request.

        If request is None, return None.
        If the header is not present, return None.
        Otherwise, return the value of the header.
        """
        return None
    

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Return the current user.

        For now, return None.
        This method will be implemented in later tasks.
        """
        return None
    