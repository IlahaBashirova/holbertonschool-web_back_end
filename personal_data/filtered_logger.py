#!/usr/bin/env python3
"""Module for filtering sensitive fields from log messages."""

import logging
import re
from typing import List


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """Return message with values of specified fields redacted."""
    sep = re.escape(separator)
    pattern = f"({'|'.join(map(re.escape, fields))})=[^{sep}]*"
    return re.sub(pattern, lambda m: m.group(1) + '=' + redaction, message)


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class."""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize the formatter with a list of fields to redact."""
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filter values in the log record."""
        msg = filter_datum(self.fields, self.REDACTION,
                           record.getMessage(), self.SEPARATOR)
        record.msg = msg
        return super().format(record)
