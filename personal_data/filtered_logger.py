#!/usr/bin/env python3
"""Tools for filtering and logging personal data safely."""

import logging
import os
import re
from typing import List, Tuple

import mysql.connector
from mysql.connector.connection import MySQLConnection


PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """Replace the values of specified fields in a log message.

    Each field is expected to appear as ``field=value`` and be separated by
    ``separator``. The returned string is the same message where the values
    of all fields present in ``fields`` are replaced by ``redaction``.
    """
    pattern = f"({'|'.join(fields)})=[^{separator}]*"
    return re.sub(
        pattern,
        lambda match: f"{match.group(1)}={redaction}",
        message,
    )


class RedactingFormatter(logging.Formatter):
    """Logging Formatter that redacts sensitive fields in log records."""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]) -> None:
        """Initialize the formatter with the list of fields to redact."""
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format a log record with sensitive fields redacted."""
        redacted = filter_datum(
            self.fields,
            self.REDACTION,
            record.getMessage(),
            self.SEPARATOR,
        )
        record.msg = redacted
        return super().format(record)


def get_logger() -> logging.Logger:
    """Create and configure a logger named ``user_data``.

    The logger logs messages with level INFO or higher, does not propagate
    to parent loggers, and has a single :class:`StreamHandler` using
    :class:`RedactingFormatter` configured with :data:`PII_FIELDS`.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))

    logger.handlers = []
    logger.addHandler(handler)

    return logger


def get_db() -> MySQLConnection:
    """Create a MySQL connection using credentials from environment vars.

    Environment variables:
        PERSONAL_DATA_DB_USERNAME: database user (default: "root")
        PERSONAL_DATA_DB_PASSWORD: database password (default: "")
        PERSONAL_DATA_DB_HOST: database host (default: "localhost")
        PERSONAL_DATA_DB_NAME: database name (no default)
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=db_name,
    )
