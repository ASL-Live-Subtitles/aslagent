from __future__ import annotations

import os
from typing import Any, Dict

import mysql.connector
from mysql.connector import Error


class MySQLService:
    """Base helper that manages connections to the MySQL database."""

    def __init__(self) -> None:
        self.db_config = self._build_db_config()
        self.connection = self._connect()

    def _build_db_config(self) -> Dict[str, Any]:
        config = {
            "host": os.environ.get("DB_HOST"),
            "user": os.environ.get("DB_USER"),
            "password": os.environ.get("DB_PASSWORD"),
            "database": os.environ.get("DB_NAME"),
            "port": int(os.environ.get("DB_PORT", "3306")),
        }

        missing = [key for key, value in config.items() if value in (None, "")]
        if missing:
            joined = ", ".join(missing)
            raise RuntimeError(
                f"Missing MySQL environment variables: {joined}. "
                "Set DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, and optionally DB_PORT."
            )

        return config

    def _connect(self):
        try:
            return mysql.connector.connect(**self.db_config)
        except Error as exc:  # pragma: no cover - requires live DB
            raise RuntimeError(f"Unable to connect to MySQL: {exc}") from exc

    def cursor(self):
        if not self.connection or not self.connection.is_connected():
            self.connection = self._connect()
        return self.connection.cursor(dictionary=True)

    def close_connection(self) -> None:
        if self.connection and self.connection.is_connected():
            self.connection.close()
