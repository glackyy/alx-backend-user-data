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
        """Extracting the base64 part of the authorization header
        for a basic auth"""
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
            dcoded = base64_authorization_header.encode('utf-8')
            dcoded = base64.b64decode(dcoded)
            return dcoded.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """Returning user email and password from base644 decode val"""
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        email = decoded_base64_authorization_header.split(":")[0]
        password = decoded_base64_authorization_header[len(email) + 1:]
        return (email, password)

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """Returning a user instance based on email and password"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({"email": user_email})
            if not users or users == []:
                return None
            for us in users:
                if us.is_valid_password(user_pwd):
                    return us
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Returning a user instance based on a received request"""
        auth_header = self.authorization_header(request)
        if auth_header is not None:
            tk = self.extract_base64_authorization_header(auth_header)
            if tk is not None:
                dd = self.decode_base64_authorization_header(tk)
                if dd is not None:
                    email, passwd = self.extract_user_credentials(dd)
                    if email is not None:
                        return self.user_object_from_credentials(email, passwd)
        return
