"""
Voice Query Engine for Airport Operations & Passenger Management System
Translates spoken natural language and text queries into:
1. Synthesized SQL queries (Equi-Joins, Subqueries, Filters)
2. Formatted Pandas DataFrame results
3. Conversational natural language text for display
4. Concise Voice Output string for Text-To-Speech (TTS) synthesis
"""

import re
import db_manager


def process_query(user_query, conn, is_mysql=False):
    """
    Parses natural language / voice input, generates and runs SQL,
    and returns:
    {
        "category": str,
        "sql": str,
        "dataframe": pd.DataFrame,
        "summary": str,
        "spoken_text": str,
        "status": "success" | "info" | "warning"
    }
    """
    q = user_query.strip()
    q_lower = q.lower()

    # 1. Greetings / Help
    if any(greet in q_lower for greet in ["hello", "hi", "hey", "help", "who are you", "what can you do"]):
        return {
            "category": "👋 Voice Assistant Help",
            "sql": "-- Conversational inquiry / system capability guide",
            "dataframe": None,
            "summary": (
                "Hello! I am your Voice-Enabled Airport Operations Assistant. "
                "You can speak queries to search flights, check passenger manifests, "
                "verify aircraft fleet status, track bookings, and inspect payments."
            ),
            "spoken_text": (
                "Hello! I am your Airport Operations Assistant. "
                "Ask me about flights from any city, passenger lists, aircraft fleet, or payment details."
            ),
            "status": "info"
        }

    # 2. Count / Summary queries
    if ("how many" in q_lower or "total" in q_lower or "count" in q_lower) and "passenger" in q_lower:
        sql = "SELECT COUNT(*) AS total_passengers FROM passenger;"
        df, err = db_manager.execute_query(conn, sql, is_mysql)
        total = int(df.iloc[0, 0]) if not df.empty else 0
        return {
            "category": "👥 Passenger Statistics",
            "sql": sql,
            "dataframe": df,
            "summary": f"There are currently **{total}** registered passengers in the Airport database.",
            "spoken_text": f"There are currently {total} registered passengers in the Airport database.",
            "status": "success"
        }

    if ("how many" in q_lower or "total" in q_lower or "count" in q_lower) and "flight" in q_lower:
        sql = "SELECT COUNT(*) AS total_flights FROM flight;"
        df, err = db_manager.execute_query(conn, sql, is_mysql)
        total = int(df.iloc[0, 0]) if not df.empty else 0
        return {
            "category": "✈️ Flight Operations Summary",
            "sql": sql,
            "dataframe": df,
            "summary": f"There are **{total}** scheduled commercial flights in the database.",
            "spoken_text": f"There are {total} scheduled commercial flights in the database.",
            "status": "success"
        }

    # 3. Flights from a specific city / origin
    m_from = re.search(r'(?:from|departing|leaving)\s+([a-zA-Z]+)', q_lower)
    if ("flight" in q_lower or "depart" in q_lower) and m_from:
        city = m_from.group(1).strip()
        sql = f"""
        SELECT 
            f.flight_no AS 'Flight No',
            a1.city AS 'Origin',
            a2.city AS 'Destination',
            f.departure_time AS 'Departure Time',
            f.arrival_time AS 'Arrival Time',
            f.fare AS 'Fare (INR)'
        FROM flight f
        JOIN airport a1 ON f.source_airport = a1.airport_id
        JOIN airport a2 ON f.destination_airport = a2.airport_id
        WHERE LOWER(a1.city) LIKE '%{city}%'
        ORDER BY f.departure_time;
        """
        df, err = db_manager.execute_query(conn, sql, is_mysql)
        if not df.empty:
            count = len(df)
            first_flight = df.iloc[0]['Flight No']
            first_dest = df.iloc[0]['Destination']
            fare = int(df.iloc[0]['Fare (INR)'])
            spoken = (
                f"Found {count} flights departing from {city.title()}. "
                f"The earliest departure is flight {first_flight} to {first_dest} with a fare of {fare} rupees."
            )
            return {
                "category": f"🛫 Departures from {city.title()}",
                "sql": sql.strip(),
                "dataframe": df,
                "summary": f"Found **{count}** flight(s) departing from **{city.title()}**.",
                "spoken_text": spoken,
                "status": "success"
            }
        else:
            return {
                "category": f"🛫 Departures from {city.title()}",
                "sql": sql.strip(),
                "dataframe": df,
                "summary": f"No flights found departing from **{city.title()}**.",
                "spoken_text": f"No flights were found departing from {city.title()}.",
                "status": "warning"
            }

    # 4. Flights to a specific city / destination
    m_to = re.search(r'(?:to|arriving at|going to|destined for)\s+([a-zA-Z]+)', q_lower)
    if ("flight" in q_lower or "arriv" in q_lower) and m_to:
        city = m_to.group(1).strip()
        sql = f"""
        SELECT 
            f.flight_no AS 'Flight No',
            a1.city AS 'Origin',
            a2.city AS 'Destination',
            f.departure_time AS 'Departure Time',
            f.arrival_time AS 'Arrival Time',
            f.fare AS 'Fare (INR)'
        FROM flight f
        JOIN airport a1 ON f.source_airport = a1.airport_id
        JOIN airport a2 ON f.destination_airport = a2.airport_id
        WHERE LOWER(a2.city) LIKE '%{city}%'
        ORDER BY f.arrival_time;
        """
        df, err = db_manager.execute_query(conn, sql, is_mysql)
        if not df.empty:
            count = len(df)
            first_flight = df.iloc[0]['Flight No']
            first_orig = df.iloc[0]['Origin']
            fare = int(df.iloc[0]['Fare (INR)'])
            spoken = (
                f"Found {count} flights arriving in {city.title()}. "
                f"The earliest is flight {first_flight} from {first_orig} with a fare of {fare} rupees."
            )
            return {
                "category": f"🛬 Arrivals at {city.title()}",
                "sql": sql.strip(),
                "dataframe": df,
                "summary": f"Found **{count}** flight(s) arriving at **{city.title()}**.",
                "spoken_text": spoken,
                "status": "success"
            }
        else:
            return {
                "category": f"🛬 Arrivals at {city.title()}",
                "sql": sql.strip(),
                "dataframe": df,
                "summary": f"No scheduled flights found arriving at **{city.title()}**.",
                "spoken_text": f"No scheduled flights were found arriving at {city.title()}.",
                "status": "warning"
            }

    # 5. Passengers on a specific flight (Manifest)
    m_flight_no = re.search(r'(?:flight|flt)\s*([a-zA-Z]*\d+)', q_lower)
    if "passenger" in q_lower and m_flight_no:
        f_val = m_flight_no.group(1).upper()
        sql = f"""
        SELECT 
            p.passenger_id AS 'Passenger ID',
            p.passenger_name AS 'Name',
            p.phone AS 'Phone',
            p.age AS 'Age',
            b.seat_no AS 'Seat',
            b.booking_status AS 'Status'
        FROM passenger p
        JOIN booking b ON p.passenger_id = b.passenger_id
        JOIN flight f ON b.flight_id = f.flight_id
        WHERE UPPER(f.flight_no) = '{f_val}' OR f.flight_id = '{f_val}'
        ORDER BY b.seat_no;
        """
        df, err = db_manager.execute_query(conn, sql, is_mysql)
        if not df.empty:
            count = len(df)
            p_names = ", ".join(df['Name'].head(3).tolist())
            spoken = f"Flight {f_val} has {count} passengers on the manifest, including {p_names}."
            return {
                "category": f"📋 Passenger Manifest: Flight {f_val}",
                "sql": sql.strip(),
                "dataframe": df,
                "summary": f"Manifest for flight **{f_val}** contains **{count}** confirmed passenger(s).",
                "spoken_text": spoken,
                "status": "success"
            }
        else:
            return {
                "category": f"📋 Passenger Manifest: Flight {f_val}",
                "sql": sql.strip(),
                "dataframe": df,
                "summary": f"No passengers found booked on flight **{f_val}**.",
                "spoken_text": f"No passengers were found on the manifest for flight {f_val}.",
                "status": "warning"
            }

    # 6. Specific flight lookup by code (e.g., AI101 or 301)
    if m_flight_no and not ("passenger" in q_lower or "booking" in q_lower):
        f_val = m_flight_no.group(1).upper()
        sql = f"""
        SELECT 
            f.flight_no AS 'Flight No',
            a1.city AS 'Origin',
            a2.city AS 'Destination',
            f.departure_time AS 'Departure',
            f.arrival_time AS 'Arrival',
            ac.model AS 'Aircraft',
            f.fare AS 'Fare (INR)'
        FROM flight f
        JOIN airport a1 ON f.source_airport = a1.airport_id
        JOIN airport a2 ON f.destination_airport = a2.airport_id
        LEFT JOIN aircraft ac ON f.aircraft_id = ac.aircraft_id
        WHERE UPPER(f.flight_no) = '{f_val}' OR f.flight_id = '{f_val}';
        """
        df, err = db_manager.execute_query(conn, sql, is_mysql)
        if not df.empty:
            f_row = df.iloc[0]
            spoken = (
                f"Flight {f_row['Flight No']} flies from {f_row['Origin']} to {f_row['Destination']}, "
                f"departing at {f_row['Departure'].split(' ')[1]}, fare is {int(f_row['Fare (INR)'])} rupees."
            )
            return {
                "category": f"✈️ Flight Status: {f_val}",
                "sql": sql.strip(),
                "dataframe": df,
                "summary": f"Details for flight **{f_val}** retrieved successfully.",
                "spoken_text": spoken,
                "status": "success"
            }

    # 7. Fare Filter (Cheaper than / under / budget)
    m_fare = re.search(r'(?:cheaper than|under|less than|below|budget)\s*(?:rs\.?|inr|₹)?\s*(\d+)', q_lower)
    if ("fare" in q_lower or "flight" in q_lower or "cheap" in q_lower) and m_fare:
        target_fare = float(m_fare.group(1))
        sql = f"""
        SELECT 
            f.flight_no AS 'Flight No',
            a1.city AS 'Origin',
            a2.city AS 'Destination',
            f.departure_time AS 'Departure Time',
            f.fare AS 'Fare (INR)'
        FROM flight f
        JOIN airport a1 ON f.source_airport = a1.airport_id
        JOIN airport a2 ON f.destination_airport = a2.airport_id
        WHERE f.fare <= {target_fare}
        ORDER BY f.fare ASC;
        """
        df, err = db_manager.execute_query(conn, sql, is_mysql)
        if not df.empty:
            count = len(df)
            min_fare = int(df.iloc[0]['Fare (INR)'])
            cheapest_flight = df.iloc[0]['Flight No']
            spoken = (
                f"Found {count} flights with fares under {int(target_fare)} rupees. "
                f"The most affordable is flight {cheapest_flight} at {min_fare} rupees."
            )
            return {
                "category": f"💰 Budget Flights (< ₹{int(target_fare)})",
                "sql": sql.strip(),
                "dataframe": df,
                "summary": f"Found **{count}** flight(s) with fares under **₹{int(target_fare)}**.",
                "spoken_text": spoken,
                "status": "success"
            }

    # 8. Available Aircraft Fleet
    if any(k in q_lower for k in ["aircraft", "fleet", "plane", "airplane"]):
        only_avail = "available" in q_lower or "active" in q_lower or "ready" in q_lower
        where_clause = "WHERE status = 'Available'" if only_avail else ""
        sql = f"""
        SELECT 
            aircraft_id AS 'Aircraft ID',
            model AS 'Aircraft Model',
            capacity AS 'Passenger Capacity',
            manufacturer AS 'Manufacturer',
            status AS 'Status'
        FROM aircraft
        {where_clause}
        ORDER BY capacity DESC;
        """
        df, err = db_manager.execute_query(conn, sql, is_mysql)
        count = len(df)
        spoken = f"Retrieved {count} aircraft records. Models include {df.iloc[0]['Aircraft Model']} with capacity of {df.iloc[0]['Passenger Capacity']} passengers."
        return {
            "category": "🛫 Aircraft Fleet Operations",
            "sql": sql.strip(),
            "dataframe": df,
            "summary": f"Displaying **{count}** aircraft in the fleet.",
            "spoken_text": spoken,
            "status": "success"
        }

    # 9. Payment queries
    if any(k in q_lower for k in ["payment", "paid", "upi", "card", "transaction"]):
        method = "UPI" if "upi" in q_lower else ("Card" if "card" in q_lower else None)
        where_clause = f"WHERE p.payment_method = '{method}'" if method else ""
        sql = f"""
        SELECT 
            p.payment_id AS 'Payment ID',
            p.booking_id AS 'Booking ID',
            p.amount AS 'Amount (INR)',
            p.payment_method AS 'Payment Method',
            p.payment_status AS 'Status',
            p.payment_date AS 'Date'
        FROM payment p
        {where_clause}
        ORDER BY p.payment_date DESC;
        """
        df, err = db_manager.execute_query(conn, sql, is_mysql)
        count = len(df)
        total_amount = int(df['Amount (INR)'].sum()) if not df.empty else 0
        spoken = f"Found {count} payment records with a total value of {total_amount} rupees."
        return {
            "category": f"💳 Payment Records {f'({method})' if method else ''}",
            "sql": sql.strip(),
            "dataframe": df,
            "summary": f"Found **{count}** payment records totaling **₹{total_amount:,}**.",
            "spoken_text": spoken,
            "status": "success"
        }

    # 10. Passenger search by name
    m_name = re.search(r'(?:find|search|where is|passenger|booking for)\s+([a-zA-Z]+)', q_lower)
    if "passenger" in q_lower and m_name:
        candidate_name = m_name.group(1).strip()
        if candidate_name not in ["the", "all", "on", "in", "for", "from", "to", "flight"]:
            sql = f"""
            SELECT 
                p.passenger_id AS 'ID',
                p.passenger_name AS 'Name',
                p.phone AS 'Phone',
                p.age AS 'Age',
                f.flight_no AS 'Flight',
                b.seat_no AS 'Seat',
                b.booking_status AS 'Booking Status'
            FROM passenger p
            LEFT JOIN booking b ON p.passenger_id = b.passenger_id
            LEFT JOIN flight f ON b.flight_id = f.flight_id
            WHERE LOWER(p.passenger_name) LIKE '%{candidate_name}%';
            """
            df, err = db_manager.execute_query(conn, sql, is_mysql)
            if not df.empty:
                count = len(df)
                p_name = df.iloc[0]['Name']
                seat = df.iloc[0]['Seat']
                flt = df.iloc[0]['Flight']
                spoken = f"Found passenger {p_name} assigned to flight {flt} in seat {seat}."
                return {
                    "category": f"👤 Passenger Profile: {candidate_name.title()}",
                    "sql": sql.strip(),
                    "dataframe": df,
                    "summary": f"Found **{count}** record(s) matching **{candidate_name.title()}**.",
                    "spoken_text": spoken,
                    "status": "success"
                }

    # 11. Bookings lookup
    if any(k in q_lower for k in ["booking", "reservation", "seats"]):
        sql = """
        SELECT 
            b.booking_id AS 'Booking ID',
            p.passenger_name AS 'Passenger',
            f.flight_no AS 'Flight',
            b.booking_date AS 'Date',
            b.seat_no AS 'Seat',
            b.booking_status AS 'Status'
        FROM booking b
        JOIN passenger p ON b.passenger_id = p.passenger_id
        JOIN flight f ON b.flight_id = f.flight_id
        ORDER BY b.booking_id ASC;
        """
        df, err = db_manager.execute_query(conn, sql, is_mysql)
        count = len(df)
        spoken = f"Retrieved {count} active flight reservations from the Booking table."
        return {
            "category": "🎟️ Confirmed Reservations",
            "sql": sql.strip(),
            "dataframe": df,
            "summary": f"Found **{count}** booking reservation(s).",
            "spoken_text": spoken,
            "status": "success"
        }

    # 12. Airport hubs
    if any(k in q_lower for k in ["airport", "hub", "terminal"]):
        sql = """
        SELECT 
            airport_id AS 'Airport ID',
            airport_name AS 'Airport Name',
            city AS 'City',
            country AS 'Country',
            airport_code AS 'IATA Code'
        FROM airport
        ORDER BY city ASC;
        """
        df, err = db_manager.execute_query(conn, sql, is_mysql)
        count = len(df)
        spoken = f"The airport network connects {count} major hubs across India."
        return {
            "category": "🌐 Airport Network Hubs",
            "sql": sql.strip(),
            "dataframe": df,
            "summary": f"Registered **{count}** airport hubs.",
            "spoken_text": spoken,
            "status": "success"
        }

    # 13. Default: Show active flights
    sql = """
    SELECT 
        f.flight_no AS 'Flight No',
        a1.city AS 'Origin',
        a2.city AS 'Destination',
        f.departure_time AS 'Departure',
        f.arrival_time AS 'Arrival',
        f.fare AS 'Fare (INR)'
    FROM flight f
    JOIN airport a1 ON f.source_airport = a1.airport_id
    JOIN airport a2 ON f.destination_airport = a2.airport_id
    ORDER BY f.departure_time ASC;
    """
    df, err = db_manager.execute_query(conn, sql, is_mysql)
    count = len(df)
    spoken = f"Displaying {count} active commercial flights currently scheduled in the Airport system."
    return {
        "category": "✈️ Flight Schedules Overview",
        "sql": sql.strip(),
        "dataframe": df,
        "summary": f"Showing **{count}** scheduled flight operations.",
        "spoken_text": spoken,
        "status": "info"
    }
