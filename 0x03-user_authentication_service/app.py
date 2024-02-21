#!/usr/bin/env python3
"""Flask App"""
from flask import (
    Flask,
    jsonify
)

app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def index() -> str:
    """Returning json response"""
    return jsonify({"message": "Bienvenue"})
