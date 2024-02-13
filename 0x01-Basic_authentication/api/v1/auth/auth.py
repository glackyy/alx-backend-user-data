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
        elif excluded_paths is None or excluded_paths == []:
            return True
        elif path in excluded_paths:
            return False
        else:
            for i in excluded_paths:
                if i.startswith(path):
                    return False
                if path.startswith(i):
                    return False
                if i[-1] == "*":
                    if path.startswith(i[:-1]):
                        return False