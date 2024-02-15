#!/usr/bin/env python3
"""SessionAuth Class"""
from typing import TypeVar
from uuid import uuid4
from .auth import Auth
from models.user import User

class SessionAuth(Auth):
    """Implementing session auth methods"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creating a session id for a user with user_id"""
        if user_id is None or not isinstance(user_id, str):
            return None
        id = uuid4()
        self.user_id_by_session_id[str(id)] = user_id
        return str(id)

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returning a user id based on a session id"""
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Returning a user instance based on a cookie val"""
        session_ck = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_ck)
        user = User.get(user_id)
        return user
