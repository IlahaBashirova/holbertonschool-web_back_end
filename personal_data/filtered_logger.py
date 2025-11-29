#!/usr/bin/env python3
"""Module for filtering and logging personal data safely."""

import logging
import os
import re
from typing import List, Tuple

import mysql.connector
from mysql.connector.connection import MySQLConnection


# Fields from user_data.csv that are considered PII
PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Return the log message with specified fields redacted."""
    pattern = (
        rf"({'|'.join(map(re.escape, fields))})="
        rf"[^{re.escape(separator)}]*"
    )
    return re.sub(
        pattern,
        lambda m: f"{m.group(1)}={redaction}",
        message,
    )


class RedactingFormatter(logging.Formatter):
    """Logging Formatter that redacts PII fields from log records."""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]) -> None:
        """Initialize the formatter with a list of fields to redact."""
        super().__init__(self.FORMAT)
        self.fields: List[str] = fields

    def format(self, record: logging.LogRecord) -> str:
        """Apply redaction to the log record and format it."""
        record.msg = filter_datum(
            self.fields,
            self.REDACTION,
            record.getMessage(),
            self.SEPARATOR,
        )
        return super().format(record)


def get_logger() -> logging.Logger:
    """Create and configure a logger for user data."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))

    # Avoid duplicate handlers when tests import multiple times
    logger.handlers.clear()
    logger.addHandler(handler)

    return logger


def get_db() -> MySQLConnection:
    """Return a connection to the MySQL database."""
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
