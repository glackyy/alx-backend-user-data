#!/usr/bin/env python3
"""class SessionDBauth"""
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Defining a SessionDBAuth class that persists
    session data in db"""
    def create_session(self, user_id: None):
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        kwargs = {
            "user_id": user_id,
            "session_id": session_id
        }
        user = UserSession(**kwargs)
        user.save()
        return session_id

    def user_id_for_session_id(self, session_id: None):
        """Returning a user id based on a session id"""
        user_id = UserSession.search({"session_id": session_id})
        if user_id:
            return user_id
        return None
