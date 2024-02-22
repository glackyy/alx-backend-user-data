#!/usr/bin/env python3
"""Flask App"""
from flask import (
    Flask,
    jsonify,
    request,
    abort,
    redirect
)
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def index() -> str:
    """Returning json response"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """Registring new users"""
    email = request.form.get("email")
    passwd = request.form.get("password")
    try:
        user = AUTH.register_user(email, passwd)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": f"{email}", "message": "user created"})


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """Login a user if the credentials provided are correct,
    and creates a new session for that user"""
    email = request.form.get("email")
    passwd = request.form.get("password")
    if not AUTH.valid_login(email, passwd):
        abort(401)
    session_id = AUTH.create_session(email)
    res = jsonify({"email": f"{email}", "message": "logged in"})
    res.set_cookie("session_id", session_id)
    return res


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """Log out a user and destroy their session"""
    session_id = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(session_id)
    if user is None or session_id is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """Returning a user's email based on session_id
    in the received cookies"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": f"{user.email}"}), 200
    abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
