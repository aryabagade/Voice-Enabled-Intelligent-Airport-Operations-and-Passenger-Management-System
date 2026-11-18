"""
Syllabus Engine for Airport Management System
Implements comprehensive theoretical and practical concepts across all 6 Units of the
DBMS Course Syllabus (VIT Pune / B.Tech CS/IT/AI-DS CS2227 / ML2302):

- Unit 1: Data Modeling, 3-Tier Architecture, Relational Integrity & Codd's Rules
- Unit 2 & 3: Relational Algebra, Advanced SQL, Joins, Subqueries, Views & Execution Plans
- Unit 4: Normalization (1NF to BCNF), Parquet Columnar Storage & ARIES Crash Recovery
- Unit 5: Transaction Management (ACID), Concurrency Control (Conflict Serializability, 2PL) & Distributed Sharding
- Unit 6: NoSQL (Document, Key-Value, Columnar, Graph), HDFS/MapReduce & Data Warehousing (Star Schema OLAP)
"""

import json
import math
from typing import Dict, List, Any, Tuple


# ==============================================================================
# UNIT 1: DATA MODELING, RELATIONAL MODEL & CODD'S RULES
# ==============================================================================
class Unit1DataModeling:
    @staticmethod
    def get_three_tier_architecture() -> Dict[str, Any]:
        """Returns the 3-Tier ANSI/SPARC Database Architecture mapping for AirportDB."""
        return {
            "External_View_Level": [
                {"name": "Passenger Portal View", "access": "Search flights, view personal bookings, seat selection"},
                {"name": "Flight Dispatcher View", "access": "Manage schedules, aircraft assignments, gate changes"},
                {"name": "Airport Operations View (FIDS)", "access": "Public departure/arrival board, delays, baggage carousels"},
                {"name": "Finance & Audit View", "access": "Payment reconciliation, route revenue, audit log tracking"}
            ],
            "Conceptual_Logical_Level": {
                "entities": ["Airport", "Aircraft", "Flight", "Passenger", "Booking", "Payment", "Baggage", "Flight_Audit"],
                "relationships": [
                    "Airport (1) ---departs---> (N) Flight",
                    "Airport (1) ---arrives---> (N) Flight",
                    "Aircraft (1) ---assigned_to---> (N) Flight",
                    "Passenger (1) ---makes---> (N) Booking",
                    "Flight (1) ---contains---> (N) Booking",
                    "Booking (1) ---generates---> (1..N) Payment",
                    "Booking (1) ---checks_in---> (0..N) Baggage"
                ],
                "normal_form": "Boyce-Codd Normal Form (BCNF) / 3NF"
            },
            "Internal_Physical_Level": {
                "storage_engine": "InnoDB (B+ Tree clustered index on Primary Keys)",
                "data_types": ["INT", "VARCHAR", "DECIMAL(10,2)", "DATETIME", "CHAR(3)"],
                "file_structures": ["AirportDB.ibd (tablespace)", "ib_logfile (WAL redo log)", "undo tablespace"]
            }
        }

    @staticmethod
    def get_integrity_constraints() -> List[Dict[str, str]]:
        """Returns the integrity constraints enforced in AirportDB."""
        return [
            {
                "type": "Entity Integrity",
                "table": "All Tables",
                "definition": "Primary Key cannot be NULL and must be unique.",
                "example": "airport_id (PK), flight_id (PK), passenger_id (PK), booking_id (PK)"
            },
            {
                "type": "Referential Integrity",
                "table": "Flight, Booking, Payment, Baggage",
                "definition": "Foreign key values must match an existing primary key in parent table or be NULL.",
                "example": "flight.source_airport -> airport.airport_id; booking.passenger_id -> passenger.passenger_id"
            },
            {
                "type": "Domain Integrity",
                "table": "All Tables",
                "definition": "Attribute values must adhere to the defined data type, length, and range.",
                "example": "fare is DECIMAL(10,2) > 0, airport_code is CHAR(3) uppercase"
            },
            {
                "type": "Check Constraint",
                "table": "Aircraft, Flight, Passenger",
                "definition": "User-defined boolean condition evaluated on INSERT and UPDATE.",
                "example": "CHECK (capacity > 0), CHECK (fare >= 0), CHECK (age >= 0)"
            },
            {
                "type": "Key Uniqueness",
                "table": "Airport, Flight",
                "definition": "Candidate keys that uniquely identify tuples beyond the surrogate PK.",
                "example": "airport_code UNIQUE (e.g. 'BOM', 'DEL'), flight_no UNIQUE (e.g. 'AI101')"
            }
        ]

    @staticmethod
    def get_codds_rules_evaluation() -> List[Dict[str, Any]]:
        """Evaluates Codd's 12 Rules against AirportDB."""
        return [
            {"rule_no": "Rule 0", "title": "Foundation Rule", "status": "Compliant", "details": "The system manages the entire database purely through relational capabilities."},
            {"rule_no": "Rule 1", "title": "Information Rule", "status": "Compliant", "details": "All data (airports, flights, bookings) is represented exclusively at the logical level as rows in tables."},
            {"rule_no": "Rule 2", "title": "Guaranteed Access Rule", "status": "Compliant", "details": "Every datum is logically addressable using table name, primary key value, and column name."},
            {"rule_no": "Rule 3", "title": "Systematic Treatment of NULLs", "status": "Compliant", "details": "NULL is treated systematically as unknown/missing data (e.g., optional middle names, baggage weight)."},
            {"rule_no": "Rule 4", "title": "Active Online Dynamic Catalog", "status": "Compliant", "details": "Database metadata is queryable in INFORMATION_SCHEMA / sqlite_master using standard SQL."},
            {"rule_no": "Rule 5", "title": "Comprehensive Data Sublanguage", "status": "Compliant", "details": "SQL supports DDL, DML, DQL, transaction control (COMMIT/ROLLBACK), and integrity constraints."},
            {"rule_no": "Rule 6", "title": "View Updating Rule", "status": "Compliant", "details": "Updatable views can propagate DML statements to underlying base tables."},
            {"rule_no": "Rule 7", "title": "High-Level Insert, Update, Delete", "status": "Compliant", "details": "Set-at-a-time operations manipulate entire sets of tuples in a single statement."},
            {"rule_no": "Rule 8", "title": "Physical Data Independence", "status": "Compliant", "details": "Changes to physical storage or disk indexing do not alter application SQL queries."},
            {"rule_no": "Rule 9", "title": "Logical Data Independence", "status": "Compliant", "details": "Views decouple front-end user interfaces from internal schema modifications."},
            {"rule_no": "Rule 10", "title": "Integrity Independence", "status": "Compliant", "details": "Integrity constraints (PK, FK, CHECK) are enforced inside the DBMS catalog, not hardcoded in apps."},
            {"rule_no": "Rule 11", "title": "Distribution Independence", "status": "Compliant", "details": "Applications operate identically whether database tables reside on one server or distributed nodes."},
            {"rule_no": "Rule 12", "title": "Non-Subversion Rule", "status": "Compliant", "details": "Low-level record access cannot bypass relational constraints or security policies."}
        ]


