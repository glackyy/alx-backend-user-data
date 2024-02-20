#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Creating a user obj and save it to the db"""
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Returning a user attrib that matches the attrib
        passed as args"""
        all_users = self._session.query(User)
        for key, val in kwargs.items():
            if key not in User.__dict__:
                raise InvalidRequestError
            for user in all_users:
                if getattr(user, key) == val:
                    return user
        raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """Updating a user attrib"""
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError()
        for k, val in kwargs.items():
            if hasattr(user, k):
                setattr(user, k, val)
            else:
                raise ValueError
        self._session.commit()
