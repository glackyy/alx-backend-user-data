#!/usr/bin/env python3
"""_hash_password function"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound

from db import DB


def _hash_password(password: str) -> bytes:
    """Hashing a passwd str and returning it in bytes"""
    passwd = password.encode('utf-8')
    return bcrypt.hashpw(passwd, bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()