import os
import io
import time
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from streamlit_mic_recorder import speech_to_text

import db_manager
import voice_query_engine

# ==============================================================================
# 1. PAGE CONFIGURATION & THEME
# ==============================================================================
st.set_page_config(
    page_title="Voice-Enabled Airport Operations & Passenger Management",
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

    /* Live FIDS Board */
    .fids-header {
        background: #0B132B;
        color: #F59E0B;
        font-family: monospace;
        padding: 10px 14px;
        border-radius: 8px 8px 0 0;
        border: 1px solid #334155;
        font-size: 0.85rem;
        font-weight: 700;
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
    # Sanitize text for JavaScript
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
                msg.onstart = function() {{
                    if (statusSpan) statusSpan.innerText = "🎙️ Speaking...";
                }};
                msg.onend = function() {{
                    if (statusSpan) statusSpan.innerText = "✓ Finished speaking";
                }};
                msg.onerror = function() {{
                    if (statusSpan) statusSpan.innerText = "Voice playback ready";
                }};
                
                window.speechSynthesis.speak(msg);
            }} else {{
                alert("Speech synthesis is not supported in this browser.");
            }}
        }}

        // Auto-play if enabled
        {'speakNow();' if auto_play else ''}
    </script>
    """
    components.html(js_code, height=52)

    # Optional server-side gTTS audio player
    try:
        from gtts import gTTS
        fp = io.BytesIO()
        tts = gTTS(text=text, lang="en", slow=False)
        tts.write_to_fp(fp)
        fp.seek(0)
        st.audio(fp.read(), format="audio/mp3", start_time=0)
    except Exception:
        # Offline or gTTS connection blocked - Web Speech API will handle the speech seamlessly
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
            if st.button("🔄 Test & Reconnect"):
                st.rerun()

    # Voice Output Settings
    st.divider()
    st.markdown("#### 🎙️ Voice Output Settings")
    auto_speak = st.checkbox("Auto-play spoken answers", value=True)
    voice_speed = st.slider("Speech Rate / Speed", min_value=0.8, max_value=1.4, value=1.0, step=0.1)

    # Establish connection
    conn, is_mysql, conn_msg = db_manager.get_db_connection(mysql_cfg, force_sqlite=force_sqlite)
    
    st.divider()
    if is_mysql:
        st.success("🟢 **MySQL Active** (Live Server)")
        st.caption(f"Host: `{mysql_cfg.get('host', 'localhost')}` | DB: `{mysql_cfg.get('database', 'AirportDB')}`")
    else:
        st.info("🟡 **AirportDB Standalone Mode**")
        st.caption("Loaded from `AirportDB.sql` into local database.")
    
    # Quick Table Counts
    st.divider()
    st.markdown("#### 📊 Core Entities Overview")
    tables_list = ["airport", "aircraft", "flight", "passenger", "booking", "payment"]
    cols_s = st.columns(2)
    for i, tbl in enumerate(tables_list):
        cnt = db_manager.get_table_row_count(conn, tbl, is_mysql)
        col = cols_s[i % 2]
        col.metric(tbl.title(), cnt)

    st.divider()
    st.markdown(
        "<div style='font-size: 0.75rem; color: #64748B;'>"
        "Voice-Enabled Airport Operations & Passenger Management System<br>"
        "Relational DBMS Project • Built with Streamlit"
        "</div>",
        unsafe_allow_html=True
    )


# ==============================================================================
# 4. MAIN WORKSPACE & HEADER
# ==============================================================================
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">🎙️ Voice-Enabled <span>Airport Operations</span> & Passenger Assistant</div>
    <div class="hero-subtitle">
        Speak questions to query flights, passenger manifests, aircraft fleet, seat bookings, and revenue records in real-time.
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
tab_voice, tab_fids, tab_tables, tab_sql = st.tabs([
    "🎙️ Voice Assistant & Queries",
    "🛫 Live Flight Board (FIDS)",
    "🗄️ Database Tables Explorer",
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
            placeholder="e.g. 'Show all flights from Mumbai', 'Passengers on flight 301'...",
            label_visibility="collapsed",
            key="text_query_input"
        )

    # Quick Suggestion Chips (1-Click Query Triggers)
    st.markdown("<div style='font-size: 0.8rem; font-weight: 700; color: #94A3B8; margin-top: 10px;'>💡 QUICK VOICE QUERY SUGGESTIONS:</div>", unsafe_allow_html=True)
    chip_cols = st.columns(6)
    
    prompts = [
        ("🛫 Flights from Mumbai", "Show flights from Mumbai"),
        ("🛬 Flights to Delhi", "Flights to Delhi"),
        ("📋 Manifest (Flight 301)", "Passengers on flight 301"),
        ("✈️ Available Aircraft", "Show available aircraft"),
        ("💰 Flights under ₹6000", "Flights cheaper than 6000"),
        ("💳 Payments via UPI", "Show payments made with UPI")
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

    # Default initial query if none submitted yet
    if not active_query and not st.session_state.chat_history:
        active_query = st.session_state.last_query

    # Process and Render Query
    if active_query:
        st.session_state.last_query = active_query
        start_time = time.time()
        
        # Call Query Engine
        result = voice_query_engine.process_query(active_query, conn, is_mysql=is_mysql)
        exec_ms = round((time.time() - start_time) * 1000, 1)

        # Store in history
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

        # Render speech in browser
        render_voice_output(
            text=result["spoken_text"],
            auto_play=auto_speak,
            speech_rate=voice_speed
        )

        # 2. Results Data Table
        if result["dataframe"] is not None and not result["dataframe"].empty:
            st.markdown(f"**Results ({len(result['dataframe'])} records found):**")
            st.dataframe(result["dataframe"], use_container_width=True)
            
            # Export CSV Button
            csv_data = result["dataframe"].to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Results as CSV",
                data=csv_data,
                file_name=f"airport_query_results.csv",
                mime="text/csv"
            )
        elif result["dataframe"] is not None and result["dataframe"].empty:
            st.warning("Zero records found matching your query criteria.")

        # 3. Synthesized SQL Query Inspector
        with st.expander("🛠️ View Synthesized Relational SQL Query", expanded=False):
            st.code(result["sql"], language="sql")
            st.caption("Formulated using 3NF relational schema joins and constraints.")

    # Interaction History Expander
    if len(st.session_state.chat_history) > 1:
        with st.expander("🕒 Recent Voice Interactions History", expanded=False):
            for h in st.session_state.chat_history[1:]:
                st.markdown(f"**[{h['time']}] {h['category']}** — *\"{h['query']}\"*")
                st.caption(f"Spoken: {h['spoken']}")
                st.markdown("---")


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
        # Filter by city search
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
# TAB 4: CUSTOM SQL TERMINAL
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
        # Safe check
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