# ==============================================================================
# UNIT 2 & 3: RELATIONAL ALGEBRA & ADVANCED SQL
# ==============================================================================
class Unit2RelationalAlgebra:
    @staticmethod
    def get_relational_algebra_mappings() -> List[Dict[str, str]]:
        """Maps standard relational algebra operations to SQL queries in AirportDB."""
        return [
            {
                "operation": "Selection (σ)",
                "formula": "σ_{fare < 6000 ∧ city = 'Mumbai'}(Flight ⨝_{source_airport = airport_id} Airport)",
                "sql": "SELECT f.* FROM flight f JOIN airport a ON f.source_airport = a.airport_id WHERE f.fare < 6000 AND a.city = 'Mumbai';",
                "explanation": "Filters horizontal subset of tuples satisfying boolean predicate."
            },
            {
                "operation": "Projection (π)",
                "formula": "π_{flight_no, fare}(Flight)",
                "sql": "SELECT flight_no, fare FROM flight;",
                "explanation": "Extracts vertical subset of specified columns and removes duplicate rows."
            },
            {
                "operation": "Natural Inner Join (⨝)",
                "formula": "Flight ⨝_{source_airport = a1.airport_id} Airport(a1) ⨝_{aircraft_id = ac.aircraft_id} Aircraft(ac)",
                "sql": "SELECT f.flight_no, a1.city AS origin, ac.model FROM flight f JOIN airport a1 ON f.source_airport = a1.airport_id JOIN aircraft ac ON f.aircraft_id = ac.aircraft_id;",
                "explanation": "Combines tuples from multiple relations matching join condition."
            },
            {
                "operation": "Left Outer Join (⟕)",
                "formula": "Aircraft ⟕_{Aircraft.aircraft_id = Flight.aircraft_id} Flight",
                "sql": "SELECT ac.aircraft_id, ac.model, f.flight_no FROM aircraft ac LEFT JOIN flight f ON ac.aircraft_id = f.aircraft_id WHERE f.flight_no IS NULL;",
                "explanation": "Preserves all aircraft even if they currently have no assigned scheduled flights."
            },
            {
                "operation": "Self Join (ρ)",
                "formula": "ρ_{F1}(Flight) ⨝_{F1.destination_airport = F2.source_airport} ρ_{F2}(Flight)",
                "sql": "SELECT F1.flight_no AS Leg1, F2.flight_no AS Leg2, F1.destination_airport AS Transfer_Hub FROM flight F1 JOIN flight F2 ON F1.destination_airport = F2.source_airport WHERE F1.source_airport <> F2.destination_airport;",
                "explanation": "Finds connecting 2-leg flights with layover hubs."
            },
            {
                "operation": "Set Union (∪)",
                "formula": "π_{city}(σ_{country='India'}(Airport)) ∪ π_{city}(σ_{country='International'}(Airport))",
                "sql": "SELECT city FROM airport WHERE country = 'India' UNION SELECT city FROM airport WHERE country <> 'India';",
                "explanation": "Combines distinct city tuples from two compatible relations."
            },
            {
                "operation": "Set Difference (−)",
                "formula": "π_{aircraft_id}(Aircraft) − π_{aircraft_id}(Flight)",
                "sql": "SELECT aircraft_id FROM aircraft EXCEPT SELECT aircraft_id FROM flight;",
                "explanation": "Finds aircraft IDs in the fleet that have never been scheduled on any flight."
            }
        ]

    @staticmethod
    def get_complex_sql_suite() -> List[Dict[str, str]]:
        """Returns advanced SQL demonstration queries for DBMS viva/evaluation."""
        return [
            {
                "category": "Correlated Subquery",
                "title": "Passengers with Highest Age per Flight",
                "sql": (
                    "SELECT p1.passenger_name, p1.age, p1.flight_id\n"
                    "FROM passenger p1\n"
                    "WHERE p1.age = (\n"
                    "    SELECT MAX(p2.age)\n"
                    "    FROM passenger p2\n"
                    "    WHERE p2.flight_id = p1.flight_id\n"
                    ");"
                ),
                "notes": "Inner query re-executes for each outer row, filtering the oldest passenger on each route."
            },
            {
                "category": "Multi-Row Subquery (IN / ALL)",
                "title": "Flights with Above-Average Revenue",
                "sql": (
                    "SELECT f.flight_no, SUM(p.amount) AS total_revenue\n"
                    "FROM flight f\n"
                    "JOIN booking b ON f.flight_id = b.flight_id\n"
                    "JOIN payment p ON b.booking_id = p.booking_id\n"
                    "GROUP BY f.flight_id, f.flight_no\n"
                    "HAVING SUM(p.amount) > (\n"
                    "    SELECT AVG(route_rev)\n"
                    "    FROM (\n"
                    "        SELECT SUM(p2.amount) AS route_rev\n"
                    "        FROM booking b2\n"
                    "        JOIN payment p2 ON b2.booking_id = p2.booking_id\n"
                    "        GROUP BY b2.flight_id\n"
                    "    ) AS sub\n"
                    ");"
                ),
                "notes": "Demonstrates derived tables, GROUP BY, HAVING, and aggregate subqueries."
            },
            {
                "category": "Window Functions (Analytics)",
                "title": "Rank Flights by Fare within Source Airport",
                "sql": (
                    "SELECT \n"
                    "    f.flight_no,\n"
                    "    a.city AS origin,\n"
                    "    f.fare,\n"
                    "    DENSE_RANK() OVER (PARTITION BY f.source_airport ORDER BY f.fare DESC) as fare_rank\n"
                    "FROM flight f\n"
                    "JOIN airport a ON f.source_airport = a.airport_id;"
                ),
                "notes": "Uses SQL windowing to rank fare tiers per origin hub without collapsing rows."
            }
        ]


