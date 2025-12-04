#!/usr/bin/env python3
"""Main_1 py"""
from api.v1.auth.auth import Auth

a = Auth()

print(a.require_auth(None, None))                               # True
print(a.require_auth(None, []))                                 # True
print(a.require_auth("/api/v1/status/", []))                    # True
print(a.require_auth("/api/v1/status/", ["/api/v1/status/"]))   # False
print(a.require_auth("/api/v1/status", ["/api/v1/status/"]))    # False
print(a.require_auth("/api/v1/status/", ["/api/v1/status"]))    # False
print(a.require_auth("/api/v1/status/", ["/api/v1/status/", "/api/v1/stats"]))  # True
