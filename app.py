import os
import io
import time
import json
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from streamlit_mic_recorder import speech_to_text

import db_manager
import voice_query_engine
import syllabus_engine

# ==============================================================================
# 1. PAGE CONFIGURATION & THEME
# ==============================================================================
st.set_page_config(
    page_title="Voice-Enabled Airport Operations & DBMS Lab",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Aviation Cyber-Theme CSS
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background: radial-gradient(circle at 50% 10%, #0d1e3d 0%, #070f1e 85%);
        color: #FFFFFF;
    }
    
    /* Top Header Banner */
    .hero-banner {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 58, 102, 0.75) 100%);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 14px;
        padding: 22px 28px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    }
    
    .hero-title {
        font-size: 1.85rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #FFFFFF;
        margin-bottom: 6px;
    }
    .hero-title span {
        color: #38BDF8;
    }
    
    .hero-subtitle {
        font-size: 0.95rem;
        color: #94A3B8;
        font-weight: 400;
    }

    /* Metric Cards */
    .metric-card {
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 10px;
        padding: 14px 18px;
        text-align: center;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
    }
    .metric-value {
        font-size: 1.6rem;
        font-weight: 800;
        color: #38BDF8;
        font-family: monospace;
    }
    .metric-label {
        font-size: 0.76rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #94A3B8;
        margin-top: 2px;
    }

    /* Spoken Answer Banner */
    .voice-response-card {
        background: linear-gradient(135deg, rgba(22, 36, 62, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%);
        border-left: 5px solid #F59E0B;
        border-top: 1px solid rgba(245, 158, 11, 0.3);
        border-right: 1px solid rgba(245, 158, 11, 0.3);
        border-bottom: 1px solid rgba(245, 158, 11, 0.3);
        border-radius: 10px;
        padding: 16px 20px;
        margin: 14px 0;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    }
    .voice-response-title {
        font-size: 0.8rem;
        font-weight: 700;
        color: #F59E0B;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 6px;
    }
    .voice-response-text {
        font-size: 1.05rem;
        color: #FFFFFF;
        font-weight: 500;
        line-height: 1.45;
    }

    /* Badges */
    .badge-on-time {
        background: rgba(16, 185, 129, 0.2);
        color: #10B981;
        border: 1px solid #10B981;
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: 700;
        font-size: 0.72rem;
    }
    .badge-delayed {
        background: rgba(244, 63, 94, 0.2);
        color: #F43F5E;
        border: 1px solid #F43F5E;
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: 700;
        font-size: 0.72rem;
    }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# 2. VOICE SYNTHESIS HELPER (Browser Web Speech API + Optional Audio Player)
# ==============================================================================
def render_voice_output(text: str, auto_play: bool = True, speech_rate: float = 1.0):
    """
    Renders speech audio in the user's browser using two complementary mechanisms:
    1. Browser-native Web Speech API (speechSynthesis) - works 100% offline with zero latency
    2. Embedded gTTS audio player (if network is available)
    """
    clean_text = text.replace('"', '\\"').replace("'", "\\'").replace("\n", " ").replace("\r", " ")
    
    js_code = f"""
    <div style="display: flex; align-items: center; gap: 10px; margin-top: 6px;">
        <button id="tts-btn" onclick="speakNow()" style="
            background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
            color: #ffffff;
            border: 1px solid #38bdf8;
            border-radius: 6px;
            padding: 7px 16px;
            cursor: pointer;
            font-size: 13px;
            font-weight: 700;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            box-shadow: 0 4px 12px rgba(2, 132, 199, 0.3);
            transition: all 0.2s;
        ">
            🔊 Replay Voice Response
        </button>
        <span id="tts-status" style="font-size: 12px; color: #94A3B8;">(Click to listen)</span>
    </div>

    <script>
        function speakNow() {{
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                var msg = new SpeechSynthesisUtterance("{clean_text}");
                msg.rate = {speech_rate};
                msg.pitch = 1.0;
                msg.lang = 'en-US';
                
                var statusSpan = document.getElementById('tts-status');
                if (statusSpan) statusSpan.innerText = "🎙️ Speaking...";
                msg.onend = function() {{
                    if (statusSpan) statusSpan.innerText = "✓ Finished speaking";
                }};
                
                window.speechSynthesis.speak(msg);
            }}
        }}
        {'speakNow();' if auto_play else ''}
    </script>
    """
    components.html(js_code, height=52)

    # Optional server-side gTTS audio player fallback
    try:
        from gtts import gTTS
        fp = io.BytesIO()
        tts = gTTS(text=text, lang="en", slow=False)
        tts.write_to_fp(fp)
        fp.seek(0)
        st.audio(fp.read(), format="audio/mp3", start_time=0)
    except Exception:
        pass


# ==============================================================================
# 3. SIDEBAR CONFIGURATION & DATABASE CONNECTIVITY
# ==============================================================================
with st.sidebar:
    st.markdown("### ✈️ Airport Operations Hub")
    st.caption("Intelligent Relational DBMS Assistant")
    
    st.divider()
    
    st.markdown("#### ⚙️ Database Configuration")
    db_mode = st.radio(
        "Select Database Mode:",
        ["Auto-Detect / Standalone (SQLite)", "Connect to Custom MySQL Server"],
        index=0
    )
    
    mysql_cfg = None
    force_sqlite = True
    
    if db_mode == "Connect to Custom MySQL Server":
        force_sqlite = False
        with st.expander("MySQL Credentials", expanded=True):
            host = st.text_input("Host", value="localhost")
            port = st.number_input("Port", value=3306, step=1)
            user = st.text_input("User", value="root")
            password = st.text_input("Password", value="1234", type="password")
            database = st.text_input("Database", value="AirportDB")
            mysql_cfg = {
                "host": host,
                "port": port,
                "user": user,
                "password": password,
                "database": database
            }

    # Voice Output Settings
    st.markdown("#### 🔊 Audio Output Settings")
    auto_speak = st.checkbox("Auto-play voice speech response", value=True)
    voice_speed = st.slider("Speech Speed Rate", min_value=0.7, max_value=1.4, value=1.0, step=0.1)

    st.divider()

    # Web Portal Link
    st.markdown("#### 🌐 Advanced Web Portal")
    st.info("A standalone modern web portal is included in `web_portal/index.html`. Open it directly or launch via `python web_portal/api_server.py`.")


# Establish Database Connection
conn, is_mysql, conn_status = db_manager.get_db_connection(mysql_config=mysql_cfg, force_sqlite=force_sqlite)


# ==============================================================================
# 4. TOP METRICS DASHBOARD
# ==============================================================================
col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)

