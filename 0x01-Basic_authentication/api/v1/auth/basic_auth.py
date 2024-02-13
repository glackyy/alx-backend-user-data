#!/usr/bin/env python3
"""Class BasicAuth"""
import base64
from .auth import Auth
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """Implementing Basic Auth methods"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extracting the base64 part of the authorization header for a basic auth"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        tk = authorization_header.split(" ")[-1]
        return tk

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """Decoding a base64 encoded str"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            dd = base64_authorization_header.encode('utf-8')
            dd = base64.b64encode(dd)
            return dd.decode('utf-8')
        except Exception:
            return None

