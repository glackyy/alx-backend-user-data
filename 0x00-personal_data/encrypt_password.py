#!/usr/bin/env python3
"""Defining a hash_password to return a hashed password"""
import bcrypt
from bcrypt import hashpw


def hash_password(password: str) -> bytes:
    """Returning a hashed password"""
    bc = password.encode()
    hashed = hashpw(bc, bcrypt.gensalt())
    return hashed
