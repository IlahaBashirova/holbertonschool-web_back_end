#!/usr/bin/env python3
"""BasicAuth module
"""

from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """BasicAuth class that inherits from Auth (empty for now)"""
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Extract the Base64 part of the Authorization header
        Return None if the header is None or doesn't start with 'Basic '
        """
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header[6:]  # Remove 'Basic ' prefix
