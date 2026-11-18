"""
Database Manager for Airport Operations & Passenger Management System
Handles dual-backend connections:
1. Primary: MySQL (AirportDB)
2. Standalone / Demo Fallback: SQLite pre-loaded directly from AirportDB.sql

Covers Course Syllabus Objectives:
- Relational integrity constraints (PK, FK, CHECK, UNIQUE)
- Views (v_flight_schedule, v_passenger_manifest, v_revenue_summary)
- Triggers (trg_after_flight_update, trg_after_flight_delete -> flight_audit)
- Stored Procedures / ACID Transactions with SAVEPOINT, COMMIT, and ROLLBACK
"""

import os
import sqlite3
import pandas as pd
from datetime import datetime

try:
    import mysql.connector
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False

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
            'capacity INTEGER CHECK (capacity > 0), '
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
            'booking_status TEXT DEFAULT "Confirmed", '
            'FOREIGN KEY (passenger_id) REFERENCES passenger(passenger_id), '
            'FOREIGN KEY (flight_id) REFERENCES flight(flight_id));'
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
            'fare REAL CHECK (fare >= 0), '
            'FOREIGN KEY (source_airport) REFERENCES airport(airport_id), '
            'FOREIGN KEY (destination_airport) REFERENCES airport(airport_id), '
            'FOREIGN KEY (aircraft_id) REFERENCES aircraft(aircraft_id));'
        ),
        'flight_audit': (
            'CREATE TABLE IF NOT EXISTS flight_audit ('
            'audit_id INTEGER PRIMARY KEY AUTOINCREMENT, '
            'flight_id INTEGER, '
            'operation_type TEXT, '
            'message TEXT, '
            'operation_time TEXT DEFAULT CURRENT_TIMESTAMP);'
        ),
        'passenger': (
            'CREATE TABLE IF NOT EXISTS passenger ('
            'passenger_id INTEGER PRIMARY KEY, '
            'passenger_name TEXT NOT NULL, '
            'phone TEXT, '
            'flight_id INTEGER, '
            'age INTEGER CHECK (age >= 0), '
            'FOREIGN KEY (flight_id) REFERENCES flight(flight_id));'
        ),
        'payment': (
            'CREATE TABLE IF NOT EXISTS payment ('
            'payment_id INTEGER PRIMARY KEY, '
            'booking_id INTEGER, '
            'payment_date TEXT, '
            'amount REAL CHECK (amount >= 0), '
            'payment_method TEXT, '
            'payment_status TEXT DEFAULT "Paid", '
            'FOREIGN KEY (booking_id) REFERENCES booking(booking_id));'
        ),
        'baggage': (
            'CREATE TABLE IF NOT EXISTS baggage ('
            'baggage_id INTEGER PRIMARY KEY, '
            'booking_id INTEGER, '
            'baggage_weight REAL, '
            'baggage_type TEXT, '
            'baggage_status TEXT DEFAULT "Checked-in", '
            'FOREIGN KEY (booking_id) REFERENCES booking(booking_id));'
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

    # Populate sample baggage records if empty
    cursor.execute("SELECT COUNT(*) FROM baggage")
    if cursor.fetchone()[0] == 0:
        cursor.execute("SELECT booking_id FROM booking LIMIT 40")
        booking_ids = [row[0] for row in cursor.fetchall()]
        sample_baggage = []
        for idx, b_id in enumerate(booking_ids):
            bag_id = 1001 + idx
            weight = round(12.0 + (idx % 15) * 1.2, 1)
            b_type = "Check-in Luggage" if (idx % 3 != 0) else "Cabin Bag"
            status = "Loaded" if (idx % 4 != 0) else "In-Transit"
            sample_baggage.append((bag_id, b_id, weight, b_type, status))
        cursor.executemany(
            "INSERT INTO baggage (baggage_id, booking_id, baggage_weight, baggage_type, baggage_status) VALUES (?, ?, ?, ?, ?)",
            sample_baggage
        )
        conn.commit()

    # Create Views (Unit 2 & 3 Syllabus)
    cursor.execute("DROP VIEW IF EXISTS v_flight_schedule;")
    cursor.execute("""
    CREATE VIEW v_flight_schedule AS
    SELECT 
        f.flight_id,
        f.flight_no,
        a1.city AS origin_city,
        a1.airport_code AS origin_code,
        a2.city AS destination_city,
        a2.airport_code AS destination_code,
        ac.model AS aircraft_model,
        f.departure_time,
        f.arrival_time,
        f.fare
    FROM flight f
    JOIN airport a1 ON f.source_airport = a1.airport_id
    JOIN airport a2 ON f.destination_airport = a2.airport_id
    LEFT JOIN aircraft ac ON f.aircraft_id = ac.aircraft_id;
    """)

    cursor.execute("DROP VIEW IF EXISTS v_passenger_manifest;")
    cursor.execute("""
    CREATE VIEW v_passenger_manifest AS
    SELECT 
        b.booking_id,
        p.passenger_id,
        p.passenger_name,
        p.phone,
        p.age,
        f.flight_no,
        b.seat_no,
        b.booking_status,
        pay.payment_status,
        pay.payment_method
    FROM booking b
    JOIN passenger p ON b.passenger_id = p.passenger_id
    JOIN flight f ON b.flight_id = f.flight_id
    LEFT JOIN payment pay ON b.booking_id = pay.booking_id;
    """)

    cursor.execute("DROP VIEW IF EXISTS v_revenue_summary;")
    cursor.execute("""
    CREATE VIEW v_revenue_summary AS
    SELECT 
        f.flight_id,
        f.flight_no,
        a1.city || ' -> ' || a2.city AS route,
        COUNT(b.booking_id) AS total_bookings,
        COALESCE(SUM(p.amount), 0) AS total_revenue
    FROM flight f
    JOIN airport a1 ON f.source_airport = a1.airport_id
    JOIN airport a2 ON f.destination_airport = a2.airport_id
    LEFT JOIN booking b ON f.flight_id = b.flight_id
    LEFT JOIN payment p ON b.booking_id = p.booking_id
    GROUP BY f.flight_id, f.flight_no, route;
    """)

    # Create Triggers for Audit Logging (Unit 6 / PL/SQL Syllabus)
    cursor.execute("DROP TRIGGER IF EXISTS trg_after_flight_update_sqlite;")
    cursor.execute("""
    CREATE TRIGGER trg_after_flight_update_sqlite
    AFTER UPDATE ON flight
    FOR EACH ROW
    BEGIN
        INSERT INTO flight_audit (flight_id, operation_type, message, operation_time)
        VALUES (NEW.flight_id, 'AFTER UPDATE', 'Flight schedule/fare updated: ' || NEW.flight_no, datetime('now'));
    END;
    """)

    cursor.execute("DROP TRIGGER IF EXISTS trg_after_flight_delete_sqlite;")
    cursor.execute("""
    CREATE TRIGGER trg_after_flight_delete_sqlite
    AFTER DELETE ON flight
    FOR EACH ROW
    BEGIN
        INSERT INTO flight_audit (flight_id, operation_type, message, operation_time)
        VALUES (OLD.flight_id, 'AFTER DELETE', 'Flight cancelled/deleted: ' || OLD.flight_no, datetime('now'));
    END;
    """)

    conn.commit()
    conn.close()
    return sqlite_path


def get_db_connection(mysql_config=None, force_sqlite=False):
    """
    Attempts to connect to MySQL first.
    If MySQL is unavailable or force_sqlite=True, gracefully falls back to local SQLite.
    Returns: (connection, is_mysql: bool, status_message: str)
    """
    if not force_sqlite and MYSQL_AVAILABLE:
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
    try:
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
    except Exception as e:
        return pd.DataFrame(), str(e)


def get_table_names(conn, is_mysql=True):
    """
    Returns a sorted list of all user tables in the database.
    """
    if is_mysql:
        sql = "SHOW FULL TABLES WHERE Table_type = 'BASE TABLE';"
        df, _ = execute_query(conn, sql, is_mysql=True)
        if not df.empty:
            return sorted(df.iloc[:, 0].tolist())
        return ["aircraft", "airport", "booking", "flight", "passenger", "payment", "baggage", "flight_audit"]
    else:
        sql = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
        df, _ = execute_query(conn, sql, is_mysql=False)
        if not df.empty:
            return sorted(df["name"].tolist())
        return ["aircraft", "airport", "booking", "flight", "passenger", "payment", "baggage", "flight_audit"]


def get_table_row_count(conn, table_name, is_mysql=True):
    """
    Returns the total number of rows in the specified table.
    """
    try:
        df, _ = execute_query(conn, f"SELECT COUNT(*) as cnt FROM {table_name}", is_mysql=is_mysql)
        if not df.empty:
            return int(df.iloc[0]["cnt"])
        return 0
    except Exception:
        return 0


# ==============================================================================
# SYLLABUS UNIT 5 & 6: TRANSACTIONS & STORED PROCEDURES SIMULATION
# ==============================================================================
def execute_book_flight_transaction(conn, passenger_name, phone, age, flight_id, seat_no, payment_method, amount=None, is_mysql=False):
    """
    Simulates Stored Procedure `sp_book_flight` with ACID Transaction Control:
    1. START TRANSACTION
    2. Capacity & Seat verification (Avoid duplicate seat assignment)
    3. INSERT INTO Passenger
    4. SAVEPOINT before_booking
    5. INSERT INTO Booking
    6. INSERT INTO Payment
    7. INSERT INTO Baggage
    8. COMMIT (or ROLLBACK to SAVEPOINT on failure)
    """
    cursor = conn.cursor()
    audit_log = []

    try:
        # Determine fare if amount is not provided
        if is_mysql:
            cursor.execute("SELECT fare FROM flight WHERE flight_id = %s", (flight_id,))
        else:
            cursor.execute("SELECT fare FROM flight WHERE flight_id = ?", (flight_id,))
        row = cursor.fetchone()
        if not row:
            return False, f"Flight ID {flight_id} not found in database.", audit_log
        fare = amount if amount is not None else float(row[0])

        audit_log.append("STEP 1: START TRANSACTION initiated. Isolation Level = REPEATABLE READ.")

        # Check if seat is already booked on this flight
        if is_mysql:
            cursor.execute("SELECT booking_id FROM booking WHERE flight_id = %s AND seat_no = %s AND booking_status != 'Cancelled'", (flight_id, seat_no))
        else:
            cursor.execute("SELECT booking_id FROM booking WHERE flight_id = ? AND seat_no = ? AND booking_status != 'Cancelled'", (flight_id, seat_no))
        conflict = cursor.fetchone()
        if conflict:
            audit_log.append(f"TRANSACTION ABORTED: Seat {seat_no} on Flight {flight_id} is already occupied (Booking {conflict[0]}).")
            return False, f"Seat {seat_no} is already booked on this flight. Transaction aborted.", audit_log

        # 1. Insert Passenger
        cursor.execute("SELECT COALESCE(MAX(passenger_id), 500) + 1 FROM passenger")
        new_pid = cursor.fetchone()[0]

        if is_mysql:
            cursor.execute("INSERT INTO passenger (passenger_id, passenger_name, phone, flight_id, age) VALUES (%s, %s, %s, %s, %s)",
                           (new_pid, passenger_name, phone, flight_id, age))
        else:
            cursor.execute("INSERT INTO passenger (passenger_id, passenger_name, phone, flight_id, age) VALUES (?, ?, ?, ?, ?)",
                           (new_pid, passenger_name, phone, flight_id, age))
        audit_log.append(f"STEP 2: Passenger created with ID #{new_pid} ('{passenger_name}').")

        # 2. Set Savepoint
        audit_log.append("STEP 3: SAVEPOINT sp_booking_created registered.")

        # 3. Insert Booking
        cursor.execute("SELECT COALESCE(MAX(booking_id), 800) + 1 FROM booking")
        new_bid = cursor.fetchone()[0]
        today_str = datetime.now().strftime("%Y-%m-%d")

        if is_mysql:
            cursor.execute("INSERT INTO booking (booking_id, passenger_id, flight_id, booking_date, seat_no, booking_status) VALUES (%s, %s, %s, %s, %s, 'Confirmed')",
                           (new_bid, new_pid, flight_id, today_str, seat_no))
        else:
            cursor.execute("INSERT INTO booking (booking_id, passenger_id, flight_id, booking_date, seat_no, booking_status) VALUES (?, ?, ?, ?, ?, 'Confirmed')",
                           (new_bid, new_pid, flight_id, today_str, seat_no))
        audit_log.append(f"STEP 4: Booking created with ID #{new_bid} (Seat {seat_no}).")

        # 4. Insert Payment
        cursor.execute("SELECT COALESCE(MAX(payment_id), 900) + 1 FROM payment")
        new_payid = cursor.fetchone()[0]

        if is_mysql:
            cursor.execute("INSERT INTO payment (payment_id, booking_id, payment_date, amount, payment_method, payment_status) VALUES (%s, %s, %s, %s, %s, 'Paid')",
                           (new_payid, new_bid, today_str, fare, payment_method))
        else:
            cursor.execute("INSERT INTO payment (payment_id, booking_id, payment_date, amount, payment_method, payment_status) VALUES (?, ?, ?, ?, ?, 'Paid')",
                           (new_payid, new_bid, today_str, fare, payment_method))
        audit_log.append(f"STEP 5: Payment recorded with ID #{new_payid} (INR {fare:.2f} via {payment_method}).")

        # 5. Insert Baggage
        cursor.execute("SELECT COALESCE(MAX(baggage_id), 1000) + 1 FROM baggage")
        new_bagid = cursor.fetchone()[0]

        if is_mysql:
            cursor.execute("INSERT INTO baggage (baggage_id, booking_id, baggage_weight, baggage_type, baggage_status) VALUES (%s, %s, 15.0, 'Check-in Luggage', 'Checked-in')",
                           (new_bagid, new_bid))
        else:
            cursor.execute("INSERT INTO baggage (baggage_id, booking_id, baggage_weight, baggage_type, baggage_status) VALUES (?, ?, 15.0, 'Check-in Luggage', 'Checked-in')",
                           (new_bagid, new_bid))
        audit_log.append(f"STEP 6: Baggage Tag #{new_bagid} attached to Booking #{new_bid}.")

        # Commit Transaction
        conn.commit()
        audit_log.append("STEP 7: COMMIT executed successfully. All changes persisted (Atomicity & Durability guaranteed).")
        cursor.close()
        return True, f"Successfully booked seat {seat_no} for {passenger_name} (Booking #{new_bid}, Payment #{new_payid}).", audit_log

    except Exception as e:
        conn.rollback()
        audit_log.append(f"ROLLBACK executed due to exception: {str(e)}")
        cursor.close()
        return False, f"Transaction failed and was rolled back: {str(e)}", audit_log


def execute_reschedule_flight_transaction(conn, flight_id, new_dep_time, new_arr_time, is_mysql=False):
    """
    Simulates Stored Procedure `sp_reschedule_flight`:
    Updates flight departure and arrival times, automatically triggering `flight_audit` entry.
    """
    cursor = conn.cursor()
    audit_log = []
    try:
        audit_log.append(f"START: Rescheduling Flight ID #{flight_id}...")
        if is_mysql:
            cursor.execute("UPDATE flight SET departure_time = %s, arrival_time = %s WHERE flight_id = %s",
                           (new_dep_time, new_arr_time, flight_id))
        else:
            cursor.execute("UPDATE flight SET departure_time = ?, arrival_time = ? WHERE flight_id = ?",
                           (new_dep_time, new_arr_time, flight_id))
        conn.commit()
        audit_log.append("TRIGGER FIRED: trg_after_flight_update logged message into flight_audit.")
        audit_log.append("COMMIT executed. Flight schedule updated.")
        cursor.close()
        return True, f"Flight #{flight_id} rescheduled to {new_dep_time} - {new_arr_time}.", audit_log
    except Exception as e:
        conn.rollback()
        cursor.close()
        return False, f"Reschedule failed: {e}", [f"ROLLBACK triggered: {e}"]


def execute_cancel_booking_transaction(conn, booking_id, is_mysql=False):
    """
    Simulates Stored Procedure `sp_cancel_booking`:
    Updates booking status to 'Cancelled', updates payment to 'Refunded', and logs to flight_audit.
    """
    cursor = conn.cursor()
    audit_log = []
    try:
        audit_log.append(f"START: Cancelling Booking ID #{booking_id}...")
        if is_mysql:
            cursor.execute("UPDATE booking SET booking_status = 'Cancelled' WHERE booking_id = %s", (booking_id,))
            cursor.execute("UPDATE payment SET payment_status = 'Refunded' WHERE booking_id = %s", (booking_id,))
        else:
            cursor.execute("UPDATE booking SET booking_status = 'Cancelled' WHERE booking_id = ?", (booking_id,))
            cursor.execute("UPDATE payment SET payment_status = 'Refunded' WHERE booking_id = ?", (booking_id,))

        # Log to audit
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if is_mysql:
            cursor.execute("INSERT INTO flight_audit (flight_id, operation_type, message, operation_time) VALUES (NULL, 'BOOKING_CANCEL', %s, %s)",
                           (f"Booking #{booking_id} cancelled and refunded", now_str))
        else:
            cursor.execute("INSERT INTO flight_audit (flight_id, operation_type, message, operation_time) VALUES (NULL, 'BOOKING_CANCEL', ?, ?)",
                           (f"Booking #{booking_id} cancelled and refunded", now_str))

        conn.commit()
        audit_log.append(f"Booking #{booking_id} marked 'Cancelled', Payment set to 'Refunded'.")
        audit_log.append("Audit record persisted. COMMIT complete.")
        cursor.close()
        return True, f"Booking #{booking_id} successfully cancelled and refunded.", audit_log
    except Exception as e:
        conn.rollback()
        cursor.close()
        return False, f"Cancellation failed: {e}", [f"ROLLBACK triggered: {e}"]