# ==============================================================================
# UNIT 4: NORMALIZATION, FILE FORMATS & RECOVERY
# ==============================================================================
class Unit4NormalizationAndStorage:
    @staticmethod
    def get_normalization_breakdown() -> Dict[str, Any]:
        """Provides theoretical and mathematical breakdown of Normalization up to BCNF."""
        return {
            "unnormalized_anomalies": {
                "insertion_anomaly": "Cannot add an aircraft unless at least one flight is scheduled.",
                "deletion_anomaly": "Deleting a flight deletes passenger details if stored in a flat denormalized spreadsheet.",
                "update_anomaly": "Updating aircraft capacity requires updating every single passenger booking row, risking inconsistencies."
            },
            "stages": [
                {
                    "stage": "1NF (First Normal Form)",
                    "rule": "All column attributes must be atomic (no multivalued attributes, arrays, or repeating groups).",
                    "airport_example": "Phone numbers and baggage items are strictly single values. Multiple bags or passenger contacts are stored as distinct rows.",
                    "status": "Achieved"
                },
                {
                    "stage": "2NF (Second Normal Form)",
                    "rule": "Must be in 1NF, and no non-prime attribute may be partially functionally dependent on any candidate key (no partial dependencies).",
                    "airport_example": "In a hypothetical Booking(passenger_id, flight_id, passenger_name, flight_fare), passenger_name depends only on passenger_id. Decomposed into Passenger and Booking.",
                    "status": "Achieved"
                },
                {
                    "stage": "3NF (Third Normal Form)",
                    "rule": "Must be in 2NF, and no non-prime attribute is transitively dependent on the primary key (X -> Y -> Z). For every FD X -> A, X is a superkey or A is a prime attribute.",
                    "airport_example": "In Flight(flight_id, aircraft_id, aircraft_model, capacity), flight_id -> aircraft_id -> aircraft_model is transitive. Decomposed into separate Aircraft entity.",
                    "status": "Achieved"
                },
                {
                    "stage": "BCNF (Boyce-Codd Normal Form)",
                    "rule": "For every non-trivial functional dependency X -> Y, X must strictly be a Super Key.",
                    "airport_example": "Airport(airport_id, airport_code, airport_name, city, country). FDs: airport_id -> {code, name, city}, and airport_code -> {airport_id, name, city}. Both determinants are candidate superkeys. Relation is in BCNF.",
                    "status": "Achieved"
                }
            ],
            "functional_dependencies": [
                "FD1: flight_id -> {flight_no, source_airport, destination_airport, aircraft_id, departure_time, arrival_time, fare}",
                "FD2: flight_no -> {flight_id, source_airport, destination_airport, aircraft_id, departure_time, arrival_time, fare}",
                "FD3: airport_id -> {airport_name, city, country, airport_code}",
                "FD4: airport_code -> {airport_id, airport_name, city, country}",
                "FD5: aircraft_id -> {model, capacity, manufacturer, status}",
                "FD6: passenger_id -> {passenger_name, phone, flight_id, age}",
                "FD7: booking_id -> {passenger_id, flight_id, booking_date, seat_no, booking_status}",
                "FD8: payment_id -> {booking_id, payment_date, amount, payment_method, payment_status}"
            ],
            "lossless_decomposition_proof": "R1 ∩ R2 = {flight_id}. Since flight_id is the primary key (Super Key) of Flight (R1), the decomposition is strictly Lossless and Dependency Preserving."
        }

    @staticmethod
    def simulate_parquet_vs_row_storage(num_rows: int = 100000) -> Dict[str, Any]:
        """
        Simulates the Row Storage vs Columnar (Parquet) Storage scan comparison
        from the VIT Pune Unit 4 syllabus lecture slides:
        Query: SELECT passenger_name, age FROM passenger WHERE age > 30;
        """
        # Row fields: passenger_id (4B), passenger_name (50B), phone (15B), flight_id (4B), age (4B) -> total 77 bytes/row
        row_size_bytes = 77
        total_row_store_bytes = num_rows * row_size_bytes

        # Query only needs passenger_name (50B) and age (4B) -> 54 bytes
        # In Row-oriented: Must scan ALL 77 bytes per row to evaluate filter and project
        row_scanned_bytes = num_rows * row_size_bytes

        # In Columnar Parquet:
        # 1. Dictionary encoding & Snappy compression reduces age column (run-length + bit-packing ~ 1.5B/entry)
        # 2. Statistics footer (Min/Max per row group) skips irrelevant blocks entirely
        # 3. Only scans age column first (~1.5B), then fetches matching passenger_name chunks (~15B compressed)
        # Matching rows assuming 40% age > 30
        matching_ratio = 0.40
        parquet_age_scanned = num_rows * 1.5
        parquet_name_scanned = (num_rows * matching_ratio) * 18.0
        parquet_scanned_bytes = parquet_age_scanned + parquet_name_scanned

        compression_ratio = round(total_row_store_bytes / (num_rows * 22.0), 2)
        io_reduction_factor = round(row_scanned_bytes / parquet_scanned_bytes, 2)

        return {
            "num_rows": num_rows,
            "row_oriented_storage": {
                "row_width_bytes": row_size_bytes,
                "total_disk_size_mb": round(total_row_store_bytes / (1024 * 1024), 2),
                "io_read_mb": round(row_scanned_bytes / (1024 * 1024), 2),
                "strategy": "Full table row scan reads unnecessary columns (phone, flight_id)"
            },
            "parquet_columnar_storage": {
                "compressed_disk_size_mb": round((num_rows * 22.0) / (1024 * 1024), 2),
                "io_read_mb": round(parquet_scanned_bytes / (1024 * 1024), 2),
                "compression_ratio": f"{compression_ratio}:1",
                "io_speedup": f"{io_reduction_factor}x faster I/O throughput",
                "features": ["Row Groups", "Column Chunks", "Page Headers", "Dictionary Encoding", "Min/Max Stats Pruning"]
            }
        }

    @staticmethod
    def simulate_recovery_wal_checkpoint() -> Dict[str, Any]:
        """Simulates Write-Ahead Logging (WAL) and Checkpointing Crash Recovery (ARIES)."""
        log_records = [
            {"lsn": 101, "tid": "T1", "type": "START", "content": "Transaction 1 started"},
            {"lsn": 102, "tid": "T1", "type": "UPDATE", "content": "Flight AI101 seat 1A allocated (old: Free, new: Reserved)"},
            {"lsn": 103, "tid": "T2", "type": "START", "content": "Transaction 2 started (Payment processing)"},
            {"lsn": 104, "tid": "T1", "type": "COMMIT", "content": "T1 committed to WAL log buffer"},
            {"lsn": 105, "tid": "CHECKPOINT", "type": "CHECKPOINT", "content": "Fuzzy checkpoint written: Active transactions = {T2}"},
            {"lsn": 106, "tid": "T2", "type": "UPDATE", "content": "Booking 804 payment marked 'Paid' (old: Pending, new: Paid)"},
            {"lsn": 107, "tid": "T3", "type": "START", "content": "Transaction 3 started (Flight rescheduling)"},
            {"lsn": 108, "tid": "T3", "type": "UPDATE", "content": "Flight AI501 dep changed to 06:45 (old: 06:30, new: 06:45)"},
            {"lsn": 109, "tid": "CRASH", "type": "SYSTEM FAILURE", "content": "💥 Sudden power failure occurs before T2/T3 commit!"}
        ]

        # Recovery Steps
        analysis_step = "Analysis Phase: Scan forward from LSN 105 Checkpoint. Undo List = {T2, T3}, Redo List = {T1}"
        redo_step = "Redo Phase: Scan forward from min LSN. Reapply all logged updates to reconstruct crash state."
        undo_step = "Undo Phase: Scan backward from crash. Roll back active uncommitted transactions T3 and T2 to maintain Atomicity."

        return {
            "log": log_records,
            "recovery_phases": {
                "1_analysis": analysis_step,
                "2_redo": redo_step,
                "3_undo": undo_step
            },
            "final_db_state": "Database restored to 100% consistent state: T1 changes persisted, T2 and T3 safely aborted."
        }


