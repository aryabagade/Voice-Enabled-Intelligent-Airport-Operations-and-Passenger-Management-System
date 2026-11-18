# ✈️ Voice-Enabled Intelligent Airport Operations & DBMS Management System
### *Academic DBMS Course Project • Second Year B.Tech • VIT Pune*
**Course Code:** CS2227 / ML2302 (Database Management Systems)  
**Author:** Arya Bagade & Team  
**Repository:** [GitHub: Voice-Enabled-Intelligent-Airport-Operations-and-Passenger-Management-System](https://github.com/aryabagade/Voice-Enabled-Intelligent-Airport-Operations-and-Passenger-Management-System.git)

---

## 🌟 Executive Summary & Highlights

This project is an **end-to-end Voice-Enabled Relational Database Management System** tailored for modern international airport operations, passenger management, baggage tracking, and financial reconciliation. It seamlessly integrates:
1. **Two-Way Voice AI Operations**: One-touch microphone speech-to-text input, intelligent natural-language-to-SQL translation, and real-time browser-native Web Speech API text-to-speech audio responses.
2. **Comprehensive Course Syllabus Implementation (Units 1 to 6)**: Covers all theoretical and practical competencies defined in the **VIT Pune DBMS Curriculum** (Data Modeling, ER/EER Diagrams, Relational Algebra, Normalization up to BCNF, ACID Transactions, Conflict Serializability Precedence Graphs, Stored Procedures, Triggers, Parquet Columnar Storage, NoSQL paradigms, and Data Warehousing OLAP Star Schemas).
3. **Dual Frontends**:
   - **Interactive Streamlit Web Dashboard** (`app.py`): Real-time FIDS board, Voice query assistant, Stored Procedure & Trigger executor, and Interactive Syllabus Lab.
   - **Advanced Modern Web Portal** (`web_portal/index.html`): High-performance aviation cockpit glassmorphism portal with live animated airspace radar, Web Speech API microphone listener, dynamic table renderer, and custom SQL console.
4. **Dual-Backend Zero-Setup Database Engine**: Connects seamlessly to a live **MySQL** server (`AirportDB`), with automatic fallback to an in-memory/standalone **SQLite** database loaded directly from `AirportDB.sql`.

---

## 📚 Complete DBMS Syllabus Mapping (Units 1 to 6)

| Syllabus Unit | Course Outcome (CO) | Theoretical Concept | Practical System Implementation in Project |
| :--- | :--- | :--- | :--- |
| **Unit 1: Data Modeling & Architecture** | **CO1** (Design data models as per organizational requirements) | 3-Tier ANSI/SPARC Architecture, ER/EER Modeling, Constraints, Codd's 12 Rules | • 3-Schema layer mapping (External, Conceptual, Internal)<br>• Entity, Referential (FK), Domain, and CHECK constraints (`capacity > 0`, `age >= 0`, `fare >= 0`)<br>• Candidate keys (`airport_code UNIQUE`, `flight_no UNIQUE`)<br>• Evaluated against Codd's Rules (Rule 0 to 12). |
| **Units 2 & 3: Relational Algebra & SQL** | **CO3** (Develop database system using relational queries & PL/SQL) | Selection (σ), Projection (π), Joins (⨝), Set Ops (∪, −), Correlated Subqueries, Views | • Relational algebra converter to SQL queries<br>• Equi-joins, Left outer joins (idle aircraft), Self joins (connecting flight layovers)<br>• Views: `v_flight_schedule`, `v_passenger_manifest`, `v_revenue_summary`<br>• GROUP BY, HAVING, and Correlated Subqueries. |
| **Unit 4: Relational Design & Storage** | **CO2 & CO4** (Synthesize schema to normal form; understand storage & recovery) | Functional Dependencies, Normalization (1NF ➔ BCNF), Lossless Join, Parquet vs Row, WAL Recovery | • Step-by-step normal form breakdown (1NF to BCNF) with formal FDs<br>• Lossless join decomposition proof ($R_1 \cap R_2 \rightarrow R_1$)<br>• Columnar Parquet vs Row Storage simulation showing 10x I/O reduction via dictionary encoding<br>• Write-Ahead Logging (WAL) and ARIES checkpoint undo/redo crash recovery. |
| **Unit 5: Transaction Management & Distributed Systems** | **CO4 & CO5** (Concurrency control, recovery, parallel & distributed databases) | ACID Properties, Schedules, Conflict Serializability, Strict 2PL, Sharding | • Precedence Graph cycle detection algorithm for Conflict Serializability<br>• Stored Procedure `sp_book_flight` with `START TRANSACTION`, `SAVEPOINT`, and `ROLLBACK`<br>• Multi-hub horizontal sharding model (BOM, DEL, BLR) and Inter vs Intra-query parallelism<br>• Elasticsearch full-text inverted index architecture. |
| **Unit 6: NoSQL, Big Data & Data Warehousing** | **CO6** (Emerging trends: NoSQL, Big Data, Data Warehouses) | NoSQL Stores (Document, Key-Value, Columnar, Graph), CAP Theorem, HDFS/MapReduce, Star Schema | • 4 NoSQL representations: MongoDB JSON passenger manifests, Redis radar cache, Cassandra IoT telemetry, Neo4j flight graphs<br>• CAP Theorem & BASE properties comparative matrix<br>• HDFS NameNode/DataNode architecture<br>• Multi-Dimensional OLAP Star Schema (`Fact_Flight_Operations`) with Roll-up, Drill-down, Slice, Dice, and Pivot. |

---

## 🗄️ Relational Database Architecture

The system is structured as a **strictly normalized 3NF / BCNF relational database** containing the following connected tables:

```
                  ┌─────────────┐
                  │   AIRPORT   │ (airport_id, airport_name, city, country, airport_code)
                  └──────┬──────┘
                         │ 1:N (Departs From / Arrives At)
                         ▼
┌──────────────┐  1:N   ┌─────────────┐
│   AIRCRAFT   ├───────►│   FLIGHT    │ (flight_id, flight_no, source_airport,
└──────────────┘ (Uses) └──────┬──────┘  destination_airport, aircraft_id, dep, arr, fare)
                               │ 1:N (Contains)
                               ▼
┌──────────────┐  1:N   ┌─────────────┐   1:N   ┌─────────────┐
│  PASSENGER   ├───────►│   BOOKING   ├────────►│   PAYMENT   │ (payment_id, booking_id,
└──────────────┘ (Makes)└──────┬──────┘  (Has)  └─────────────┘  date, amount, method, status)
                               │ 1:N (Contains)
                               ▼
                        ┌─────────────┐
                        │   BAGGAGE   │ (baggage_id, booking_id, weight, type, status)
                        └─────────────┘
                               ▲
                               │ Trigger-Logged
                        ┌─────────────┐
                        │FLIGHT_AUDIT │ (audit_id, flight_id, operation_type, message, time)
                        └─────────────┘
```

### Verified Table Record Counts (from Academic Evaluation Database)
- **`airport`**: 24 major domestic and international hubs (`BOM`, `DEL`, `BLR`, `HYD`, `PUN`, `GOI`, `COK`, `CCU`, etc.)
- **`aircraft`**: 22 commercial aircraft (Airbus A320/A321/A330/A350, Boeing 737/747/777/787)
- **`flight`**: 23 active commercial routes with schedules and fares
- **`passenger`**: 43 registered passengers with contact and age demographics
- **`booking`**: 40 confirmed ticket reservations with seat assignments (`1A`, `2B`, `3C`, etc.)
- **`payment`**: 30 billing transactions via UPI, Credit/Debit Card, and NetBanking
- **`baggage`**: 40 registered luggage tags with weights and load statuses
- **`flight_audit`**: Automatically populated audit logs generated by SQL triggers (`AFTER UPDATE`, `AFTER INSERT`, `AFTER DELETE`)

---

## 🎙️ Two-Way Voice Architecture

```
 User Speaks into Mic (e.g. "Flights from Mumbai")
                     │
                     ▼
 [Web Speech API / Audio Recorder]
                     │
                     ▼
           [Query Text Recognized]
                     │
                     ▼
           [Voice Query Engine]
                     │  Translates Natural Language to 3NF SQL
                     ▼
            [Relational Database]
                     │  Executes SELECT / Joins / Aggregations
                     ▼
  ┌──────────────────┴──────────────────┐
  ▼                                     ▼
[Pandas DataFrame]            [Voice Speech Output]
- Rendered in interactive     - Spoken aloud via Web Speech API
  data tables                 - Audio replay button
- CSV Export available        - Speed controls
```

### Sample Supported Voice Queries
- *"Show all flights from Mumbai"* ➔ Multi-table join querying BOM departures with aircraft and fare.
- *"Flights arriving in Delhi"* ➔ Inbound flight schedule with arrival timestamps.
- *"Passengers on flight 301"* ➔ Live passenger manifest for flight AI101.
- *"Show baggage status"* ➔ Retrieves checked-in baggage weight and loading status.
- *"Show total revenue"* ➔ Aggregates ticket payments by route using `GROUP BY` and `SUM()`.
- *"Show available aircraft"* ➔ Queries fleet availability ordered by seating capacity.
- *"Flights under 6000"* ➔ Filtered price query sorted by fare ascending.
- *"Show audit history"* ➔ Inspects trigger-generated audit trail.

---

## 💻 How to Run the Applications

### 1. Clone the Repository
```bash
git clone https://github.com/aryabagade/Voice-Enabled-Intelligent-Airport-Operations-and-Passenger-Management-System.git
cd Voice-Enabled-Intelligent-Airport-Operations-and-Passenger-Management-System
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch Frontend Option A: Streamlit Web Dashboard
```bash
streamlit run app.py
```
*Opens automatically at `http://localhost:8501`.*

### 4. Launch Frontend Option B: Modern Aviation Web Portal
You can run the web portal server:
```bash
python web_portal/api_server.py
```
*Opens at `http://localhost:8080` (or double-click `web_portal/index.html` to open directly in any web browser).*

---

## ⚡ Stored Procedures & Triggers (PL/SQL)

The system includes simulated and native PL/SQL stored procedures and triggers:
1. **`sp_book_flight`**:
   - Executes an atomic ACID transaction.
   - Checks seat availability to prevent double booking.
   - Inserts passenger, creates booking, registers payment, allocates baggage tag.
   - Uses `SAVEPOINT` and issues `ROLLBACK` on violation, or `COMMIT` on success.
2. **`sp_reschedule_flight`**:
   - Updates departure and arrival times.
   - Automatically triggers `trg_after_flight_update` to log changes into `flight_audit`.
3. **`sp_cancel_booking`**:
   - Updates booking status to `Cancelled`.
   - Sets payment status to `Refunded`.
   - Records cancellation event in `flight_audit`.
4. **`trg_after_flight_update`**:
   - Database trigger monitoring the `flight` table and creating audit records without application intervention.

---

## 🎓 Academic Defense & Viva Voce Quick Reference

- **Q: Why is the database in BCNF?**
  - *A: In all relations (Airport, Aircraft, Flight, Passenger, Booking, Payment), every non-trivial functional dependency $X \rightarrow Y$ has a determinant $X$ that is strictly a Candidate/Super Key. No transitive or partial dependencies exist.*
- **Q: How does the system handle concurrent seat bookings?**
  - *A: Using Strict Two-Phase Locking (2PL) and transaction isolation (`REPEATABLE READ`). A unique constraint and verification check ensures no two transactions can allocate the same seat on the same flight simultaneously.*
- **Q: Why simulate Parquet storage in Unit 4?**
  - *A: To demonstrate the difference between row-oriented scans (which read all attributes like phone numbers and IDs when only checking passenger age) versus columnar chunk scans with dictionary encoding, reducing disk I/O by over 80%.*
- **Q: How does speech synthesis work without external cloud dependencies?**
  - *A: It utilizes the browser's native HTML5 `window.speechSynthesis` (Web Speech API), providing zero-latency, offline voice output.*