cnt_flights = db_manager.get_table_row_count(conn, "flight", is_mysql)
cnt_passengers = db_manager.get_table_row_count(conn, "passenger", is_mysql)
cnt_airports = db_manager.get_table_row_count(conn, "airport", is_mysql)
cnt_aircraft = db_manager.get_table_row_count(conn, "aircraft", is_mysql)
cnt_bookings = db_manager.get_table_row_count(conn, "booking", is_mysql)

with col_m1:
    st.markdown(f"""<div class="metric-card"><div class="metric-value">{cnt_flights}</div><div class="metric-label">Scheduled Flights</div></div>""", unsafe_allow_html=True)
with col_m2:
    st.markdown(f"""<div class="metric-card"><div class="metric-value">{cnt_passengers}</div><div class="metric-label">Passengers</div></div>""", unsafe_allow_html=True)
with col_m3:
    st.markdown(f"""<div class="metric-card"><div class="metric-value">{cnt_airports}</div><div class="metric-label">Airport Hubs</div></div>""", unsafe_allow_html=True)
with col_m4:
    st.markdown(f"""<div class="metric-card"><div class="metric-value">{cnt_aircraft}</div><div class="metric-label">Fleet Size</div></div>""", unsafe_allow_html=True)
with col_m5:
    st.markdown(f"""<div class="metric-card"><div class="metric-value">{cnt_bookings}</div><div class="metric-label">Bookings</div></div>""", unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 14px;'></div>", unsafe_allow_html=True)

# Connection Status Alert
if is_mysql:
    st.success(f"🟢 {conn_status}")
else:
    st.info(f"🔵 {conn_status} (Zero-setup local standalone mode)")


# Top Hero Banner
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">🎙️ Voice-Enabled <span>Airport Operations</span> & DBMS System</div>
    <div class="hero-subtitle">
        Speak queries into your microphone to inspect flights, passenger manifests, baggage, revenue, transactions (ACID), and all 6 units of the DBMS course syllabus.
    </div>
</div>
""", unsafe_allow_html=True)


# Initialize Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_query" not in st.session_state:
    st.session_state.last_query = "Flights from Mumbai"
if "trigger_query" not in st.session_state:
    st.session_state.trigger_query = None


# Navigation Tabs
tab_voice, tab_fids, tab_tables, tab_proc, tab_syllabus, tab_sql = st.tabs([
    "🎙️ Voice Assistant & Queries",
    "🛫 Live Flight Board (FIDS)",
    "🗄️ Database Tables Explorer",
    "⚡ Stored Procedures & Triggers",
    "📚 DBMS Syllabus Lab (Units 1-6)",
    "💻 Custom SQL Terminal"
])


# ==============================================================================
# TAB 1: VOICE ASSISTANT & PASSENGER CONCIERGE
# ==============================================================================
with tab_voice:
    st.subheader("🗣️ Speak or Type Your Airport Query")
    st.caption("Click the microphone below to speak, type in the text box, or tap any quick suggestion chip.")

    col_input1, col_input2 = st.columns([1.2, 3])
    
    with col_input1:
        st.markdown("**🎙️ Audio Input (Microphone):**")
        spoken_audio = speech_to_text(
            language="en",
            start_prompt="🎙️ Click to Speak Query",
            stop_prompt="⏹️ Stop Recording",
            just_once=True,
            use_container_width=True,
            key="mic_audio_input"
        )
    
    with col_input2:
        st.markdown("**⌨️ Text Input (Alternative):**")
        typed_text = st.text_input(
            label="Type your question here",
            placeholder="e.g. 'Show all flights from Mumbai', 'Show baggage status', 'Passengers on AI101'...",
            label_visibility="collapsed",
            key="text_query_input"
        )

    # Quick Suggestion Chips (1-Click Query Triggers)
    st.markdown("<div style='font-size: 0.8rem; font-weight: 700; color: #94A3B8; margin-top: 10px;'>💡 QUICK VOICE QUERY SUGGESTIONS:</div>", unsafe_allow_html=True)
    chip_cols = st.columns(6)
    
    prompts = [
        ("🛫 Flights from Mumbai", "Show flights from Mumbai"),
        ("🛬 Flights to Delhi", "Flights to Delhi"),
        ("🧳 Baggage Status", "Show baggage status"),
        ("💰 Total Revenue", "Show total revenue"),
        ("✈️ Available Aircraft", "Show available aircraft"),
        ("📜 Audit History", "Show audit log")
    ]
    
    for i, (label, query_str) in enumerate(prompts):
        if chip_cols[i].button(label, use_container_width=True, key=f"chip_{i}"):
            st.session_state.trigger_query = query_str

    # Determine Active Query
    active_query = None
    if spoken_audio and spoken_audio.strip():
        active_query = spoken_audio.strip()
    elif typed_text and typed_text.strip():
        active_query = typed_text.strip()
    elif st.session_state.trigger_query:
        active_query = st.session_state.trigger_query
        st.session_state.trigger_query = None

    if not active_query and not st.session_state.chat_history:
        active_query = st.session_state.last_query

    # Process and Render Query
    if active_query:
        st.session_state.last_query = active_query
        start_time = time.time()
        
        # Call Query Engine
        result = voice_query_engine.process_query(active_query, conn, is_mysql=is_mysql)
        exec_ms = round((time.time() - start_time) * 1000, 1)

        st.session_state.chat_history.insert(0, {
            "query": active_query,
            "category": result["category"],
            "spoken": result["spoken_text"],
            "sql": result["sql"],
            "time": time.strftime("%H:%M:%S")
        })
        if len(st.session_state.chat_history) > 6:
            st.session_state.chat_history.pop()

        st.divider()

        # Query Details Header
        col_res1, col_res2 = st.columns([3, 1])
        with col_res1:
            st.markdown(f"#### 🎯 {result['category']}")
            st.markdown(f"**Recognized Voice Input:** *\"{active_query}\"*")
        with col_res2:
            st.markdown(
                f"<div style='text-align: right; color: #10B981; font-weight: 700; font-size: 0.85rem; margin-top: 10px;'>"
                f"⚡ Executed in {exec_ms} ms"
                f"</div>",
                unsafe_allow_html=True
            )

        # 1. Spoken Output Card (Text-To-Speech Output)
        st.markdown(f"""
        <div class="voice-response-card">
            <div class="voice-response-title">🔊 Spoken Voice Response (Audio Output)</div>
            <div class="voice-response-text">{result['spoken_text']}</div>
        </div>
        """, unsafe_allow_html=True)

        render_voice_output(
            text=result["spoken_text"],
            auto_play=auto_speak,
            speech_rate=voice_speed
        )

        # 2. Results Data Table
        if result["dataframe"] is not None and not result["dataframe"].empty:
            st.markdown(f"**Results ({len(result['dataframe'])} records found):**")
            st.dataframe(result["dataframe"], use_container_width=True)
            
            csv_data = result["dataframe"].to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Results as CSV",
                data=csv_data,
                file_name="airport_query_results.csv",
                mime="text/csv"
            )
        elif result["dataframe"] is not None and result["dataframe"].empty:
            st.warning("Zero records found matching your query criteria.")

        # 3. Synthesized SQL Query Inspector
        with st.expander("🛠️ View Synthesized Relational SQL Query", expanded=False):
            st.code(result["sql"], language="sql")
            st.caption("Formulated using 3NF relational schema joins and constraints.")


# ==============================================================================
# TAB 2: LIVE FLIGHT INFORMATION DISPLAY SYSTEM (FIDS)
# ==============================================================================
with tab_fids:
    st.subheader("🛫 Real-Time Flight Information Display System (FIDS)")
    st.caption("Live digital flight schedule connecting source and destination hubs.")

    fids_sql = """
    SELECT 
        f.flight_no AS 'Flight',
        a1.city AS 'Origin',
        a2.city AS 'Destination',
        f.departure_time AS 'Scheduled Departure',
        f.arrival_time AS 'Estimated Arrival',
        ac.model AS 'Aircraft',
        f.fare AS 'Fare (INR)'
    FROM flight f
    JOIN airport a1 ON f.source_airport = a1.airport_id
    JOIN airport a2 ON f.destination_airport = a2.airport_id
    LEFT JOIN aircraft ac ON f.aircraft_id = ac.aircraft_id
    ORDER BY f.departure_time ASC;
    """
    fids_df, _ = db_manager.execute_query(conn, fids_sql, is_mysql=is_mysql)
    
    if not fids_df.empty:
        search_fids = st.text_input("🔍 Filter FIDS by City or Flight No:", placeholder="e.g. Mumbai, Delhi, AI101...")
        if search_fids:
            s_term = search_fids.strip().lower()
            fids_df = fids_df[
                fids_df['Flight'].str.lower().str.contains(s_term) |
                fids_df['Origin'].str.lower().str.contains(s_term) |
                fids_df['Destination'].str.lower().str.contains(s_term)
            ]
        
        st.dataframe(fids_df, use_container_width=True)
    else:
        st.info("No active flights found on the schedule.")


# ==============================================================================
# TAB 3: DATABASE EXPLORER
# ==============================================================================
with tab_tables:
    st.subheader("🗄️ Airport Database Tables Explorer")
    st.caption("Browse tables, view columns, inspect primary/foreign keys, and examine raw records.")

    all_tables = db_manager.get_table_names(conn, is_mysql=is_mysql)
    
    if all_tables:
        col_t1, col_t2 = st.columns([1, 2])
        with col_t1:
            sel_table = st.selectbox("Select a table to inspect:", all_tables)
            limit_rows = st.slider("Record Limit:", min_value=10, max_value=200, value=50, step=10)
        
        tbl_data, _ = db_manager.execute_query(conn, f"SELECT * FROM {sel_table} LIMIT {limit_rows}", is_mysql=is_mysql)
        
        with col_t2:
            st.markdown(f"#### Table: `{sel_table}`")
            row_cnt = db_manager.get_table_row_count(conn, sel_table, is_mysql=is_mysql)
            st.caption(f"Total Rows: **{row_cnt}** | Displaying up to **{limit_rows}** records.")

        if not tbl_data.empty:
            st.dataframe(tbl_data, use_container_width=True)
        else:
            st.info(f"Table '{sel_table}' is currently empty.")


# ==============================================================================
# TAB 4: STORED PROCEDURES & TRIGGERS STUDIO
# ==============================================================================
with tab_proc:
    st.subheader("⚡ Stored Procedures & Triggers Execution Studio")
    st.caption("Demonstrates atomic PL/SQL operations, Savepoints, Rollbacks, and Audit Triggers (Units 5 & 6).")

    proc_mode = st.radio("Choose Stored Procedure to Execute:", [
        "1. sp_book_flight (Atomic ACID Booking with Payment & Baggage)",
        "2. sp_reschedule_flight (Updates Flight & Fires Audit Trigger)",
        "3. sp_cancel_booking (Rolls back reservation and refunds payment)"
    ])

    if "sp_book_flight" in proc_mode:
        st.markdown("#### 🎫 Execute `sp_book_flight`")
        col_b1, col_b2, col_b3 = st.columns(3)
        with col_b1:
            p_name = st.text_input("Passenger Name", value="Aditi Sharma")
            p_phone = st.text_input("Phone Number", value="9876509999")
            p_age = st.number_input("Age", min_value=1, max_value=120, value=25)
        with col_b2:
            p_flight = st.selectbox("Select Flight", [301, 302, 303, 701, 702, 703])
            p_seat = st.text_input("Seat No", value="18A")
        with col_b3:
            p_method = st.selectbox("Payment Method", ["UPI", "Card", "NetBanking"])

        if st.button("🚀 Execute Atomic Booking (START TRANSACTION)"):
            success, msg, logs = db_manager.execute_book_flight_transaction(
                conn, p_name, p_phone, p_age, p_flight, p_seat, p_method, is_mysql=is_mysql
            )
            if success:
                st.success(msg)
            else:
                st.error(msg)
            
            with st.expander("📝 View Transaction Execution Step-by-Step Log", expanded=True):
                for l in logs:
                    st.code(l, language="sql")

    elif "sp_reschedule_flight" in proc_mode:
        st.markdown("#### ⏰ Execute `sp_reschedule_flight`")
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            rf_id = st.selectbox("Flight ID to Reschedule", [301, 302, 303, 701])
            new_dep = st.text_input("New Departure Time", value="2026-07-20 09:30:00")
        with col_r2:
            new_arr = st.text_input("New Arrival Time", value="2026-07-20 11:30:00")

        if st.button("🔄 Execute Reschedule (Fires trg_after_flight_update)"):
            success, msg, logs = db_manager.execute_reschedule_flight_transaction(
                conn, rf_id, new_dep, new_arr, is_mysql=is_mysql
            )
            if success:
                st.success(msg)
            else:
                st.error(msg)

            with st.expander("📜 Check Trigger Audit Trail"):
                audit_df, _ = db_manager.execute_query(conn, "SELECT * FROM flight_audit ORDER BY audit_id DESC LIMIT 5", is_mysql)
                st.dataframe(audit_df, use_container_width=True)

    elif "sp_cancel_booking" in proc_mode:
        st.markdown("#### ❌ Execute `sp_cancel_booking`")
        cb_id = st.number_input("Booking ID to Cancel", min_value=801, max_value=900, value=801)
        if st.button("⚠️ Cancel Booking & Process Refund"):
            success, msg, logs = db_manager.execute_cancel_booking_transaction(conn, cb_id, is_mysql)
            if success:
                st.success(msg)
            else:
                st.error(msg)


# ==============================================================================
# TAB 5: DBMS SYLLABUS LAB (UNITS 1 - 6)
# ==============================================================================
with tab_syllabus:
    st.subheader("📚 Interactive DBMS Syllabus Laboratory")
    st.caption("Complete mapping to VIT Pune Second-Year B.Tech DBMS Curriculum (CS2227 / ML2302).")

    sub_unit = st.selectbox("Select Syllabus Unit to Explore:", [
        "Unit 1: Data Modeling, Relational Model & Codd's Rules",
        "Unit 2 & 3: Relational Algebra & Advanced SQL Suite",
        "Unit 4: Normalization (1NF to BCNF) & Parquet Storage Simulation",
        "Unit 5: Transactions, Conflict Serializability & Distributed Databases",
        "Unit 6: NoSQL, Big Data & Data Warehousing (OLAP Star Schema)"
    ])

    if "Unit 1" in sub_unit:
        st.markdown("### 🏛️ Unit 1: Data Modeling & Relational Integrity")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 3-Tier ANSI/SPARC Architecture")
            arch = syllabus_engine.Unit1DataModeling.get_three_tier_architecture()
            st.json(arch)
        with c2:
            st.markdown("#### Codd's 12 Rules Compliance")
            codds = syllabus_engine.Unit1DataModeling.get_codds_rules_evaluation()
            st.dataframe(pd.DataFrame(codds), use_container_width=True)

        st.markdown("#### Relational Integrity Constraints")
        constraints = syllabus_engine.Unit1DataModeling.get_integrity_constraints()
        st.dataframe(pd.DataFrame(constraints), use_container_width=True)

    elif "Unit 2" in sub_unit:
        st.markdown("### 🧮 Units 2 & 3: Relational Algebra & Advanced SQL Suite")
        st.markdown("#### Relational Algebra vs SQL Mappings")
        ra_data = syllabus_engine.Unit2RelationalAlgebra.get_relational_algebra_mappings()
        st.dataframe(pd.DataFrame(ra_data), use_container_width=True)

        st.markdown("#### Complex Joins & Subqueries Suite")
        complex_suite = syllabus_engine.Unit2RelationalAlgebra.get_complex_sql_suite()
        for item in complex_suite:
            with st.expander(f"🔹 {item['category']}: {item['title']}", expanded=True):
                st.code(item['sql'], language="sql")
                st.caption(f"**Explanation:** {item['notes']}")

    elif "Unit 4" in sub_unit:
        st.markdown("### 📐 Unit 4: Normalization, Parquet Storage & Recovery")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Normalization Breakdown (1NF ➔ BCNF)")
            norm = syllabus_engine.Unit4NormalizationAndStorage.get_normalization_breakdown()
            st.dataframe(pd.DataFrame(norm["stages"]), use_container_width=True)
            st.info(f"**Proof of Lossless Join:** {norm['lossless_decomposition_proof']}")
        with c2:
            st.markdown("#### Parquet Columnar Storage vs Row-Oriented Storage")
            st.caption("Simulating VIT Pune lecture slide: SELECT passenger_name, age FROM passenger WHERE age > 30;")
            sim_rows = st.select_slider("Number of Database Tuples", options=[10000, 50000, 100000, 500000], value=100000)
            parquet_sim = syllabus_engine.Unit4NormalizationAndStorage.simulate_parquet_vs_row_storage(sim_rows)
            st.json(parquet_sim)

    elif "Unit 5" in sub_unit:
        st.markdown("### 🔄 Unit 5: Transactions, Serializability & Distributed Systems")
        st.markdown("#### Conflict Serializability & Precedence Graph Analyzer")
        st.caption("Tests whether concurrent transaction schedule on Flight seats contains serializability cycles.")
        ser_result = syllabus_engine.Unit5TransactionsAndConcurrency.test_conflict_serializability()
        st.json(ser_result)

        st.markdown("#### Distributed Sharding & Hub Partitioning")
        shard_model = syllabus_engine.Unit5TransactionsAndConcurrency.get_distributed_sharding_model()
        st.json(shard_model)

    elif "Unit 6" in sub_unit:
        st.markdown("### 🌐 Unit 6: NoSQL, Big Data & Data Warehousing")
        st.markdown("#### Multi-Model NoSQL Representations")
        nosql_data = syllabus_engine.Unit6NoSQLAndDataWarehouse.get_nosql_multi_model_representations()
        st.json(nosql_data)

        st.markdown("#### Data Warehouse Star Schema & OLAP")
        dw_data = syllabus_engine.Unit6NoSQLAndDataWarehouse.get_data_warehouse_star_schema()
        st.json(dw_data)


# ==============================================================================
# TAB 6: CUSTOM SQL TERMINAL
# ==============================================================================
with tab_sql:
    st.subheader("💻 Custom Relational SQL Terminal")
    st.caption("Execute custom SELECT queries directly against the Airport database.")

    default_sample_sql = (
        "SELECT f.flight_no, a1.city AS origin, a2.city AS destination, f.fare\n"
        "FROM flight f\n"
        "JOIN airport a1 ON f.source_airport = a1.airport_id\n"
        "JOIN airport a2 ON f.destination_airport = a2.airport_id\n"
        "WHERE f.fare > 6000\n"
        "ORDER BY f.fare DESC;"
    )

    custom_sql = st.text_area("SQL Query Editor:", value=default_sample_sql, height=140)

    if st.button("⚡ Run Query", key="btn_run_sql"):
        q_strip = custom_sql.strip().lower()
        if not q_strip.startswith("select"):
            st.error("Only SELECT queries are permitted in this console for safety.")
        else:
            try:
                res_df, q_err = db_manager.execute_query(conn, custom_sql, is_mysql=is_mysql)
                if q_err:
                    st.error(f"SQL Execution Error: {q_err}")
                else:
                    st.success(f"Query returned {len(res_df)} rows.")
                    st.dataframe(res_df, use_container_width=True)
            except Exception as e:
                st.error(f"Execution Error: {e}")
