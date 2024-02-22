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
        assert (res.status_code == 400)
        assert (res.json() == {"message": "email already registered"})


def log_in_wrong_password(email: str, password: str) -> None:
    """Testing login with the given wrong credentials"""
    response = requests.post('http://127.0.0.1:5000/sessions',
                             data={'email': email, 'password': password})
    assert (response.status_code == 401)


def log_in(email: str, password: str) -> str:
    """Testing log in with the correct credentials"""
    res = requests.post('http://127.0.0.1:5000/sessions',
                        data={'email': email, 'password': password})
    assert (res.status_code == 200)
    assert (res.json() == {"email": email, "message": "logged in"})
    assert res.cookies['session_id']


def profile_unlogged() -> str:
    """Testing for profile without being logged in with
    session id"""
    resp = requests.get('http://127.0.0.1:5000/profile')
    assert (resp.status_code == 403)


def profile_logged(session_id: str) -> None:
    """Testing for profile with being logged in
    with session id"""
    cookies = {'session_id': session_id}
    resp = requests.delete('http://127.0.0.1:5000/profile',
                           cookies=cookies)
    assert (resp.status_code == 200)


def log_out(session_id: str) -> None:
    """Testing for log out with the given session_id"""
    cookies = {'session_id': session_id}
    resp = requests.delete('http://127.0.0.1:5000/sessions',
                           cookies=cookies)
    if resp.status_code == 302:
        assert (resp.url == 'http://127.0.0.1:5000/')
    else:
        assert (resp.status_code == 200)


def reset_password_token(email: str) -> str:
    """Testing for rest password token with the given
    email"""
    resp = requests.post('http://127.0.0.1:5000/reset_password',
                         data={'email': email})
    if resp.status_code == 200:
        return resp.json()['reset_token']
    assert (resp.status_code == 401)


def update_password(email: str, reset_token: str,
                    new_password: str) -> str:
    """Testing for update password with the given
    email, reset_token, new_password"""
    data = {'email': email, 'reset_token': reset_token,
            'new_password': new_password}
    resp = requests.put('http://127.0.0.1:5000/reset_password',
                        data=data)
    if resp.status_code == 200:
        assert (resp.json() == {"email": email, "message": "Password updated"})
    else:
        assert (resp.status_code == 203)


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
