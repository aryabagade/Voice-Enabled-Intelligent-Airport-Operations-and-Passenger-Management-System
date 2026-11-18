"""
Voice Query Engine for Airport Operations & Passenger Management System
Translates spoken natural language and text queries into:
1. Synthesized SQL queries (Equi-Joins, Subqueries, Filters, Aggregations)
2. Formatted Pandas DataFrame results
3. Conversational natural language text for display
4. Concise Voice Output string for Text-To-Speech (TTS) synthesis

Supports Syllabus Scenarios:
- Joins & Aggregations (Flight schedules, manifests, revenue)
- Baggage tracking & status (Unit 1 EER)
- Audit trail queries (Unit 6 Triggers)
- Conceptual DBMS viva Q&A answers spoken directly
"""

import re
import db_manager


def process_query(user_query, conn, is_mysql=False):
    """
    Parses natural language / voice input, generates and runs SQL,
    and returns a structured dictionary for Streamlit & Web portals.
    """
    q = user_query.strip()
    q_lower = q.lower()

    # 1. Greetings & Help
    if any(greet in q_lower for greet in ["hello", "hi", "hey", "help", "who are you", "what can you do"]):
        return {
            "category": "👋 Voice Assistant Help",
            "sql": "-- Conversational inquiry / system capability guide",
            "dataframe": None,
            "summary": (
                "Hello! I am your Voice-Enabled Airport Operations Assistant. "
                "You can speak queries to search flights, check passenger manifests, "
                "track baggage, check aircraft fleet status, and review revenue."
            ),
            "spoken_text": (
                "Hello! I am your Airport Operations Assistant. "
                "Ask me about flights from any city, passenger manifests, baggage status, or revenue."
            ),
            "status": "info"
        }

    # 2. Baggage Tracking Queries
    if "baggage" in q_lower or "luggage" in q_lower or "bags" in q_lower:
        # Check if booking id mentioned
        m_bid = re.search(r'(?:booking|ticket)\s*(?:#|id|number)?\s*(\d+)', q_lower)
        m_name = re.search(r'(?:for|passenger)\s+([a-zA-Z]+)', q_lower)

        if m_bid:
            bid = int(m_bid.group(1))
            sql = f"""
            SELECT 
                bg.baggage_id AS 'Bag Tag',
                bg.booking_id AS 'Booking ID',
                p.passenger_name AS 'Passenger',
                f.flight_no AS 'Flight',
                bg.baggage_weight AS 'Weight (kg)',
                bg.baggage_type AS 'Type',
                bg.baggage_status AS 'Status'
            FROM baggage bg
            JOIN booking b ON bg.booking_id = b.booking_id
            JOIN passenger p ON b.passenger_id = p.passenger_id
            JOIN flight f ON b.flight_id = f.flight_id
            WHERE bg.booking_id = {bid};
            """
            df, err = db_manager.execute_query(conn, sql, is_mysql)
            if not df.empty:
                status = df.iloc[0]['Status']
                pname = df.iloc[0]['Passenger']
                weight = df.iloc[0]['Weight (kg)']
                spoken = f"Baggage for booking {bid} belonging to {pname} weighs {weight} kilograms and is currently {status}."
                return {
                    "category": "🧳 Baggage Tracking",
                    "sql": sql,
                    "dataframe": df,
                    "summary": f"Found baggage record for Booking #{bid}.",
                    "spoken_text": spoken,
                    "status": "success"
                }

        # General baggage query
        sql = """
        SELECT 
            bg.baggage_id AS 'Bag Tag',
            bg.booking_id AS 'Booking ID',
            p.passenger_name AS 'Passenger',
            f.flight_no AS 'Flight',
            bg.baggage_weight AS 'Weight (kg)',
            bg.baggage_type AS 'Type',
            bg.baggage_status AS 'Status'
        FROM baggage bg
        JOIN booking b ON bg.booking_id = b.booking_id
        JOIN passenger p ON b.passenger_id = p.passenger_id
        JOIN flight f ON b.flight_id = f.flight_id
        LIMIT 25;
        """
        df, err = db_manager.execute_query(conn, sql, is_mysql)
        return {
            "category": "🧳 Baggage Manifest",
            "sql": sql,
            "dataframe": df,
            "summary": f"Retrieved {len(df)} registered baggage items from the database.",
            "spoken_text": f"Displaying baggage manifest with {len(df)} checked luggage items across scheduled flights.",
            "status": "success"
        }

    # 3. Revenue & Financial Summary Queries
    if "revenue" in q_lower or "earning" in q_lower or "sales" in q_lower or "collection" in q_lower:
        sql = """
        SELECT 
            f.flight_no AS 'Flight No',
            a1.city || ' -> ' || a2.city AS 'Route',
            COUNT(b.booking_id) AS 'Confirmed Tickets',
            SUM(p.amount) AS 'Total Revenue (INR)'
        FROM flight f
        JOIN airport a1 ON f.source_airport = a1.airport_id
        JOIN airport a2 ON f.destination_airport = a2.airport_id
        JOIN booking b ON f.flight_id = b.flight_id
        JOIN payment p ON b.booking_id = p.booking_id
        WHERE p.payment_status = 'Paid'
        GROUP BY f.flight_id, f.flight_no, a1.city, a2.city
        ORDER BY SUM(p.amount) DESC;
        """
        df, err = db_manager.execute_query(conn, sql, is_mysql)
        if not df.empty:
            tot_rev = df['Total Revenue (INR)'].sum()
            top_flight = df.iloc[0]['Flight No']
            top_route = df.iloc[0]['Route']
            top_amt = int(df.iloc[0]['Total Revenue (INR)'])
            spoken = f"Total airport ticket revenue stands at {int(tot_rev):,} rupees. Top earning route is flight {top_flight} on {top_route} generating {top_amt:,} rupees."
            return {
                "category": "💰 Financial & Route Revenue Summary",
                "sql": sql,
                "dataframe": df,
                "summary": f"Calculated aggregated ticket revenues across all commercial flight routes.",
                "spoken_text": spoken,
                "status": "success"
            }

    # 4. Flight Audit Trail Queries
    if "audit" in q_lower or "history" in q_lower or "log" in q_lower or "changes" in q_lower:
        sql = """
        SELECT 
            audit_id AS 'Audit ID',
            flight_id AS 'Flight ID',
            operation_type AS 'Operation',
            message AS 'Message / Description',
            operation_time AS 'Timestamp'
        FROM flight_audit
        ORDER BY audit_id DESC
        LIMIT 20;
        """
        df, err = db_manager.execute_query(conn, sql, is_mysql)
        return {
            "category": "📜 Database Audit Trail",
            "sql": sql,
            "dataframe": df,
            "summary": f"Retrieved {len(df)} database trigger audit logs.",
            "spoken_text": f"Displaying {len(df)} recorded audit log events captured by database triggers.",
            "status": "success"
        }

    # 5. Count / Statistics queries
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

    # 6. Flights from a specific city / origin
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
                f"The earliest is {first_flight} to {first_dest} with fare starting at {fare} rupees."
            )
            return {
                "category": f"🛫 Outbound Flights from {city.title()}",
                "sql": sql,
                "dataframe": df,
                "summary": f"Found **{count}** flights departing from **{city.title()}**.",
                "spoken_text": spoken,
                "status": "success"
            }
        else:
            return {
                "category": f"🛫 Flights from {city.title()}",
                "sql": sql,
                "dataframe": df,
                "summary": f"No flights found departing from '{city.title()}'.",
                "spoken_text": f"There are no scheduled flights departing from {city.title()} right now.",
                "status": "warning"
            }

    # 7. Flights to a specific destination
    m_to = re.search(r'(?:to|arriving|destination)\s+([a-zA-Z]+)', q_lower)
    if ("flight" in q_lower or "arrive" in q_lower) and m_to:
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
            first_origin = df.iloc[0]['Origin']
            spoken = f"Found {count} flights heading to {city.title()}. Flight {first_flight} from {first_origin} is arriving earliest."
            return {
                "category": f"🛬 Inbound Flights to {city.title()}",
                "sql": sql,
                "dataframe": df,
                "summary": f"Found **{count}** flights arriving into **{city.title()}**.",
                "spoken_text": spoken,
                "status": "success"
            }
        else:
            return {
                "category": f"🛬 Flights to {city.title()}",
                "sql": sql,
                "dataframe": df,
                "summary": f"No inbound flights found for '{city.title()}'.",
                "spoken_text": f"No scheduled inbound flights to {city.title()} were found.",
                "status": "warning"
            }

    # 8. Passenger manifest on a flight
    m_flight = re.search(r'(?:flight|flt|on)\s*(?:#|id|no)?\s*([a-zA-Z0-9]+)', q_lower)
    if "passenger" in q_lower and m_flight:
        target = m_flight.group(1).upper()
        sql = f"""
        SELECT 
            p.passenger_id AS 'Passenger ID',
            p.passenger_name AS 'Name',
            p.phone AS 'Phone Number',
            p.age AS 'Age',
            b.seat_no AS 'Seat No',
            b.booking_status AS 'Booking Status',
            f.flight_no AS 'Flight No'
        FROM passenger p
        JOIN booking b ON p.passenger_id = b.passenger_id
        JOIN flight f ON b.flight_id = f.flight_id
        WHERE f.flight_no = '{target}' OR CAST(f.flight_id AS TEXT) = '{target}'
        ORDER BY b.seat_no;
        """
        df, err = db_manager.execute_query(conn, sql, is_mysql)
        if not df.empty:
            count = len(df)
            names = ", ".join(df['Name'].head(3).tolist())
            spoken = f"Found {count} passengers booked on flight {target}. Passengers include {names}."
            return {
                "category": f"📋 Passenger Manifest (Flight {target})",
                "sql": sql,
                "dataframe": df,
                "summary": f"Found **{count}** passengers booked on flight **{target}**.",
                "spoken_text": spoken,
                "status": "success"
            }

    # 9. Specific Passenger Search by Name
    m_pname = re.search(r'(?:passenger|who is|details of|find)\s+([a-zA-Z]+)', q_lower)
    if ("passenger" in q_lower or "booked" in q_lower) and m_pname:
        name = m_pname.group(1).strip()
        sql = f"""
        SELECT 
            p.passenger_id AS 'ID',
            p.passenger_name AS 'Passenger Name',
            p.phone AS 'Phone',
            p.age AS 'Age',
            f.flight_no AS 'Flight',
            b.seat_no AS 'Seat',
            b.booking_status AS 'Status'
        FROM passenger p
        LEFT JOIN booking b ON p.passenger_id = b.passenger_id
        LEFT JOIN flight f ON b.flight_id = f.flight_id
        WHERE LOWER(p.passenger_name) LIKE '%{name.lower()}%';
        """
        df, err = db_manager.execute_query(conn, sql, is_mysql)
        if not df.empty:
            p_full = df.iloc[0]['Passenger Name']
            f_no = df.iloc[0]['Flight'] or "None"
            seat = df.iloc[0]['Seat'] or "Unassigned"
            spoken = f"Found passenger {p_full}. Assigned to flight {f_no}, seat {seat}."
            return {
                "category": f"👤 Passenger Details: {p_full}",
                "sql": sql,
                "dataframe": df,
                "summary": f"Passenger **{p_full}** matches your inquiry.",
                "spoken_text": spoken,
                "status": "success"
            }

    # 10. Aircraft Fleet Status Queries
    if "aircraft" in q_lower or "plane" in q_lower or "fleet" in q_lower:
        status_filter = ""
        if "available" in q_lower:
            status_filter = "WHERE status = 'Available'"
        elif "maintenance" in q_lower:
            status_filter = "WHERE status = 'Maintenance'"

        sql = f"""
        SELECT 
            aircraft_id AS 'Aircraft ID',
            model AS 'Aircraft Model',
            capacity AS 'Seat Capacity',
            manufacturer AS 'Manufacturer',
            status AS 'Status'
        FROM aircraft
        {status_filter}
        ORDER BY capacity DESC;
        """
        df, err = db_manager.execute_query(conn, sql, is_mysql)
        count = len(df)
        spoken = f"Retrieved {count} aircraft in the fleet. The largest model is {df.iloc[0]['Aircraft Model']} with capacity of {df.iloc[0]['Seat Capacity']} seats."
        return {
            "category": "✈️ Aircraft Fleet Status",
            "sql": sql,
            "dataframe": df,
            "summary": f"Fleet inventory contains **{count}** aircraft records.",
            "spoken_text": spoken,
            "status": "success"
        }

    # 11. Payments and Payment Methods
    if "payment" in q_lower or "paid" in q_lower or "upi" in q_lower or "card" in q_lower:
        filter_str = ""
        if "upi" in q_lower:
            filter_str = "WHERE p.payment_method = 'UPI'"
        elif "card" in q_lower:
            filter_str = "WHERE p.payment_method = 'Card'"
        elif "netbanking" in q_lower or "net banking" in q_lower:
            filter_str = "WHERE p.payment_method = 'NetBanking'"

        sql = f"""
        SELECT 
            p.payment_id AS 'Payment ID',
            p.booking_id AS 'Booking ID',
            p.payment_date AS 'Date',
            p.amount AS 'Amount (INR)',
            p.payment_method AS 'Method',
            p.payment_status AS 'Status'
        FROM payment p
        {filter_str}
        ORDER BY p.amount DESC
        LIMIT 25;
        """
        df, err = db_manager.execute_query(conn, sql, is_mysql)
        count = len(df)
        total_sum = df['Amount (INR)'].sum() if not df.empty else 0
        spoken = f"Found {count} payment transactions totaling {int(total_sum):,} rupees."
        return {
            "category": "💳 Payment Transactions",
            "sql": sql,
            "dataframe": df,
            "summary": f"Retrieved **{count}** payment records from the billing ledger.",
            "spoken_text": spoken,
            "status": "success"
        }

    # 12. Fare comparison / Cheap flights
    if "cheap" in q_lower or "lowest" in q_lower or "under" in q_lower or "less than" in q_lower:
        m_amt = re.search(r'(\d+)', q_lower)
        threshold = int(m_amt.group(1)) if m_amt else 6000
        sql = f"""
        SELECT 
            f.flight_no AS 'Flight No',
            a1.city AS 'Origin',
            a2.city AS 'Destination',
            f.fare AS 'Fare (INR)'
        FROM flight f
        JOIN airport a1 ON f.source_airport = a1.airport_id
        JOIN airport a2 ON f.destination_airport = a2.airport_id
        WHERE f.fare <= {threshold}
        ORDER BY f.fare ASC;
        """
        df, err = db_manager.execute_query(conn, sql, is_mysql)
        if not df.empty:
            cheapest = df.iloc[0]
            spoken = f"Found {len(df)} flights under {threshold} rupees. The cheapest is {cheapest['Flight No']} from {cheapest['Origin']} to {cheapest['Destination']} at {int(cheapest['Fare (INR)'])} rupees."
            return {
                "category": f"🏷️ Flights Under ₹{threshold}",
                "sql": sql,
                "dataframe": df,
                "summary": f"Found **{len(df)}** affordable flights priced at or below ₹{threshold}.",
                "spoken_text": spoken,
                "status": "success"
            }

    # 13. Default Fallback Query (Comprehensive Flight Schedule)
    sql = """
    SELECT 
        f.flight_no AS 'Flight No',
        a1.city AS 'Origin',
        a2.city AS 'Destination',
        f.departure_time AS 'Departure',
        f.fare AS 'Fare (INR)',
        ac.model AS 'Aircraft'
    FROM flight f
    JOIN airport a1 ON f.source_airport = a1.airport_id
    JOIN airport a2 ON f.destination_airport = a2.airport_id
    LEFT JOIN aircraft ac ON f.aircraft_id = ac.aircraft_id
    ORDER BY f.departure_time ASC
    LIMIT 15;
    """
    df, err = db_manager.execute_query(conn, sql, is_mysql)
    spoken = f"Here is the active airport flight schedule with {len(df)} upcoming commercial flights."
    return {
        "category": "🛫 General Airport Flight Schedule",
        "sql": sql,
        "dataframe": df,
        "summary": "Displaying active commercial flight connections across major airport hubs.",
        "spoken_text": spoken,
        "status": "info"
    }
