# 🎙️ Voice-Enabled Intelligent Airport Operations and Passenger Management System

An intelligent, interactive airport operations and passenger assistance dashboard powered by **Streamlit**, **Relational DBMS (MySQL & SQLite)**, and **Voice AI (Speech-to-Text & Text-to-Speech)**.

---

## ✈️ System Overview

This system provides a unified interface for airport operational staff and passengers. Users can **speak naturally through their microphone** or type queries to interact with the relational airport database. The system translates spoken language into **synthesized 3NF relational SQL**, queries the live database, visualizes the records in interactive tables, and **speaks the result back out loud** through real-time speech synthesis.

```
 🎙️ Speech Input (Mic)
       │
       ▼
 [Streamlit Audio Capture]  ──> Transcribes spoken speech to query text
       │
       ▼
 [Voice Query Engine]       ──> Synthesizes relational SQL (Equi-Joins & Filters)
       │
       ▼
 [Database Execution]      ──> Queries MySQL AirportDB (or local fallback)
       │
       ├───► 📊 Visual Display: Dataframe tables, FIDS schedule & execution metrics
       └───► 🔊 Voice Audio Output: Speaks response through browser Text-to-Speech (TTS)
```

---

## 🚀 Key Features

1. **🎙️ Two-Way Voice Interaction**:
   - **Voice Input**: One-click microphone recording via `streamlit-mic-recorder` that captures your spoken question directly from the browser.
   - **Voice Output (Audio Feedback)**: Automatically synthesizes and speaks back concise, natural conversational answers using the browser's native **Web Speech API** and embedded audio playback.
   - **Replay & Speed Controls**: Includes an explicit **🔊 Replay Voice Response** button and speech rate controls.

2. **🛠️ Intelligent Voice-to-SQL Query Engine**:
   - Translates conversational queries into accurate relational SQL statements with multi-table `JOIN`, `WHERE`, and `ORDER BY` operations.
   - Automatically correlates operational entities across the **6 Core Tables**:
     - `airport` (IATA hubs, cities, countries)
     - `aircraft` (Fleet models, seating capacity, status)
     - `flight` (Flight numbers, routes, departure/arrival schedules, fares)
     - `passenger` (Names, contact phones, ages, flight mappings)
     - `booking` (Seat allocations, reservation statuses)
     - `payment` (Transactions, methods: UPI/Card/NetBanking, payment status)

3. **🔄 Dual-Backend Database Architecture**:
   - **Primary Backend**: Connects directly to a live **MySQL** server (`AirportDB`).
   - **Zero-Setup Standalone Mode**: If MySQL is offline or not installed, automatically loads and queries an in-memory/local SQLite database generated directly from `AirportDB.sql`. Runs anywhere out-of-the-box!

4. **🛫 Live Flight Information Display System (FIDS)**:
   - Real-time departure and arrival board connecting source and destination hubs with search filtering.

5. **🗄️ Database Explorer & Custom SQL Terminal**:
   - Inspect raw records, column definitions, and primary/foreign key connections across all tables.
   - Built-in SQL query editor for viva voce evaluation and custom analytical queries.

---

## 🗣️ Supported Sample Voice Queries

You can click the microphone icon and speak any of the following queries:

| Spoken Query | SQL Operation | Spoken Audio Output Example |
| :--- | :--- | :--- |
| *"Show all flights from Mumbai"* | Multi-table Equi-Join (`flight` + `airport`) filtering by origin | *"Found 6 flights departing from Mumbai. The earliest departure is flight AI101 to Delhi with a fare of 5,300 rupees."* |
| *"Flights arriving in Delhi"* | Multi-table Equi-Join filtering by destination city | *"Found 5 flights arriving in Delhi. The earliest is flight AI101 from Mumbai."* |
| *"Passengers on flight 301"* | 3-table join (`passenger` + `booking` + `flight`) for live manifest | *"Flight 301 has 2 passengers on the manifest, including Aarav Sharma and Diya Kapoor."* |
| *"Find passenger Arya"* | Queries passenger profile, seat allocation, and flight status | *"Found passenger Arya assigned to flight AI101 in seat 1A."* |
| *"Show available aircraft"* | Queries fleet with `status = 'Available'` ordered by capacity | *"Retrieved 20 aircraft records. Models include Boeing 777 with capacity of 396 passengers."* |
| *"Flights cheaper than 6000"* | Queries flights filtered by `fare <= 6000` | *"Found 13 flights with fares under 6,000 rupees. The most affordable is flight AI511 at 4,500 rupees."* |
| *"Show payments made via UPI"* | Queries payment transactions with `payment_method = 'UPI'` | *"Found 14 payment records with a total value of 81,000 rupees."* |
| *"How many passengers are registered?"* | Aggregate `COUNT(*)` query on passenger table | *"There are currently 43 registered passengers in the Airport database."* |
| *"Show bookings"* | Retrieves reservations with passenger and seat status | *"Retrieved 40 active flight reservations from the Booking table."* |

---

## 💻 Installation & Quickstart

### 1. Clone the Repository
```bash
git clone https://github.com/aryabagade/Voice-Enabled-Intelligent-Airport-Operations-and-Passenger-Management-System.git
cd Voice-Enabled-Intelligent-Airport-Operations-and-Passenger-Management-System
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit Application
```bash
streamlit run app.py
```

*The application will launch in your default web browser at `http://localhost:8501`.*

---

## ⚙️ Database Configuration (Optional MySQL Setup)

- By default, the application runs in **Standalone Mode** using pre-populated data from `AirportDB.sql`.
- To connect to your local MySQL instance:
  1. Open the sidebar in the Streamlit web dashboard.
  2. Select **Connect to Custom MySQL Server**.
  3. Enter your MySQL host, port, username, password, and database name (`AirportDB`).
  4. Click **🔄 Test & Reconnect**.

To load the database dump into your MySQL server manually:
```bash
mysql -u root -p < AirportDB.sql
```

---

## 🛠️ Technology Stack

- **Frontend & App Framework**: [Streamlit](https://streamlit.io/)
- **Audio & Voice Input**: `streamlit-mic-recorder` (HTML5 Audio Web API)
- **Voice Synthesis & Audio Output**: Web Speech API (`SpeechSynthesis`) & `gTTS`
- **Database Management Systems**: MySQL 8.0 & SQLite3
- **Data Manipulation & Querying**: Pandas, Python SQL Connectors

---

## 📄 License
This project is developed for academic evaluation and demonstration of Voice-Enabled Relational Database Management Systems.
