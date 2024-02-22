#!/usr/bin/env python3
"""Main File"""
import requests


def register_user(email: str, password: str) -> None:
    """Testing register a usr with given email and password"""
    res = requests.post('http://127.0.0.1:5000/users',
                        data={'email': email, 'password': password})
    if res.status_code == 200:
        assert (res.json() == {"email": email, "message": "user created"})
    else:
        assert(res.status_code == 400)
        assert (res.json() == {"message": "email already registered"})
