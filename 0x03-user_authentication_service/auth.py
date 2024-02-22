#!/usr/bin/env python3
"""_hash_password function"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound

from typing import Union, TypeVar
from db import DB
from user import User
from uuid import uuid4

u = TypeVar(User)


def _hash_password(password: str) -> bytes:
    """Hashing a passwd str and returning it in bytes"""
    passwd = password.encode('utf-8')
    return bcrypt.hashpw(passwd, bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generating a uuid and returning a string"""
    return str(uuid4())


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

    def create_session(self, email: str) -> Union[None, str]:
        """Creating a session_id for an existing user and
        updating the user's session_id"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[None, u]:
        """Taking a session id and returning the corresponding
        user, if exists else returning None"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """Taking a user_id and destroying that user's
        session and updating their session id attrib to None"""
        try:
            self._db.update_user(user_id, session_id=None)
        except ValueError:
            return None
        return None

    def get_reset_password_token(self, email: str) -> str:
        """Generating a reset_token uuid for a user
        identified by the given email"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token
