#!/usr/bin/env python3
"""SessionExpAuth class"""
from .session_auth import SessionAuth
import os
from datetime import (
    datetime,
    timedelta
)


class SessionExpAuth(SessionAuth):
    """Defining class SEA that adds an
    exp date to a session id"""
    def __init__(self):
        """Initializing the class"""
        try:
            duration = int(os.getenv('SESSION_DURATION'))
        except Exception:
            duration = 0
        self.session_duration = duration

    def create_session(self, user_id: None):
        """Creating a session id for user"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dict = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id: None):
        """Returning a user id based on a session id"""
        if session_id is None:
            return None
        user_details = self.user_id_by_session_id.get(session_id)
        if user_details is None:
            return None
        if "created_at" not in user_details.keys():
            return None
        if self.session_duration <= 0:
            return user_details.get("user_id")
        created_at = user_details.get("created_at")
        allow_window = created_at + timedelta(seconds=self.session_duration)
        if allow_window < datetime.now():
            return None
        return user_details.get("user_id")
