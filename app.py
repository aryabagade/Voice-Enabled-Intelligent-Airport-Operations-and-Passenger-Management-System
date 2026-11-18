import os
import io
import time
import json
import re
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

# Custom Aviation Cyber-Theme CSS + Mobile Voice UI + Lyrics Animation
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
        padding: 20px 26px;
        margin-bottom: 22px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    }
    .hero-title {
        font-size: 1.85rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #FFFFFF;
        margin-bottom: 4px;
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

    /* ========================================================================= */
    /* MOBILE PHONE MOCKUP VOICE SEARCH CARD (Inspired by User Screenshot)       */
    /* ========================================================================= */
    .phone-mockup {
        background: linear-gradient(180deg, #070e24 0%, #0d214d 45%, #081534 100%);
        border: 4px solid #1e293b;
        border-radius: 36px;
        padding: 20px 18px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.6), inset 0 1px 3px rgba(255, 255, 255, 0.12);
        position: relative;
        overflow: hidden;
        margin: 0 auto 20px auto;
        text-align: center;
    }

    .phone-top-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-family: monospace;
        font-size: 0.76rem;
        color: #94a3b8;
        margin-bottom: 12px;
        padding: 0 8px;
    }

    .voice-search-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: 0.02em;
        margin-bottom: 14px;
    }

    /* Floating Colorful Particles */
    .mic-stage-box {
        position: relative;
        width: 220px;
        height: 200px;
        margin: 0 auto;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .particle {
        position: absolute;
        border-radius: 50%;
        filter: drop-shadow(0 0 6px currentColor);
    }
    .p-pink-1   { width: 14px; height: 14px; background: #ff2a6d; color: #ff2a6d; top: 22px; left: 18px; }
    .p-yellow-1 { width: 12px; height: 12px; background: #fbbf24; color: #fbbf24; top: 14px; left: 75px; }
    .p-cyan-1   { width: 15px; height: 15px; background: #22d3ee; color: #22d3ee; top: 26px; right: 24px; }
    .p-yellow-2 { width: 10px; height: 10px; background: #f59e0b; color: #f59e0b; top: 72px; right: 12px; }
    .p-cyan-2   { width: 11px; height: 11px; background: #38bdf8; color: #38bdf8; bottom: 35px; left: 16px; }
    .p-yellow-3 { width: 16px; height: 16px; background: #fbbf24; color: #fbbf24; bottom: 16px; left: 40px; }
    .p-pink-2   { width: 11px; height: 11px; background: #f43f5e; color: #f43f5e; bottom: 30px; right: 20px; }

    /* Concentric Pulsing Coral-Pink Microphone Orb */
    @keyframes pulse-ring-glow {
        0% { transform: scale(0.96); box-shadow: 0 0 0 0 rgba(255, 42, 109, 0.7); }
        70% { transform: scale(1.04); box-shadow: 0 0 0 22px rgba(255, 42, 109, 0); }
        100% { transform: scale(0.96); box-shadow: 0 0 0 0 rgba(255, 42, 109, 0); }
    }

    .mic-orb {
        width: 130px;
        height: 130px;
        border-radius: 50%;
        background: radial-gradient(circle at 35% 35%, #ff4b72 0%, #ff1a4a 65%, #c8002d 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 10px 30px rgba(255, 26, 74, 0.5), inset 0 -4px 8px rgba(0,0,0,0.3);
        animation: pulse-ring-glow 2.4s infinite cubic-bezier(0.45, 0, 0.55, 1);
        cursor: pointer;
        transition: transform 0.2s;
        border: 2px solid rgba(255, 255, 255, 0.2);
    }
    .mic-orb:hover {
        transform: scale(1.08);
    }
    .mic-orb svg {
        width: 58px;
        height: 58px;
        fill: none;
        stroke: #ffffff;
        stroke-width: 2;
        stroke-linecap: round;
        stroke-linejoin: round;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.4));
    }

    .tap-speak-label {
        font-size: 0.9rem;
        color: #e2e8f0;
        font-weight: 600;
        margin: 12px 0 14px 0;
        letter-spacing: 0.03em;
    }

    .btn-search-pill {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: #ffffff;
        border: none;
        padding: 9px 24px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 0.92rem;
        box-shadow: 0 4px 16px rgba(245, 158, 11, 0.4);
        cursor: pointer;
        display: inline-block;
        width: 80%;
    }

    /* ========================================================================= */
    /* "WRITED OUTPUT LIKE LYRICS" SYNCHRONIZED KARAOKE DISPLAY                  */
    /* ========================================================================= */
    .lyrics-card {
        background: linear-gradient(135deg, rgba(13, 23, 50, 0.95) 0%, rgba(18, 35, 75, 0.85) 100%);
        border: 1px solid rgba(56, 189, 248, 0.35);
        border-left: 6px solid #38bdf8;
        border-radius: 18px;
        padding: 22px 26px;
        box-shadow: 0 16px 40px rgba(0, 0, 0, 0.5);
        margin-bottom: 20px;
        position: relative;
    }

    .lyrics-top-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 14px;
        padding-bottom: 10px;
        border-bottom: 1px solid rgba(56, 189, 248, 0.2);
    }

    .lyrics-tag {
        font-size: 0.78rem;
        font-weight: 800;
        color: #38bdf8;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        display: inline-flex;
        align-items: center;
        gap: 8px;
    }

    /* Equalizer Soundwave Animation */
    @keyframes eq-bounce {
        0%   { height: 4px; }
        50%  { height: 20px; }
        100% { height: 6px; }
    }
    .equalizer-box {
        display: inline-flex;
        align-items: flex-end;
        gap: 3px;
        height: 22px;
    }
    .eq-bar {
        width: 3.5px;
        height: 14px;
        background: #38bdf8;
        border-radius: 2px;
        animation: eq-bounce 0.8s ease-in-out infinite;
    }
    .eq-bar:nth-child(2) { animation-delay: 0.2s; background: #f59e0b; }
    .eq-bar:nth-child(3) { animation-delay: 0.4s; background: #ff2a6d; }
    .eq-bar:nth-child(4) { animation-delay: 0.15s; background: #10b981; }
    .eq-bar:nth-child(5) { animation-delay: 0.35s; background: #a855f7; }

    /* Lyrics Typography Lines */
    .lyrics-body {
        margin: 10px 0;
    }
    .lyrics-line-active {
        font-size: 1.28rem;
        font-weight: 700;
        color: #ffffff;
        line-height: 1.55;
        text-shadow: 0 0 16px rgba(56, 189, 248, 0.6);
        margin-bottom: 10px;
        letter-spacing: -0.01em;
    }
    .lyrics-line-sub {
        font-size: 1.08rem;
        font-weight: 600;
        color: #38bdf8;
        line-height: 1.5;
        margin-bottom: 8px;
    }
    .lyrics-line-muted {
        font-size: 0.95rem;
        font-weight: 400;
        color: #94a3b8;
        line-height: 1.45;
    }

    .badge-on-time {
        background: rgba(16, 185, 129, 0.2);
        color: #10B981;
        border: 1px solid #10B981;
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
    clean_text = text.replace('"', '\\"').replace("'", "\\'").replace("\n", " ").replace("\r", " ")
    
    js_code = f"""
    <div style="display: flex; align-items: center; gap: 12px; margin-top: 8px;">
        <button id="tts-btn" onclick="speakNow()" style="
            background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
            color: #ffffff;
            border: 1px solid #38bdf8;
            border-radius: 8px;
            padding: 8px 18px;
            cursor: pointer;
            font-size: 13px;
            font-weight: 700;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 4px 14px rgba(2, 132, 199, 0.35);
            transition: all 0.2s;
        ">
            🔊 Replay Spoken Voice
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
                if (statusSpan) statusSpan.innerText = "🎙️ Speaking aloud...";
                msg.onend = function() {{
                    if (statusSpan) statusSpan.innerText = "✓ Voice speech complete";
                }};
                
                window.speechSynthesis.speak(msg);
            }}
        }}
        {'speakNow();' if auto_play else ''}
    </script>
    """
    components.html(js_code, height=54)

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


# Helper to format text into lyrics-style lines
def split_into_lyrics(text: str) -> list[str]:
    raw_sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    lines = [s.strip() for s in raw_sentences if s.strip()]
    if not lines:
        lines = [text.strip()]
    return lines


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
    st.markdown("#### 🔊 Audio & Voice Settings")
    auto_speak = st.checkbox("Auto-play voice response", value=True)
    voice_speed = st.slider("Speech Rate (Speed)", min_value=0.7, max_value=1.4, value=1.0, step=0.1)

    st.divider()

    # Web Portal Link
    st.markdown("#### 🌐 Modern Web Portal")
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

st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)

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
        Speak queries to search flights, check passenger manifests, track baggage, verify fleet status, and review ACID transactions.
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
    "🎙️ Voice Search & Lyrics Output",
    "🛫 Live Flight Board (FIDS)",
    "🗄️ Database Tables Explorer",
    "⚡ Stored Procedures & Triggers",
    "📚 DBMS Syllabus Lab (Units 1-6)",
    "💻 Custom SQL Terminal"
])


# ==============================================================================
# TAB 1: VOICE SEARCH (PHONE UI) + LYRICS & DATA OUTPUT
# ==============================================================================
with tab_voice:
    # 2-Column Layout: Left = Mobile Voice Search Phone UI | Right = Lyrics & Data Output
    col_phone, col_output = st.columns([1.15, 1.85], gap="large")

    with col_phone:
        # Render the mobile phone mockup matching the user's uploaded image
        st.markdown("""
        <div class="phone-mockup">
            <div class="phone-top-bar">
                <span>12:00</span>
                <span>📶 5G &nbsp; 🔋 100%</span>
            </div>
            <div class="voice-search-title">Voice search</div>
            
            <!-- Colorful floating particles + Pulsing Mic Orb -->
            <div class="mic-stage-box">
                <div class="particle p-pink-1"></div>
                <div class="particle p-yellow-1"></div>
                <div class="particle p-cyan-1"></div>
                <div class="particle p-yellow-2"></div>
                <div class="particle p-cyan-2"></div>
                <div class="particle p-yellow-3"></div>
                <div class="particle p-pink-2"></div>
                
                <div class="mic-orb">
                    <svg viewBox="0 0 24 24">
                        <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
                        <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
                        <line x1="12" y1="19" x2="12" y2="23"></line>
                        <line x1="8" y1="23" x2="16" y2="23"></line>
                    </svg>
                </div>
            </div>

            <div class="tap-speak-label">Tap to speak or select an option below</div>
        </div>
        """, unsafe_allow_html=True)

        # Embedded Voice Input controls directly in the card flow
        st.markdown("<div style='text-align: center; margin-bottom: 8px;'>", unsafe_allow_html=True)
        spoken_audio = speech_to_text(
            language="en",
            start_prompt="🎙️ Tap to Speak (Start Recording)",
            stop_prompt="⏹️ Stop Recording",
            just_once=True,
            use_container_width=True,
            key="mic_audio_input_phone"
        )
        st.markdown("</div>", unsafe_allow_html=True)

        # Manual text query fallback
        typed_text = st.text_input(
            label="Type query (alternative):",
            placeholder="e.g. Flights from Mumbai, Show baggage status...",
            key="phone_typed_text"
        )

        # Quick Option Pills ("with some options")
        st.markdown("<div style='font-size: 0.78rem; font-weight: 700; color: #94A3B8; text-transform: uppercase; margin: 10px 0 6px 0;'>💡 Quick Category Options:</div>", unsafe_allow_html=True)
        opt_c1, opt_c2 = st.columns(2)
        with opt_c1:
            if st.button("🛫 Flights from Mumbai", use_container_width=True, key="opt_1"):
                st.session_state.trigger_query = "Show flights from Mumbai"
            if st.button("🧳 Baggage Tracking", use_container_width=True, key="opt_2"):
                st.session_state.trigger_query = "Show baggage status"
            if st.button("✈️ Available Aircraft", use_container_width=True, key="opt_3"):
                st.session_state.trigger_query = "Show available aircraft"
        with opt_c2:
            if st.button("🛬 Flights to Delhi", use_container_width=True, key="opt_4"):
                st.session_state.trigger_query = "Flights to Delhi"
            if st.button("💰 Total Revenue", use_container_width=True, key="opt_5"):
                st.session_state.trigger_query = "Show total revenue"
            if st.button("👥 Passenger Manifest", use_container_width=True, key="opt_6"):
                st.session_state.trigger_query = "Passengers on flight 301"

    with col_output:
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

        if active_query:
            st.session_state.last_query = active_query
            start_time = time.time()
            
            # Execute voice query engine
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

            # Format spoken text as musical lyrics lines
            lyrics_lines = split_into_lyrics(result["spoken_text"])
            
            lyrics_html_parts = []
            for idx, line in enumerate(lyrics_lines):
                if idx == 0:
                    lyrics_html_parts.append(f'<div class="lyrics-line-active">"{line}"</div>')
                elif idx == 1:
                    lyrics_html_parts.append(f'<div class="lyrics-line-sub">"{line}"</div>')
                else:
                    lyrics_html_parts.append(f'<div class="lyrics-line-muted">"{line}"</div>')

            lyrics_html_content = "".join(lyrics_html_parts)

            # ==================================================================
            # 1. LYRICS-STYLE SPOKEN RESPONSE DISPLAY
            # ==================================================================
            st.markdown(f"""
            <div class="lyrics-card">
                <div class="lyrics-top-bar">
                    <div class="lyrics-tag">
                        <div class="equalizer-box">
                            <span class="eq-bar"></span>
                            <span class="eq-bar"></span>
                            <span class="eq-bar"></span>
                            <span class="eq-bar"></span>
                            <span class="eq-bar"></span>
                        </div>
                        <span>🎵 LIVE VOICE TRANSCRIPTION • LYRICS MODE</span>
                    </div>
                    <span style="font-size: 0.76rem; color: #10B981; font-weight: 700; font-family: monospace;">
                        ⚡ Executed in {exec_ms} ms
                    </span>
                </div>
                
                <div style="font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; color: #F59E0B; font-weight: 700; margin-bottom: 6px;">
                    🎙️ Recognized Input: "{active_query}"
                </div>

                <div class="lyrics-body">
                    {lyrics_html_content}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Browser Text-to-Speech Output (Web Speech API)
            render_voice_output(
                text=result["spoken_text"],
                auto_play=auto_speak,
                speech_rate=voice_speed
            )

            # ==================================================================
            # 2. STRUCTURED DATA RESULTS
            # ==================================================================
            st.markdown(f"#### 📊 Structured Data Output (`{result['category']}`)")
            
            if result["dataframe"] is not None and not result["dataframe"].empty:
                st.caption(f"Found **{len(result['dataframe'])}** relational records matching query criteria.")
                st.dataframe(result["dataframe"], use_container_width=True)

                # CSV Download Button
                csv_data = result["dataframe"].to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Data Records as CSV",
                    data=csv_data,
                    file_name="airport_records.csv",
                    mime="text/csv"
                )
            elif result["dataframe"] is not None and result["dataframe"].empty:
                st.warning("Zero records found matching your query criteria.")

            # Synthesized 3NF SQL Inspector
            with st.expander("🛠️ View Synthesized Relational SQL Statement", expanded=False):
                st.code(result["sql"], language="sql")
                st.caption("Formulated using normalized 3NF relational schema joins and constraints.")


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
