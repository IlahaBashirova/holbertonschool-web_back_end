#!/usr/bin/env python3
"""Module for filtering sensitive fields from log messages."""

import re
from typing import List


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """Return message with values of `fields` replaced by `redaction`."""
    sep = re.escape(separator)
    pattern = f"({'|'.join(map(re.escape, fields))})=[^{sep}]*"
    return re.sub(pattern, lambda match: f"{match.group(1)}={redaction}", message)
