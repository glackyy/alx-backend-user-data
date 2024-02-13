#!/usr/bin/env python3
"""Module Index"""
from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """Getting api/v1/status"""
    return jsonify({"status": "OK"})
