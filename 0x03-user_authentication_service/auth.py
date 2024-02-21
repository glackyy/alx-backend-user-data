#!/usr/bin/env python3
"""_hash_password function"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Hashing a passwd str and returning it in bytes"""
    passwd = password.encode('utf-8')
    return bcrypt.hashpw(passwd, bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registration of a new user and returning a user obj"""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            h_pass = _hash_password(password)
            user = self._db.add_user(email, h_pass)
            return user
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """Validating a user login credentials and returning True
        if correct or false if not"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        user_pwd = user.hashed_password
        passwd = password.encode("utf-8")
        return bcrypt.checkpw(passwd, user_pwd)
