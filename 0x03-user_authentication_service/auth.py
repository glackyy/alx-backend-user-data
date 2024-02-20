#!/usr/bin/env python3
"""_hash_password function"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hashing a passwd str and returning it in bytes"""
    passwd = password.encode('utf-8')
    return bcrypt.hashpw(passwd, bcrypt.gensalt())
 