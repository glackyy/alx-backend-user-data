#!/usr/bin/env python3
"""SessionAuth Class"""
from uuid import uuid4
from .auth import Auth


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
