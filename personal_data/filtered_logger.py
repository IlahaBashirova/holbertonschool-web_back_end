#!/usr/bin/env python3
"""Module for filtering sensitive fields from log messages."""

import re
from typing import List


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """Return message with values of specified fields redacted."""
    sep = re.escape(separator)
    pattern = f"({'|'.join(map(re.escape, fields))})=[^{sep}]*"

    def repl(m):
        return m.group(1) + "=" + redaction

    return re.sub(pattern, repl, message)
