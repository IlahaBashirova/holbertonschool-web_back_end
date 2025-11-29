#!/usr/bin/env python3
"""Module for filtering and logging personal data safely."""

import logging
import os
import re
from typing import List

import mysql.connector
from mysql.connector.connection import MySQLConnection


# Fields from user_data.csv that are considered PII
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """Return message with values of specified fields redacted."""
    pattern = "({})=[^{}]*".format("|".join(fields), separator)
    return re.sub(pattern, r"\1={}".format(redaction), message)


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class."""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]) -> None:
        """Initialize the formatter with a list of fields to redact."""
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filter values in the log record."""
        msg = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                            msg, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """Return a configured logger for user data."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))

    logger.handlers = []
    logger.addHandler(handler)
    return logger


def get_db() -> MySQLConnection:
    """Return a connector to the MySQL database."""
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


def main() -> None:
    """Obtain a DB connection and display filtered rows from users table."""
    db = get_db()
    cursor = db.cursor()
    query = ("SELECT name, email, phone, ssn, password, ip, "
             "last_login, user_agent FROM users;")
    cursor.execute(query)

    logger = get_logger()
    fields = ("name", "email", "phone", "ssn",
              "password", "ip", "last_login", "user_agent")

    for row in cursor:
        message = "; ".join(
            "{}={}".format(field, value) for field, value in zip(fields, row)
        )
        logger.info(message)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
