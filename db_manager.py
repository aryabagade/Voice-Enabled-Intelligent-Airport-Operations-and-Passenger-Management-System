"""
Database Manager for Airport Operations & Passenger Management System
Handles dual-backend connections:
1. Primary: MySQL (AirportDB)
2. Standalone / Demo Fallback: SQLite pre-loaded directly from AirportDB.sql
"""

import os
import sqlite3
import pandas as pd
import mysql.connector

# Default MySQL configuration
DEFAULT_MYSQL_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "1234",
    "database": "AirportDB"
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQL_DUMP_PATH = os.path.join(BASE_DIR, "AirportDB.sql")
SQLITE_DB_PATH = os.path.join(BASE_DIR, "AirportDB.sqlite")


def init_sqlite_from_dump(sql_path=SQL_DUMP_PATH, sqlite_path=SQLITE_DB_PATH):
    """
    Initializes a local SQLite database from AirportDB.sql if it doesn't exist
    or if it needs regeneration. Ensures zero-setup out-of-the-box experience.
    """
    table_defs = {
        'aircraft': (
            'CREATE TABLE IF NOT EXISTS aircraft ('
            'aircraft_id INTEGER PRIMARY KEY, '
            'model TEXT NOT NULL, '
            'capacity INTEGER, '
            'manufacturer TEXT, '
            'status TEXT DEFAULT "Available");'
        ),
        'airport': (
            'CREATE TABLE IF NOT EXISTS airport ('
            'airport_id INTEGER PRIMARY KEY, '
            'airport_name TEXT NOT NULL, '
            'city TEXT NOT NULL, '
            'country TEXT NOT NULL, '
            'airport_code TEXT UNIQUE);'
        ),
        'booking': (
            'CREATE TABLE IF NOT EXISTS booking ('
            'booking_id INTEGER PRIMARY KEY, '
            'passenger_id INTEGER, '
            'flight_id INTEGER, '
            'booking_date TEXT, '
            'seat_no TEXT, '
            'booking_status TEXT);'
        ),
        'flight': (
            'CREATE TABLE IF NOT EXISTS flight ('
            'flight_id INTEGER PRIMARY KEY, '
            'flight_no TEXT UNIQUE NOT NULL, '
            'source_airport INTEGER, '
            'destination_airport INTEGER, '
            'aircraft_id INTEGER, '
            'departure_time TEXT, '
            'arrival_time TEXT, '
            'fare REAL);'
        ),
        'flight_audit': (
            'CREATE TABLE IF NOT EXISTS flight_audit ('
            'audit_id INTEGER PRIMARY KEY, '
            'flight_id INTEGER, '
            'action_type TEXT, '
            'description TEXT, '
            'change_time TEXT);'
        ),
        'passenger': (
            'CREATE TABLE IF NOT EXISTS passenger ('
            'passenger_id INTEGER PRIMARY KEY, '
            'passenger_name TEXT NOT NULL, '
            'phone TEXT, '
            'flight_id INTEGER, '
            'age INTEGER);'
        ),
        'payment': (
            'CREATE TABLE IF NOT EXISTS payment ('
            'payment_id INTEGER PRIMARY KEY, '
            'booking_id INTEGER, '
            'payment_date TEXT, '
            'amount REAL, '
            'payment_method TEXT, '
            'payment_status TEXT);'
        )
    }

    conn = sqlite3.connect(sqlite_path)
    cursor = conn.cursor()

    # Create tables
    for ddl in table_defs.values():
        cursor.execute(ddl)

    # Check if records already exist
    cursor.execute("SELECT COUNT(*) FROM flight")
    flight_count = cursor.fetchone()[0]

    if flight_count == 0 and os.path.exists(sql_path):
        with open(sql_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                l = line.strip()
                if l.startswith("INSERT INTO `") and "VALUES" in l:
                    stmt = l.replace("`", '"')
                    try:
                        cursor.execute(stmt)
                    except Exception:
                        pass
        conn.commit()

    conn.close()
    return sqlite_path


def get_db_connection(mysql_config=None, force_sqlite=False):
    """
    Attempts to connect to MySQL first.
    If MySQL is unavailable or force_sqlite=True, gracefully falls back to local SQLite.
    Returns: (connection, is_mysql: bool, status_message: str)
    """
    if not force_sqlite:
        cfg = mysql_config or DEFAULT_MYSQL_CONFIG
        try:
            conn = mysql.connector.connect(
                host=cfg.get("host", "localhost"),
                port=int(cfg.get("port", 3306)),
                user=cfg.get("user", "root"),
                password=cfg.get("password", "1234"),
                database=cfg.get("database", "AirportDB"),
                connection_timeout=2
            )
            return conn, True, f"Connected to MySQL Database: {cfg.get('database', 'AirportDB')} on {cfg.get('host', 'localhost')}:{cfg.get('port', 3306)}"
        except Exception as e:
            msg = f"MySQL unavailable ({e}). Fallback to local AirportDB (SQLite)."
    else:
        msg = "Using Standalone Local AirportDB (SQLite mode)."

    # Initialize/verify SQLite database
    sqlite_file = init_sqlite_from_dump()
    conn = sqlite3.connect(sqlite_file, check_same_thread=False)
    return conn, False, msg


def execute_query(conn, query, is_mysql=True):
    """
    Executes a SQL query safely and returns a pandas DataFrame.
    """
    if is_mysql:
        cursor = conn.cursor()
        cursor.execute(query)
        if cursor.description:
            columns = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()
            cursor.close()
            return pd.DataFrame(data, columns=columns), None
        else:
            conn.commit()
            cursor.close()
            return pd.DataFrame(), None
    else:
        cursor = conn.cursor()
        cursor.execute(query)
        if cursor.description:
            columns = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()
            cursor.close()
            return pd.DataFrame(data, columns=columns), None
        else:
            conn.commit()
            cursor.close()
            return pd.DataFrame(), None


def get_table_names(conn, is_mysql=True):
    """
    Returns list of table names in the database.
    """
    if is_mysql:
        df, _ = execute_query(conn, "SHOW TABLES", is_mysql=True)
        return df.iloc[:, 0].tolist() if not df.empty else []
    else:
        df, _ = execute_query(conn, "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'", is_mysql=False)
        return df.iloc[:, 0].tolist() if not df.empty else []


def get_table_row_count(conn, table_name, is_mysql=True):
    """
    Returns row count for a given table.
    """
    try:
        df, _ = execute_query(conn, f"SELECT COUNT(*) AS total FROM {table_name}", is_mysql=is_mysql)
        return int(df.iloc[0, 0]) if not df.empty else 0
    except Exception:
        return 0
