#!/usr/bin/env python3
"""Auth Class"""
from flask import request
from typing import (
    List,
    TypeVar
)


class Auth:
    """Managing the API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determining whether a given path requires auth or not"""
        if path is None:
            return True