# ==============================================================================
# UNIT 5: TRANSACTIONS, CONCURRENCY CONTROL & DISTRIBUTED SYSTEMS
# ==============================================================================
class Unit5TransactionsAndConcurrency:
    @staticmethod
    def test_conflict_serializability(schedule_actions: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyzes a schedule of read/write operations on data items (e.g. Flight Seat, Fare)
        using a Precedence Graph (Serialization Graph) to detect cycles.
        """
        if not schedule_actions:
            # Default schedule from syllabus:
            # S1: R1(A), W1(A), R2(A), W2(A), R1(B), W1(B), R2(B), W2(B) -> Conflict Serializable (T1 -> T2)
            # Cycle schedule: R1(A), W2(A), W1(A), R2(A)
            schedule_actions = [
                {"step": 1, "tid": "T1", "op": "READ", "item": "Seat_AI101_1A"},
                {"step": 2, "tid": "T2", "op": "READ", "item": "Seat_AI101_1A"},
                {"step": 3, "tid": "T1", "op": "WRITE", "item": "Seat_AI101_1A"},
                {"step": 4, "tid": "T2", "op": "WRITE", "item": "Fare_AI101"}
            ]

        # Find conflicting pairs: (T_i, T_j) where i != j, same item, and at least one is WRITE
        edges = set()
        transactions = set()
        for i in range(len(schedule_actions)):
            a1 = schedule_actions[i]
            transactions.add(a1["tid"])
            for j in range(i + 1, len(schedule_actions)):
                a2 = schedule_actions[j]
                if a1["tid"] != a2["tid"] and a1["item"] == a2["item"]:
                    if a1["op"] == "WRITE" or a2["op"] == "WRITE":
                        edges.add((a1["tid"], a2["tid"]))

        # Cycle detection using DFS
        adj = {t: [] for t in transactions}
        for u, v in edges:
            adj[u].append(v)

        has_cycle = False
        visited = {}
        rec_stack = {}
        cycle_path = []

        def dfs(node, path):
            nonlocal has_cycle, cycle_path
            visited[node] = True
            rec_stack[node] = True
            for neighbor in adj.get(node, []):
                if not visited.get(neighbor, False):
                    if dfs(neighbor, path + [neighbor]):
                        return True
                elif rec_stack.get(neighbor, False):
                    has_cycle = True
                    cycle_path = path + [neighbor]
                    return True
            rec_stack[node] = False
            return False

        for t in transactions:
            if not visited.get(t, False):
                if dfs(t, [t]):
                    break

        equivalent_serial = None
        if not has_cycle:
            # Topological sort
            topo_order = []
            visited_topo = set()

            def topo_dfs(n):
                visited_topo.add(n)
                for nxt in adj.get(n, []):
                    if nxt not in visited_topo:
                        topo_dfs(nxt)
                topo_order.append(n)

            for t in transactions:
                if t not in visited_topo:
                    topo_dfs(t)
            equivalent_serial = " -> ".join(reversed(topo_order))

        return {
            "schedule": schedule_actions,
            "conflicting_edges": [f"{u} -> {v}" for u, v in sorted(edges)],
            "is_conflict_serializable": not has_cycle,
            "has_cycle": has_cycle,
            "cycle_detected": " -> ".join(cycle_path) if has_cycle else "None (Acyclic graph)",
            "equivalent_serial_schedule": equivalent_serial or "None (Non-serializable)",
            "conclusion": "Schedule preserves ACID Isolation" if not has_cycle else "Schedule causes concurrency anomalies (Dirty Read/Lost Update)"
        }

    @staticmethod
    def get_distributed_sharding_model() -> Dict[str, Any]:
        """Models horizontal sharding and parallel database architecture for AirportDB."""
        return {
            "partitioning_strategy": "Range & Hash Partitioning based on Hub airport_id",
            "shards": [
                {
                    "shard_id": "Shard_West_BOM",
                    "region": "West India Hub (Mumbai - BOM)",
                    "primary_node": "db-west-01.airport.internal",
                    "replica_nodes": ["db-west-02.replica", "db-west-03.replica"],
                    "data_scope": "Flights departing from BOM, local gate assignments, west passenger bookings"
                },
                {
                    "shard_id": "Shard_North_DEL",
                    "region": "North India Hub (Delhi - DEL)",
                    "primary_node": "db-north-01.airport.internal",
                    "replica_nodes": ["db-north-02.replica"],
                    "data_scope": "Flights departing from DEL, northern route telemetry, VIP lounges"
                },
                {
                    "shard_id": "Shard_South_BLR",
                    "region": "South India Hub (Bangalore - BLR)",
                    "primary_node": "db-south-01.airport.internal",
                    "replica_nodes": ["db-south-02.replica"],
                    "data_scope": "Flights departing from BLR, southern tech corridor passenger records"
                }
            ],
            "parallel_query_types": {
                "Intra_Query_Parallelism": "Query scanning all 100,000 bookings partitions the table across 4 CPU cores running simultaneous partial sums, merging in 1 coordinator thread.",
                "Inter_Query_Parallelism": "Concurrent passenger ticket transactions from Mumbai and Delhi execute in parallel on independent shard nodes without lock contention."
            },
            "elasticsearch_index_mapping": {
                "index_name": "airport_passengers",
                "shards": 3,
                "replicas": 1,
                "inverted_index_fields": ["passenger_name", "flight_no", "source_city", "destination_city"],
                "search_speed": "< 10ms for fuzzy search 'Arun Sharma AI101' across 5 million passenger manifests."
            }
        }


# ==============================================================================
# UNIT 6: NOSQL, BIG DATA & DATA WAREHOUSING
# ==============================================================================
class Unit6NoSQLAndDataWarehouse:
    @staticmethod
    def get_nosql_multi_model_representations() -> Dict[str, Any]:
        """Demonstrates how AirportDB data is modeled across 4 NoSQL paradigms."""
        return {
            "1_Document_Store_MongoDB": {
                "paradigm": "JSON / BSON Document",
                "use_case": "Full passenger e-ticket & travel itinerary (Single nested document retrieval)",
                "sample_document": {
                    "_id": "TICKET-801",
                    "booking_id": 801,
                    "passenger": {"id": 501, "name": "Aarav Sharma", "age": 24, "phone": "9876501001"},
                    "flight": {"flight_no": "AI101", "origin": "Mumbai", "destination": "Delhi", "dep": "2026-07-20 09:00:00"},
                    "baggage": [{"tag": "BAG-01", "weight_kg": 18.5, "status": "Loaded"}],
                    "payment": {"amount": 5200.0, "method": "UPI", "status": "Paid"}
                }
            },
            "2_Key_Value_Store_Redis": {
                "paradigm": "Key-Value In-Memory Cache",
                "use_case": "Real-time Flight Radar status & seat availability lock cache (sub-millisecond TTL)",
                "sample_keys": {
                    "flight:AI101:status": "On-Time | Gate 12B | Boarding",
                    "flight:AI101:available_seats": 142,
                    "lock:seat:AI101:14B": "HELD_BY_USER_501_EXP_60s"
                }
            },
            "3_Column_Family_Cassandra": {
                "paradigm": "Wide-Column Family / Bigtable",
                "use_case": "IoT Aircraft Engine Telemetry & Sensor time-series data",
                "sample_row": {
                    "row_key": "AIRCRAFT_601_20260720",
                    "columns": {
                        "09:05:00:altitude": 10000,
                        "09:05:00:airspeed_knots": 420,
                        "09:05:00:engine_temp_c": 650,
                        "09:10:00:altitude": 28000
                    }
                }
            },
            "4_Graph_Database_Neo4j": {
                "paradigm": "Property Graph (Nodes & Directed Relationships)",
                "use_case": "Airport Route Network shortest-path traversal & Hub centrality",
                "cypher_query": "MATCH path = (a:Airport {code: 'BOM'})-[:FLIGHT*1..2]->(b:Airport {code: 'COK'}) RETURN path, length(path) ORDER BY length(path) ASC LIMIT 1;"
            }
        }

    @staticmethod
    def get_cap_theorem_comparison() -> Dict[str, Any]:
        """Provides comparative analysis of CAP Theorem and BASE vs ACID."""
        return {
            "CAP_Classification": {
                "CA_Systems": "Traditional RDBMS (MySQL, PostgreSQL) - Enforces Consistency & Availability during normal operations; halts partition.",
                "CP_Systems": "MongoDB, HBase - Guarantees Consistency & Partition Tolerance; blocks writes during split-brain.",
                "AP_Systems": "Cassandra, DynamoDB - Guarantees High Availability & Partition Tolerance; adopts Eventual Consistency."
            },
            "ACID_vs_BASE": [
                {"aspect": "Fundamental Goal", "ACID_Relational": "Pessimistic Data Integrity & Exact Consistency", "BASE_NoSQL": "Optimistic High Availability & Fault Tolerance"},
                {"aspect": "Consistency Model", "ACID_Relational": "Immediate Consistency (Every read sees latest write)", "BASE_NoSQL": "Eventual Consistency (Replicas synchronize over time)"},
                {"aspect": "Schema Structure", "ACID_Relational": "Rigid 3NF / BCNF Schema with Foreign Keys", "BASE_NoSQL": "Schemaless / Dynamic flexible documents"},
                {"aspect": "Scaling Strategy", "ACID_Relational": "Vertical Scaling (Scale-Up with bigger CPU/RAM)", "BASE_NoSQL": "Horizontal Scaling (Scale-Out across commodity clusters)"}
            ]
        }

    @staticmethod
    def get_data_warehouse_star_schema() -> Dict[str, Any]:
        """
        Defines the OLAP Data Warehouse Multi-Dimensional Star Schema
        for Airport Business Intelligence (BI) and Executive Analytics.
        """
        return {
            "Fact_Table": {
                "name": "Fact_Flight_Operations",
                "measures": [
                    "tickets_sold_count",
                    "total_revenue_amount",
                    "fuel_consumed_liters",
                    "departure_delay_minutes",
                    "arrival_delay_minutes",
                    "total_baggage_weight_kg"
                ],
                "foreign_keys": ["time_key", "airport_origin_key", "airport_dest_key", "aircraft_key", "fare_class_key"]
            },
            "Dimension_Tables": [
                {"name": "Dim_Time", "attributes": ["time_key", "date", "day_of_week", "month", "quarter", "year", "is_holiday"]},
                {"name": "Dim_Airport", "attributes": ["airport_key", "airport_code", "city", "state", "country", "timezone", "hub_category"]},
                {"name": "Dim_Aircraft", "attributes": ["aircraft_key", "model", "manufacturer", "seat_capacity", "engine_type"]},
                {"name": "Dim_Passenger_Segment", "attributes": ["segment_key", "loyalty_tier (Gold/Silver)", "age_group", "travel_type (Business/Leisure)"]}
            ],
            "OLAP_Operations": [
                {"operation": "Roll-up", "description": "Aggregates revenue from Daily -> Monthly -> Quarterly -> Yearly."},
                {"operation": "Drill-down", "description": "Breaks down total delay minutes from Airport level down to specific Gate or Flight number."},
                {"operation": "Slice", "description": "Selects a single dimension slice: All flights departing strictly from 'Mumbai' (BOM)."},
                {"operation": "Dice", "description": "Selects sub-cube: Origin in ('BOM', 'DEL'), Time in 'Q3-2026', and Aircraft Model = 'Airbus A320'."},
                {"operation": "Pivot", "description": "Rotates data matrix: Origin Hub on Y-axis, Months on X-axis, Total Ticket Revenue in cells."}
            ]
        }
