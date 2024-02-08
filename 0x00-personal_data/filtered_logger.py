#!/usr/bin/env python3
"""filtered logger module"""
from typing import List
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Returning an obfuscated log msg"""
    for field in fields:
        message = re.sub(field+'=.*?'+separator,
                         field+'='+redaction+separator, message)
    return message
