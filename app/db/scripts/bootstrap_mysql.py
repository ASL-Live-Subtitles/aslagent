from __future__ import annotations

import argparse
import sys
from typing import Iterable

import mysql.connector
from mysql.connector import Error

from schema_sql import (
    DEFAULT_DB_NAME,
    DEFAULT_DB_PASSWORD,
    DEFAULT_DB_USER,
    EXPRESSION_RULES_SEED_SQL,
    EXPRESSION_RULES_TABLE_SQL,
    TRANSLATION_SESSIONS_SEED_SQL,
    TRANSLATION_SESSIONS_TABLE_SQL,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bootstrap the ASL Agent MySQL schema.")
    parser.add_argument("--host", default="127.0.0.1", help="MySQL host for the root connection")
    parser.add_argument("--port", default=3306, type=int, help="MySQL port for the root connection")
    parser.add_argument("--root-user", default="root", help="MySQL administrative user")
    parser.add_argument("--root-password", default=None, help="Password for the root user")
    parser.add_argument("--db-name", default=DEFAULT_DB_NAME, help="Database/schema name to create")
    parser.add_argument("--db-user", default=DEFAULT_DB_USER, help="Application DB user to create/grant")
    parser.add_argument("--db-password", default=DEFAULT_DB_PASSWORD, help="Password for the application user")
    parser.add_argument("--skip-seed", action="store_true", help="Skip inserting sample rows")
    return parser.parse_args()


def connect(host: str, port: int, user: str, password: str | None, database: str | None = None):
    return mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
    )


def run_statements(connection, statements: Iterable[str]) -> None:
    cursor = connection.cursor()
    try:
        for statement in statements:
            stmt = statement.strip()
            if not stmt:
                continue
            cursor.execute(stmt)
        connection.commit()
    finally:
        cursor.close()


def create_database_and_user(args: argparse.Namespace) -> None:
    statements = [
        f"CREATE DATABASE IF NOT EXISTS `{args.db_name}`;",
        f"CREATE USER IF NOT EXISTS '{args.db_user}'@'%' IDENTIFIED BY '{args.db_password}';",
        f"GRANT ALL PRIVILEGES ON `{args.db_name}`.* TO '{args.db_user}'@'%';",
        "FLUSH PRIVILEGES;",
    ]

    root_conn = connect(args.host, args.port, args.root_user, args.root_password)
    try:
        run_statements(root_conn, statements)
    finally:
        root_conn.close()


def create_tables(args: argparse.Namespace) -> None:
    conn = connect(args.host, args.port, args.root_user, args.root_password, args.db_name)
    try:
        run_statements(conn, [EXPRESSION_RULES_TABLE_SQL, TRANSLATION_SESSIONS_TABLE_SQL])
    finally:
        conn.close()


def seed_tables(args: argparse.Namespace) -> None:
    conn = connect(args.host, args.port, args.root_user, args.root_password, args.db_name)
    try:
        run_statements(conn, [EXPRESSION_RULES_SEED_SQL, TRANSLATION_SESSIONS_SEED_SQL])
    finally:
        conn.close()


def main() -> int:
    args = parse_args()

    try:
        create_database_and_user(args)
        create_tables(args)
        if not args.skip_seed:
            seed_tables(args)
    except Error as exc:
        print(f"MySQL error: {exc}")
        return 1
    except Exception as exc:  # pragma: no cover - CLI guard
        print(f"Unexpected error: {exc}")
        return 1

    print(
        "Bootstrap complete! Database '{db}' is ready for the ASL Agent service.".format(
            db=args.db_name
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
