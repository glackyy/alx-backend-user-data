#!/usr/bin/env python3
"""SessionExpAuth class"""
from .session_auth import SessionAuth
import os

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