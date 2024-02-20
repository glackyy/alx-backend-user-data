#!/usr/bin/env python3
"""Declaring a SQLAlchemy user corresponding to db "users" """
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    Integer,
    String,
)

Base = declarative_base()

