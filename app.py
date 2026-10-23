
import streamlit as st
import mysql.connector
import pandas as pd
from streamlit_mic_recorder import speech_to_text

st.set_page_config(
    page_title="Intelligent Airport Operations",
    page_icon="✈️",
    layout="wide"
)

st.title(" Voice-Enabled Intelligent Airport Operations")
st.caption("Airport database dashboard and passenger assistance")

# Update these values to match your MySQL setup.
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "1234",
    "database": "AirportDB"
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def get_tables(connection):
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES")
    tables = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return tables


def get_columns(connection, table):
    cursor = connection.cursor()
    cursor.execute(f"DESCRIBE `{table}`")
    columns = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return columns


def get_table_data(connection, table, limit=100):
    # Table names come from SHOW TABLES, not from user input.
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM `{table}` LIMIT {int(limit)}")
    rows = cursor.fetchall()
    columns = [item[0] for item in cursor.description]
    cursor.close()
    return pd.DataFrame(rows, columns=columns)


try:
    connection = get_connection()
    tables = get_tables(connection)

    st.success("Connected to MySQL database: AirportDB")

    # Dashboard summary
    st.subheader("Airport Database Overview")
    col1, col2 = st.columns(2)
    col1.metric("Database tables", len(tables))
    col2.metric("Database", "AirportDB")

    if not tables:
        st.warning("No tables found in AirportDB.")

    # Browse database tables
    st.subheader("Explore Airport Records")

    if tables:
        selected_table = st.selectbox("Select a table", tables)
        data = get_table_data(connection, selected_table)

        st.write(f"Showing up to 100 records from **{selected_table}**")
        st.dataframe(data, use_container_width=True)

        with st.expander("View table columns"):
            st.write(get_columns(connection, selected_table))

    # Passenger assistant
    st.divider()
    st.subheader("🎙️ Passenger Voice Assistant")
    st.write(
        "Try asking: 'Show flights', 'Show passengers', "
        "or 'Show bookings'."
    )

    spoken_question = speech_to_text(
        language="en",
        start_prompt="Start speaking",
        stop_prompt="Stop recording",
        key="passenger_voice"
    )

    typed_question = st.text_input(
        "Or type your question here",
        placeholder="For example: Show all flights"
    )

    question = typed_question.strip() or (
        spoken_question.strip() if spoken_question else ""
    )

    if question:
        st.write("**Your question:**", question)
        q = question.lower()

        # Basic table selection using actual database table names.
        matched_table = None
        for table in tables:
            name = table.lower()
            if name in q or name.rstrip("s") in q:
                matched_table = table
                break

        # Common passenger wording mapped to existing tables.
        if matched_table is None:
            aliases = {
                "flight": ["flight", "flights", "departure", "arrival"],
                "passenger": ["passenger", "passengers", "traveller",
                              "travelers", "travellers"],
                "booking": ["booking", "bookings", "reservation",
                            "reservations"],
                "airport": ["airport", "airports", "terminal"],
                "aircraft": ["aircraft", "plane", "planes", "airplane"],
                "payment": ["payment", "payments", "fare", "refund"]
            }

            for table in tables:
                for keyword in aliases.get(table.lower(), []):
                    if keyword in q:
                        matched_table = table
                        break
                if matched_table:
                    break

        if any(word in q for word in ["hello", "hi", "help"]):
            answer = (
                "Hello! I can help you explore airport records. "
                "Ask me about flights, passengers, bookings, airports "
                "or payments."
            )
            st.info(answer)
            st.caption("Voice playback can be added in the next stage.")

        elif matched_table:
            result = get_table_data(connection, matched_table)
            st.success(f"Here are the records for {matched_table}.")
            st.dataframe(result, use_container_width=True)

            st.write(
                f"I found {len(result)} record(s) in the displayed "
                f"results for {matched_table}."
            )

        else:
            st.info(
                "I couldn't identify the requested information yet. "
                "Try asking about flights, passengers, bookings, "
                "airports, aircraft or payments."
            )

    connection.close()

except mysql.connector.Error as error:
    st.error(f"MySQL connection or query error: {error}")
    st.info(
        "Check your MySQL password, database name, server status "
        "and table permissions."
    )

except Exception as error:
    st.error(f"Application error: {error}")
    st.info(
        "Check the installed packages and microphone permissions."
    )
