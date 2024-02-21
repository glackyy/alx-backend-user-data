#!/usr/bin/env python3
"""Flask App"""
from flask import (
    Flask,
    jsonify,
    request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
