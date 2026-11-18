"""
End-Semester DBMS Presentation Generator
Generates a 14-slide academic presentation for:
"Airport Management System Using Database Management System"
Vishwakarma Institute of Technology, Pune (VIT Pune)
Guide: Dr. Renu Kachhoria
Team Members: Shree Ambekar, Suyash Ambi, Varad Arali, Arush Patil, Arya Bagade
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(OUTPUT_DIR, "presentation_assets")
PPTX_PATH = os.path.join(OUTPUT_DIR, "Airport_Management_System_EndSem_Presentation.pptx")

# Palette constants
COLOR_BG = RGBColor(7, 15, 30)          # #070F1E Deep Dark Navy
COLOR_CARD_BG = RGBColor(15, 29, 56)     # #0F1D38 Card Navy
COLOR_CARD_BORDER = RGBColor(30, 58, 102)# #1E3A66 Border
COLOR_CYAN = RGBColor(56, 189, 248)      # #38BDF8 Cyan Accent
COLOR_BLUE = RGBColor(37, 99, 235)       # #2563EB Blue
COLOR_AMBER = RGBColor(245, 158, 11)     # #F59E0B Amber
COLOR_EMERALD = RGBColor(16, 185, 129)   # #10B981 Green
COLOR_WHITE = RGBColor(255, 255, 255)
COLOR_TEXT_LIGHT = RGBColor(226, 232, 240)
COLOR_TEXT_MUTED = RGBColor(148, 163, 184)


def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def set_slide_background(slide, color=COLOR_BG):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, tracker_text="END-SEMESTER DBMS PROJECT EVALUATION • VIT PUNE • AIDS-A"):
        # Header banner
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(1.1))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_track = tf.paragraphs[0]
        p_track.text = tracker_text.upper()
        p_track.font.size = Pt(9.5)
        p_track.font.bold = True
        p_track.font.color.rgb = COLOR_CYAN
        p_track.space_after = Pt(2)

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_WHITE

        # Subtle divider
        div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.45), Inches(11.733), Inches(0.02))
        div.fill.solid()
        div.fill.fore_color.rgb = COLOR_CARD_BORDER
        div.line.fill.background()

    def add_footer(slide, current_slide, total_slides=14):
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.733), Inches(0.35))
        tf = footer_box.text_frame
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p = tf.paragraphs[0]
        p.text = f"VIT Pune | AI&DS-A | Batch 1 | DBMS Course Project                                                                                Slide {current_slide} of {total_slides}"
        p.font.size = Pt(9)
        p.font.color.rgb = COLOR_TEXT_MUTED

    def add_card(slide, left, top, width, height, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.2)
        return card

    # ==========================================================================
    # SLIDE 1: TITLE SLIDE
    # ==========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    # Use template slide 1 background if available
    s1_bg_path = os.path.join(ASSETS_DIR, "template_slide_1.jpg")
    if not os.path.exists(s1_bg_path):
        s1_bg_path = os.path.join(ASSETS_DIR, "template_slide_1.png")
    
    if os.path.exists(s1_bg_path):
        s1.shapes.add_picture(s1_bg_path, 0, 0, Inches(13.333), Inches(7.5))
        # Add End-Semester Evaluation badge at top right
        badge = add_card(s1, 9.6, 0.4, 3.2, 0.45, bg_color=RGBColor(37, 99, 235), border_color=COLOR_CYAN)
        tb_b = s1.shapes.add_textbox(Inches(9.6), Inches(0.42), Inches(3.2), Inches(0.4))
        tf_b = tb_b.text_frame
        p_b = tf_b.paragraphs[0]
        p_b.text = "END-SEMESTER EVALUATION"
        p_b.font.size = Pt(11)
        p_b.font.bold = True
        p_b.font.color.rgb = COLOR_WHITE
        p_b.alignment = PP_ALIGN.CENTER
    else:
        set_slide_background(s1)
        # Fallback text
        tb = s1.shapes.add_textbox(Inches(1), Inches(2), Inches(11.333), Inches(3))
        tf = tb.text_frame
        p = tf.paragraphs[0]
        p.text = "AIRPORT MANAGEMENT SYSTEM USING DBMS"
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE

    # ==========================================================================
    # SLIDE 2: WORK DISTRIBUTION
    # ==========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "WORK DISTRIBUTION & CONTRIBUTION MATRIX", "TEAM RESPONSIBILITIES • CO1 TO CO6 MAPPING")

    members = [
        {
            "name": "Shree Ambekar",
            "co": "CO1: Requirements",
            "role": "Requirement Analysis, Problem Definition, EER Weak Entities & Comprehensive Documentation",
            "icon": "📋"
        },
        {
            "name": "Varad Arali",
            "co": "CO1 & CO2: Design",
            "role": "ER Diagram Modeling, Relational Schema Design, Normalization Proofs (1NF to BCNF)",
            "icon": "📐"
        },
        {
            "name": "Suyash Ambi",
            "co": "CO3: DDL & Tables",
            "role": "DDL, Table Architecture, Primary/Foreign Keys, Constraints & Population (MySQL/SQLite)",
            "icon": "🗄️"
        },
        {
            "name": "Arush Patil",
            "co": "CO3: Queries",
            "role": "DQL, Complex Joins (Equi, Outer, Self), Correlated Subqueries, Relational Views & Testing",
            "icon": "💻"
        },
        {
            "name": "Arya Bagade",
            "co": "CO4, CO5, CO6: Voice & Web",
            "role": "Two-Way Voice AI Engine, Web Speech API Integration, Stored Procedures, Triggers & Web Portal",
            "icon": "🎙️"
        }
    ]

    card_w = 2.22
    spacing = 0.16
    start_x = 0.8
    for i, m in enumerate(members):
        cx = start_x + i * (card_w + spacing)
        add_card(s2, cx, 1.7, card_w, 4.9)

        tb = s2.shapes.add_textbox(Inches(cx + 0.15), Inches(1.85), Inches(card_w - 0.3), Inches(4.6))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        p0.text = m["icon"]
        p0.font.size = Pt(28)
        p0.alignment = PP_ALIGN.CENTER
        p0.space_after = Pt(8)

        p1 = tf.add_paragraph()
        p1.text = m["name"]
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_WHITE
        p1.alignment = PP_ALIGN.CENTER
        p1.space_after = Pt(4)

        p2 = tf.add_paragraph()
        p2.text = m["co"]
        p2.font.size = Pt(9)
        p2.font.bold = True
        p2.font.color.rgb = COLOR_CYAN
        p2.alignment = PP_ALIGN.CENTER
        p2.space_after = Pt(12)

        p3 = tf.add_paragraph()
        p3.text = m["role"]
        p3.font.size = Pt(9.5)
        p3.font.color.rgb = COLOR_TEXT_LIGHT
        p3.alignment = PP_ALIGN.CENTER

    add_footer(s2, 2)

    # ==========================================================================
    # SLIDE 3: PROBLEM STATEMENT & AVIATION DATA SCALE
    # ==========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "PROBLEM STATEMENT: THE AVIATION DATA CHALLENGE", "PROBLEM ANALYSIS • DATA FRAGMENTATION • NEED FOR RELATIONAL DBMS")

    # Metrics row
    metric_data = [
        ("9.8 BILLION", "Passengers Annually (Global Aviation)", COLOR_CYAN),
        ("2,817+", "Commercial International Airports", COLOR_AMBER),
        ("185+ COUNTRIES", "Cross-Border Regulatory Hubs", COLOR_EMERALD),
        ("40,000+ DAILY", "Flight Departures & Reschedules", COLOR_CYAN)
    ]
    for i, (val, lbl, col) in enumerate(metric_data):
        mx = 0.8 + i * (2.8 + 0.17)
        add_card(s3, mx, 1.65, 2.8, 1.15)
        tb = s3.shapes.add_textbox(Inches(mx + 0.15), Inches(1.75), Inches(2.5), Inches(0.95))
        tf = tb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = val
        p0.font.size = Pt(16)
        p0.font.bold = True
        p0.font.color.rgb = col
        p1 = tf.add_paragraph()
        p1.text = lbl
        p1.font.size = Pt(8.5)
        p1.font.color.rgb = COLOR_TEXT_MUTED

    # 3 Content Columns
    cols_data = [
        ("01. THE PROBLEM", "Fragmented Operational Records", [
            "Data scattered across ticketing, check-in desks, baggage carousels, and gates.",
            "Schedule changes (e.g., AI101 delayed from 09:00 to 10:30) require manual multi-system updates.",
            "Risk of duplicate bookings, invalid seat allocations, and lost passenger manifests.",
            "High concurrency lock contention during morning peak flight departures."
        ]),
        ("02. EXISTING SHORTFALLS", "Isolated Siloed Systems", [
            "Manual coordination between airline operators, airport security, and baggage handlers.",
            "Lack of referential integrity: flight deletions leave orphan ticket records.",
            "Slow data retrieval: flat files or disconnected tables require multi-pass scans.",
            "No automated trigger auditing to track unauthorized fare or schedule modifications."
        ]),
        ("03. THE SOLUTION GAP", "Unified 3NF/BCNF Relational DBMS", [
            "Single relational data core connecting Airport, Aircraft, Flight, Passenger, Booking, Payment, and Baggage.",
            "Strict integrity constraints (PK, FK, CHECK, UNIQUE) preventing anomalous records.",
            "Sub-millisecond query retrieval via B+ Tree index structures and relational views.",
            "ACID transaction control with Strict 2PL for double-booking prevention."
        ])
    ]

    for i, (tag, heading, points) in enumerate(cols_data):
        cx = 0.8 + i * (3.8 + 0.16)
        add_card(s3, cx, 3.0, 3.8, 3.85)
        tb = s3.shapes.add_textbox(Inches(cx + 0.2), Inches(3.15), Inches(3.4), Inches(3.55))
        tf = tb.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = tag
        p0.font.size = Pt(9.5)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_CYAN

        p1 = tf.add_paragraph()
        p1.text = heading
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_WHITE
        p1.space_after = Pt(10)

        for pt in points:
            p_bullet = tf.add_paragraph()
            p_bullet.text = f"•  {pt}"
            p_bullet.font.size = Pt(9.5)
            p_bullet.font.color.rgb = COLOR_TEXT_LIGHT
            p_bullet.space_after = Pt(6)

    add_footer(s3, 3)

    # ==========================================================================
    # SLIDE 4: PROPOSED SOLUTION & 3-TIER ARCHITECTURE
    # ==========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "PROPOSED DBMS SOLUTION & 3-TIER ARCHITECTURE", "SYSTEM ARCHITECTURE • ANSI/SPARC 3-SCHEMA MODEL • OPERATIONAL DATA FLOW")

    # Left: 3-Tier Architecture Card
    add_card(s4, 0.8, 1.65, 5.7, 5.2)
    tb_arch = s4.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.3), Inches(4.9))
    tf_arch = tb_arch.text_frame
    tf_arch.word_wrap = True

    p = tf_arch.paragraphs[0]
    p.text = "🏛️ 3-TIER ANSI/SPARC ARCHITECTURE"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN
    p.space_after = Pt(8)

    tiers = [
        ("1. External / View Level (User Interfaces)", [
            "Voice Concierge Interface (Microphone speech-to-text queries)",
            "Live Flight Information Display System (FIDS schedule board)",
            "Passenger Check-in Portal & Finance Audit Console",
            "Decouples end-users from underlying logical database modifications."
        ]),
        ("2. Conceptual / Logical Level (Relational Schema)", [
            "Normalized 3NF / BCNF operational database (7 core tables)",
            "Referential constraints (Foreign Keys with CASCADE / RESTRICT)",
            "Relational Views: v_flight_schedule, v_passenger_manifest, v_revenue_summary",
            "PL/SQL Stored Procedures (sp_book_flight) & Trigger Audit Logs."
        ]),
        ("3. Internal / Physical Level (Storage & Indices)", [
            "InnoDB Storage Engine with Clustered B+ Tree Primary Key Indexing",
            "Write-Ahead Logging (WAL) via redo log buffer ensuring durability",
            "Physical tablespace files (AirportDB.ibd) and row-group storage."
        ])
    ]

    for t_title, t_items in tiers:
        pt = tf_arch.add_paragraph()
        pt.text = t_title
        pt.font.size = Pt(10.5)
        pt.font.bold = True
        pt.font.color.rgb = COLOR_AMBER
        pt.space_after = Pt(2)
        for it in t_items:
            pi = tf_arch.add_paragraph()
            pi.text = f"  ▹ {it}"
            pi.font.size = Pt(9)
            pi.font.color.rgb = COLOR_TEXT_LIGHT
            pi.space_after = Pt(3)

    # Right: Data Pipeline Flow
    add_card(s4, 6.7, 1.65, 5.8, 5.2)
    tb_pipe = s4.shapes.add_textbox(Inches(6.9), Inches(1.8), Inches(5.4), Inches(4.9))
    tf_pipe = tb_pipe.text_frame
    tf_pipe.word_wrap = True

    pp0 = tf_pipe.paragraphs[0]
    pp0.text = "🔄 END-TO-END DATA PROCESSING PIPELINE"
    pp0.font.size = Pt(13)
    pp0.font.bold = True
    pp0.font.color.rgb = COLOR_CYAN
    pp0.space_after = Pt(8)

    pipeline_steps = [
        ("STEP 1: AUTHORIZED DATA CAPTURE", "Voice speech input / Web form submissions / Flight dispatch schedule updates."),
        ("STEP 2: DOMAIN & REFERENTIAL INTEGRITY VALIDATION", "Pre-commit verification: valid aircraft capacity, passenger age >= 0, positive fare, and non-overlapping seat assignments."),
        ("STEP 3: RELATIONAL CORE ENGINE EXECUTION", "ACID transaction execution with Strict 2PL locks, SAVEPOINTS, and automatic trigger firing into flight_audit."),
        ("STEP 4: INTELLIGENT QUERY SYNTHESIS & RETRIEVAL", "Voice query engine maps natural language to multi-table Equi-Joins and aggregates across Airport, Flight, Passenger, and Booking."),
        ("STEP 5: MULTI-CHANNEL OUTPUT DISPATCH", "Instant visual rendering on FIDS departure screens, CSV manifest export, and browser-native Web Speech API audio spoken response.")
    ]

    for s_title, s_desc in pipeline_steps:
        ps = tf_pipe.add_paragraph()
        ps.text = s_title
        ps.font.size = Pt(10)
        ps.font.bold = True
        ps.font.color.rgb = COLOR_EMERALD
        ps.space_after = Pt(2)
        pd = tf_pipe.add_paragraph()
        pd.text = s_desc
        pd.font.size = Pt(9)
        pd.font.color.rgb = COLOR_TEXT_LIGHT
        pd.space_after = Pt(5)

    add_footer(s4, 4)

    # ==========================================================================
    # SLIDE 5: ER DIAGRAM & RELATIONAL SCHEMA MODEL
    # ==========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "ENTITY-RELATIONSHIP (ER) MODEL & SCHEMA ARCHITECTURE", "CONCEPTUAL MODELING • ENTITIES • CARDINALITIES • PRIMARY & FOREIGN KEYS")

    # Left: Embedded ER diagram image
    er_img = os.path.join(ASSETS_DIR, "er_diagram.png")
    if os.path.exists(er_img):
        s5.shapes.add_picture(er_img, Inches(0.8), Inches(1.65), Inches(6.8), Inches(5.2))
    else:
        add_card(s5, 0.8, 1.65, 6.8, 5.2)

    # Right: Relational Schema Details Card
    add_card(s5, 7.8, 1.65, 4.7, 5.2)
    tb_schema = s5.shapes.add_textbox(Inches(8.0), Inches(1.8), Inches(4.3), Inches(4.9))
    tf_sch = tb_schema.text_frame
    tf_sch.word_wrap = True

    ps0 = tf_sch.paragraphs[0]
    ps0.text = "📊 7 CORE NORMALIZED TABLES"
    ps0.font.size = Pt(12)
    ps0.font.bold = True
    ps0.font.color.rgb = COLOR_CYAN
    ps0.space_after = Pt(6)

    tables_summary = [
        ("AIRPORT (24 Rows)", "PK: airport_id | UNIQUE: airport_code\nAttrs: airport_name, city, country"),
        ("AIRCRAFT (22 Rows)", "PK: aircraft_id | CHECK (capacity > 0)\nAttrs: model, manufacturer, status"),
        ("FLIGHT (23 Rows)", "PK: flight_id | UNIQUE: flight_no\nFK: source_airport, dest_airport, aircraft_id\nAttrs: dep_time, arr_time, fare (CHECK >= 0)"),
        ("PASSENGER (43 Rows)", "PK: passenger_id | FK: flight_id\nAttrs: passenger_name, phone, age (CHECK >= 0)"),
        ("BOOKING (40 Rows)", "PK: booking_id | FK: passenger_id, flight_id\nAttrs: booking_date, seat_no, booking_status"),
        ("PAYMENT (30 Rows)", "PK: payment_id | FK: booking_id\nAttrs: payment_date, amount, method, status"),
        ("BAGGAGE (40 Rows)", "PK: baggage_id | FK: booking_id\nAttrs: baggage_weight, baggage_type, status")
    ]

    for t_name, t_detail in tables_summary:
        ptn = tf_sch.add_paragraph()
        ptn.text = f"• {t_name}"
        ptn.font.size = Pt(9.5)
        ptn.font.bold = True
        ptn.font.color.rgb = COLOR_AMBER
        ptd = tf_sch.add_paragraph()
        ptd.text = t_detail
        ptd.font.size = Pt(8.5)
        ptd.font.color.rgb = COLOR_TEXT_LIGHT
        ptd.space_after = Pt(4)

    add_footer(s5, 5)

    # ==========================================================================
    # SLIDE 6: RELATIONAL INTEGRITY CONSTRAINTS & CODD'S RULES
    # ==========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "RELATIONAL INTEGRITY CONSTRAINTS & CODD'S RULES EVALUATION", "DATA ACCURACY GUARANTEES • SYSTEMATIC CONSTRAINTS • 100% CODD COMPLIANCE")

    # Left: Integrity Constraints Table Card
    add_card(s6, 0.8, 1.65, 6.4, 5.2)
    tb_c = s6.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(6.0), Inches(4.9))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True

    p = tf_c.paragraphs[0]
    p.text = "🛡️ ENFORCED INTEGRITY CONSTRAINTS"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN
    p.space_after = Pt(6)

    constraints_list = [
        ("1. Entity Integrity", "Primary Keys (airport_id, flight_id, passenger_id, booking_id) are strictly NOT NULL and uniquely indexed via clustered B+ Trees."),
        ("2. Referential Integrity", "Foreign Keys enforce real-world operational linkages. Flight source and destination link to Airport; Booking links Passenger to Flight."),
        ("3. Domain Integrity", "Strict field types: fares use DECIMAL(10,2), dates use DATETIME/DATE, airport_code uses CHAR(3)."),
        ("4. Check Constraints", "CHECK (capacity > 0) prevents aircraft with zero seats;\nCHECK (fare >= 0) and CHECK (age >= 0) ensure semantic validity."),
        ("5. Unique Candidate Keys", "airport_code UNIQUE ('BOM', 'DEL', 'BLR') and flight_no UNIQUE ('AI101', 'AI202') prevent identity collisions."),
        ("6. Default Values", "DEFAULT 'Available' for aircraft status; DEFAULT 'Confirmed' for bookings; DEFAULT 'Paid' for payments.")
    ]

    for c_title, c_desc in constraints_list:
        pc1 = tf_c.add_paragraph()
        pc1.text = c_title
        pc1.font.size = Pt(10)
        pc1.font.bold = True
        pc1.font.color.rgb = COLOR_AMBER
        pc2 = tf_c.add_paragraph()
        pc2.text = c_desc
        pc2.font.size = Pt(8.5)
        pc2.font.color.rgb = COLOR_TEXT_LIGHT
        pc2.space_after = Pt(4)

    # Right: Codd's Rules Evaluation Card
    add_card(s6, 7.4, 1.65, 5.1, 5.2)
    tb_codd = s6.shapes.add_textbox(Inches(7.6), Inches(1.8), Inches(4.7), Inches(4.9))
    tf_codd = tb_codd.text_frame
    tf_codd.word_wrap = True

    pc0 = tf_codd.paragraphs[0]
    pc0.text = "📜 CODD'S 12 RULES AUDIT"
    pc0.font.size = Pt(13)
    pc0.font.bold = True
    pc0.font.color.rgb = COLOR_CYAN
    pc0.space_after = Pt(6)

    codd_items = [
        ("Rule 0: Foundation Rule", "The system manages all operational data purely through relational capabilities."),
        ("Rule 1: Information Rule", "All data (airports, flights, passengers) is represented strictly at the logical level as values in tables."),
        ("Rule 2: Guaranteed Access", "Every atomic datum is addressable via Table Name + Primary Key + Column Name."),
        ("Rule 3: Systematic NULLs", "NULL represents missing/unassigned data (e.g., baggage weights or optional contacts)."),
        ("Rule 4: Dynamic Catalog", "Database structure is queryable via standard SQL (INFORMATION_SCHEMA)."),
        ("Rule 8 & 9: Data Independence", "Physical disk layout changes or logical table partitioning do not alter frontend queries."),
        ("Rule 10: Integrity Independence", "Integrity constraints are enforced in the database catalog, not hardcoded in the frontend.")
    ]

    for r_title, r_desc in codd_items:
        pr1 = tf_codd.add_paragraph()
        pr1.text = f"✓ {r_title}"
        pr1.font.size = Pt(9.5)
        pr1.font.bold = True
        pr1.font.color.rgb = COLOR_EMERALD
        pr2 = tf_codd.add_paragraph()
        pr2.text = r_desc
        pr2.font.size = Pt(8.5)
        pr2.font.color.rgb = COLOR_TEXT_LIGHT
        pr2.space_after = Pt(3)

    add_footer(s6, 6)

    # ==========================================================================
    # SLIDE 7: RELATIONAL NORMALIZATION (1NF TO BCNF)
    # ==========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "RELATIONAL DESIGN & NORMALIZATION (1NF ➔ BCNF)", "FUNCTIONAL DEPENDENCIES • ANOMALY ELIMINATION • LOSSLESS JOIN DECOMPOSITION PROOF")

    stages = [
        ("1NF (First Normal Form)", "Atomic Attributes", [
            "Eliminated multivalued fields and repeating groups.",
            "Passenger phone numbers and baggage tags are atomic rows rather than comma-separated lists.",
            "Enforced primary keys on all tables."
        ], COLOR_CYAN),
        ("2NF (Second Normal Form)", "No Partial Dependencies", [
            "Must be in 1NF.",
            "All non-prime attributes are fully functionally dependent on the entire primary key.",
            "In Booking(passenger_id, flight_id, seat_no), passenger demographics are isolated into Passenger table."
        ], COLOR_BLUE),
        ("3NF (Third Normal Form)", "No Transitive Dependencies", [
            "Must be in 2NF.",
            "No non-prime attribute transitively depends on the primary key (X -> Y -> Z).",
            "In Flight table, flight_id -> aircraft_id -> model was transitive. Decomposed into separate Aircraft entity."
        ], COLOR_AMBER),
        ("BCNF (Boyce-Codd Normal Form)", "Strict Super Key Determinants", [
            "For every non-trivial FD X -> Y, X must strictly be a Super Key.",
            "Airport(airport_id, airport_code, name, city) has determinants airport_id and airport_code, both candidate superkeys.",
            "Relation satisfies BCNF."
        ], COLOR_EMERALD)
    ]

    card_w7 = 2.8
    spacing7 = 0.17
    for i, (st_name, st_sub, pts, col7) in enumerate(stages):
        cx = 0.8 + i * (card_w7 + spacing7)
        add_card(s7, cx, 1.65, card_w7, 3.8)

        tb = s7.shapes.add_textbox(Inches(cx + 0.15), Inches(1.8), Inches(card_w7 - 0.3), Inches(3.5))
        tf = tb.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = st_name
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = col7
        p0.space_after = Pt(2)

        p1 = tf.add_paragraph()
        p1.text = st_sub
        p1.font.size = Pt(9)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_TEXT_MUTED
        p1.space_after = Pt(8)

        for pt in pts:
            pb = tf.add_paragraph()
            pb.text = f"• {pt}"
            pb.font.size = Pt(8.5)
            pb.font.color.rgb = COLOR_TEXT_LIGHT
            pb.space_after = Pt(4)

    # Bottom Banner: Mathematical Proof of Lossless Join
    add_card(s7, 0.8, 5.65, 11.733, 1.25, bg_color=COLOR_CARD_BG, border_color=COLOR_EMERALD)
    tb_proof = s7.shapes.add_textbox(Inches(1.0), Inches(5.75), Inches(11.333), Inches(1.05))
    tf_p = tb_proof.text_frame
    tf_p.word_wrap = True

    pp0 = tf_p.paragraphs[0]
    pp0.text = "📐 MATHEMATICAL PROOF OF LOSSLESS JOIN DECOMPOSITION & DEPENDENCY PRESERVATION"
    pp0.font.size = Pt(10.5)
    pp0.font.bold = True
    pp0.font.color.rgb = COLOR_EMERALD
    pp0.space_after = Pt(2)

    pp1 = tf_p.add_paragraph()
    pp1.text = "Let relation R = (flight_id, flight_no, source_airport, destination_airport, aircraft_id, booking_id, passenger_id). Decomposed into R1(Flight) and R2(Booking). Common attribute R1 ∩ R2 = {flight_id}. Since flight_id -> R1 attributes (flight_id is the primary Super Key of R1), by Heath's Theorem the decomposition is guaranteed Lossless and Dependency Preserving without spurious tuples."
    pp1.font.size = Pt(8.5)
    pp1.font.color.rgb = COLOR_TEXT_LIGHT

    add_footer(s7, 7)

    # ==========================================================================
    # SLIDE 8: ADVANCED SQL IMPLEMENTATION (JOINS, SUBQUERIES & VIEWS)
    # ==========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "ADVANCED SQL IMPLEMENTATION: JOINS, SUBQUERIES & VIEWS", "RELATIONAL ALGEBRA MAPPING • MULTI-TABLE JOINS • COMPLEX ANALYTIC VIEWS")

    sql_boxes = [
        ("1. Multi-Table Equi-Join (FIDS Schedule)", (
            "SELECT f.flight_no, a1.city AS Origin, a2.city AS Dest, ac.model, f.fare\n"
            "FROM flight f\n"
            "JOIN airport a1 ON f.source_airport = a1.airport_id\n"
            "JOIN airport a2 ON f.destination_airport = a2.airport_id\n"
            "JOIN aircraft ac ON f.aircraft_id = ac.aircraft_id\n"
            "WHERE f.fare > 5500 ORDER BY f.departure_time;"
        ), "Combines 4 relations to produce full flight departure schedules with aircraft models."),
        
        ("2. Left Outer Join (Unassigned Fleet Assets)", (
            "SELECT ac.aircraft_id, ac.model, ac.capacity\n"
            "FROM aircraft ac\n"
            "LEFT JOIN flight f ON ac.aircraft_id = f.aircraft_id\n"
            "WHERE f.flight_no IS NULL;\n"
            "-- Identifies idle aircraft available for emergency maintenance or routing."
        ), "Preserves all aircraft tuples even when no scheduled flights exist in the Flight relation."),
        
        ("3. Correlated Subquery (Oldest Passenger per Route)", (
            "SELECT p1.passenger_name, p1.age, p1.flight_id\n"
            "FROM passenger p1\n"
            "WHERE p1.age = (\n"
            "    SELECT MAX(p2.age) FROM passenger p2\n"
            "    WHERE p2.flight_id = p1.flight_id\n"
            ");"
        ), "Subquery re-executes per outer tuple to filter demographic extremes per flight."),
        
        ("4. Relational Materialized View (Route Revenue)", (
            "CREATE VIEW v_revenue_summary AS\n"
            "SELECT f.flight_no, a1.city || ' -> ' || a2.city AS route,\n"
            "       COUNT(b.booking_id) AS tickets, SUM(p.amount) AS revenue\n"
            "FROM flight f JOIN booking b ON f.flight_id = b.flight_id\n"
            "JOIN payment p ON b.booking_id = p.booking_id\n"
            "GROUP BY f.flight_id, route HAVING SUM(p.amount) > 10000;"
        ), "Abstracts financial KPIs for executive analytics without repeated table scans.")
    ]

    for i, (q_title, q_code, q_desc) in enumerate(sql_boxes):
        rx = 0.8 + (i % 2) * (5.8 + 0.13)
        ry = 1.65 + (i // 2) * (2.55 + 0.12)
        add_card(s8, rx, ry, 5.8, 2.55)

        tb = s8.shapes.add_textbox(Inches(rx + 0.15), Inches(ry + 0.1), Inches(5.5), Inches(2.35))
        tf = tb.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = q_title
        p0.font.size = Pt(10.5)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_CYAN
        p0.space_after = Pt(2)

        p1 = tf.add_paragraph()
        p1.text = q_code
        p1.font.size = Pt(7.5)
        p1.font.name = "Consolas"
        p1.font.color.rgb = COLOR_EMERALD
        p1.space_after = Pt(3)

        p2 = tf.add_paragraph()
        p2.text = f"Note: {q_desc}"
        p2.font.size = Pt(8)
        p2.font.color.rgb = COLOR_TEXT_MUTED

    add_footer(s8, 8)

    # ==========================================================================
    # SLIDE 9: PL/SQL STORED PROCEDURES & TRIGGERS
    # ==========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "PL/SQL PROGRAMMABLE OBJECTS: PROCEDURES & TRIGGERS", "BUSINESS LOGIC AUTOMATION • ACID TRANSACTION CONTROL • AUDIT TRAIL LOGGING")

    # Left: Stored Procedure sp_book_flight
    add_card(s9, 0.8, 1.65, 5.8, 5.2)
    tb_sp = s9.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.4), Inches(4.9))
    tf_sp = tb_sp.text_frame
    tf_sp.word_wrap = True

    p = tf_sp.paragraphs[0]
    p.text = "⚡ STORED PROCEDURE: sp_book_flight"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN
    p.space_after = Pt(6)

    sp_code = (
        "DELIMITER //\n"
        "CREATE PROCEDURE sp_book_flight(\n"
        "    IN p_name VARCHAR(100), IN p_phone VARCHAR(15),\n"
        "    IN p_age INT, IN p_flight_id INT, IN p_seat VARCHAR(5),\n"
        "    IN p_method VARCHAR(20))\n"
        "BEGIN\n"
        "    DECLARE EXIT HANDLER FOR SQLEXCEPTION\n"
        "    BEGIN\n"
        "        ROLLBACK;\n"
        "        RESIGNAL;\n"
        "    END;\n"
        "    START TRANSACTION;\n"
        "    -- Step 1: Verify seat availability\n"
        "    IF EXISTS (SELECT 1 FROM booking WHERE flight_id = p_flight_id\n"
        "               AND seat_no = p_seat AND booking_status != 'Cancelled') THEN\n"
        "        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Seat Occupied';\n"
        "    END IF;\n"
        "    -- Step 2: Atomic multi-table insertion\n"
        "    INSERT INTO passenger VALUES (NULL, p_name, p_phone, p_flight_id, p_age);\n"
        "    INSERT INTO booking VALUES (NULL, LAST_INSERT_ID(), p_flight_id, CURDATE(), p_seat, 'Confirmed');\n"
        "    INSERT INTO payment VALUES (NULL, LAST_INSERT_ID(), CURDATE(), 5200.0, p_method, 'Paid');\n"
        "    COMMIT;\n"
        "END //\n"
        "DELIMITER ;"
    )
    p_code = tf_sp.add_paragraph()
    p_code.text = sp_code
    p_code.font.size = Pt(7.5)
    p_code.font.name = "Consolas"
    p_code.font.color.rgb = COLOR_EMERALD

    # Right: Trigger trg_after_flight_update & Audit
    add_card(s9, 6.8, 1.65, 5.733, 5.2)
    tb_trg = s9.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.9))
    tf_trg = tb_trg.text_frame
    tf_trg.word_wrap = True

    pt = tf_trg.paragraphs[0]
    pt.text = "📜 DATABASE TRIGGER: trg_after_flight_update"
    pt.font.size = Pt(12)
    pt.font.bold = True
    pt.font.color.rgb = COLOR_AMBER
    pt.space_after = Pt(6)

    trg_code = (
        "DELIMITER //\n"
        "CREATE TRIGGER trg_after_flight_update\n"
        "AFTER UPDATE ON flight\n"
        "FOR EACH ROW\n"
        "BEGIN\n"
        "    INSERT INTO flight_audit (\n"
        "        flight_id, operation_type, message, operation_time\n"
        "    ) VALUES (\n"
        "        NEW.flight_id, 'AFTER UPDATE',\n"
        "        CONCAT('Schedule changed: Departure=', NEW.departure_time,\n"
        "               ' Fare=', NEW.fare),\n"
        "        NOW()\n"
        "    );\n"
        "END //\n"
        "DELIMITER ;"
    )
    p_trg = tf_trg.add_paragraph()
    p_trg.text = trg_code
    p_trg.font.size = Pt(8)
    p_trg.font.name = "Consolas"
    p_trg.font.color.rgb = COLOR_EMERALD
    p_trg.space_after = Pt(8)

    p_expl = tf_trg.add_paragraph()
    p_expl.text = "Audit Logging Benefits:"
    p_expl.font.size = Pt(10)
    p_expl.font.bold = True
    p_expl.font.color.rgb = COLOR_WHITE
    p_expl.space_after = Pt(2)

    audit_pts = [
        "100% Automatic: Fired directly by database kernel on every schedule or fare edit.",
        "Non-Subversion (Codd Rule 12): No application process can bypass audit logging.",
        "Regulatory Compliance: Airport authorities maintain an immutable event log for flight delay investigations."
    ]
    for ap in audit_pts:
        pa = tf_trg.add_paragraph()
        pa.text = f"• {ap}"
        pa.font.size = Pt(8.5)
        pa.font.color.rgb = COLOR_TEXT_LIGHT
        pa.space_after = Pt(2)

    add_footer(s9, 9)

    # ==========================================================================
    # SLIDE 10: TRANSACTION MANAGEMENT & CONCURRENCY CONTROL
    # ==========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "TRANSACTION MANAGEMENT & CONCURRENCY CONTROL", "ACID GUARANTEES • CONFLICT SERIALIZABILITY • STRICT TWO-PHASE LOCKING (2PL)")

    # 4 ACID Cards
    acid_cards = [
        ("ATOMICITY", "All-or-Nothing", "Booking + Payment + Baggage commit together. If payment gateway times out, transaction executes ROLLBACK to SAVEPOINT, ensuring zero phantom charges.", COLOR_CYAN),
        ("CONSISTENCY", "Integrity Preserved", "State transition preserves capacity invariants. A flight with 190 seats can never exceed 190 bookings, enforced via CHECK and uniqueness constraints.", COLOR_BLUE),
        ("ISOLATION", "No Concurrency Anomalies", "Operates under REPEATABLE READ isolation, preventing Dirty Reads (W1 -> R2), Lost Updates (W1 -> W2), and Non-Repeatable Reads during simultaneous bookings.", COLOR_AMBER),
        ("DURABILITY", "Crash-Resilient State", "Committed flight reservations are flushed to non-volatile disk tablespaces and Write-Ahead Log buffers (ib_logfile0), surviving power outages.", COLOR_EMERALD)
    ]

    for i, (a_name, a_sub, a_text, a_col) in enumerate(acid_cards):
        ax = 0.8 + i * (2.8 + 0.17)
        add_card(s10, ax, 1.65, 2.8, 2.6)

        tb = s10.shapes.add_textbox(Inches(ax + 0.15), Inches(1.8), Inches(2.5), Inches(2.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = a_name
        p0.font.size = Pt(13)
        p0.font.bold = True
        p0.font.color.rgb = a_col

        p1 = tf.add_paragraph()
        p1.text = a_sub
        p1.font.size = Pt(9)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_TEXT_MUTED
        p1.space_after = Pt(6)

        p2 = tf.add_paragraph()
        p2.text = a_text
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = COLOR_TEXT_LIGHT

    # Bottom Row: Conflict Serializability & 2PL
    add_card(s10, 0.8, 4.45, 5.8, 2.45)
    tb_ser = s10.shapes.add_textbox(Inches(1.0), Inches(4.55), Inches(5.4), Inches(2.25))
    tf_ser = tb_ser.text_frame
    tf_ser.word_wrap = True

    ps0 = tf_ser.paragraphs[0]
    ps0.text = "🔄 CONFLICT SERIALIZABILITY (PREVENTING CYCLES)"
    ps0.font.size = Pt(11)
    ps0.font.bold = True
    ps0.font.color.rgb = COLOR_CYAN
    ps0.space_after = Pt(4)

    ps1 = tf_ser.add_paragraph()
    ps1.text = "• Tested via Precedence Graph (Serialization Graph) where nodes = transactions, directed edge Ti -> Tj if conflicting operation on same seat item.\n• DFS Cycle Detection algorithm verifies the schedule graph is Directed Acyclic (DAG).\n• Equivalent serial schedule T1 -> T2 executed without interleaving conflicts."
    ps1.font.size = Pt(8.5)
    ps1.font.color.rgb = COLOR_TEXT_LIGHT

    add_card(s10, 6.8, 4.45, 5.733, 2.45)
    tb_2pl = s10.shapes.add_textbox(Inches(7.0), Inches(4.55), Inches(5.3), Inches(2.25))
    tf_2pl = tb_2pl.text_frame
    tf_2pl.word_wrap = True

    p20 = tf_2pl.paragraphs[0]
    p20.text = "🔒 STRICT TWO-PHASE LOCKING PROTOCOL (STRICT 2PL)"
    p20.font.size = Pt(11)
    p20.font.bold = True
    p20.font.color.rgb = COLOR_AMBER
    p20.space_after = Pt(4)

    p21 = tf_2pl.add_paragraph()
    p21.text = "• Growing Phase: Transaction acquires exclusive X-locks on seat and payment tuples.\n• Lock Point: Maximum concurrency boundary reached.\n• Strict Shrinking Phase: All exclusive locks are held until COMMIT / ROLLBACK.\n• Eliminates Cascading Rollbacks and guarantees Strict Serializability."
    p21.font.size = Pt(8.5)
    p21.font.color.rgb = COLOR_TEXT_LIGHT

    add_footer(s10, 10)

    # ==========================================================================
    # SLIDE 11: STORAGE FORMATS, PARQUET & RECOVERY
    # ==========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "STORAGE FORMATS, PARQUET COLUMNAR SCAN & ARIES RECOVERY", "PHYSICAL STORAGE • PARQUET VS ROW-ORIENTED SCANS • WRITE-AHEAD LOGGING (WAL)")

    # Left: Parquet Simulation Card (matching syllabus slides)
    add_card(s11, 0.8, 1.65, 5.8, 5.2)
    tb_par = s11.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.4), Inches(4.9))
    tf_par = tb_par.text_frame
    tf_par.word_wrap = True

    pp0 = tf_par.paragraphs[0]
    pp0.text = "📊 PARQUET COLUMNAR VS ROW-STORE SCAN"
    pp0.font.size = Pt(12)
    pp0.font.bold = True
    pp0.font.color.rgb = COLOR_CYAN
    pp0.space_after = Pt(4)

    pp_sub = tf_par.add_paragraph()
    pp_sub.text = "Query: SELECT passenger_name, age FROM passenger WHERE age > 30;"
    pp_sub.font.size = Pt(8.5)
    pp_sub.font.name = "Consolas"
    pp_sub.font.color.rgb = COLOR_AMBER
    pp_sub.space_after = Pt(6)

    par_comparison = [
        ("Row-Oriented Storage (Traditional)", [
            "Row Width: 77 bytes (ID: 4B, Name: 50B, Phone: 15B, Flight: 4B, Age: 4B).",
            "100,000 Rows: Scans full 7.34 MB from disk.",
            "Wasted I/O: 30% of read bytes are unrequested columns (Phone, Flight ID)."
        ]),
        ("Parquet Columnar Storage (Advanced)", [
            "Organized in Row Groups, Column Chunks, and Pages with metadata footers.",
            "Only scans Age column (1.5B with bit-packing) + matching Name chunks.",
            "100,000 Rows: Scans only 0.78 MB from disk.",
            "Result: 10x I/O reduction and 3.5:1 Snappy compression ratio."
        ])
    ]

    for p_title, p_lines in par_comparison:
        ppt = tf_par.add_paragraph()
        ppt.text = p_title
        ppt.font.size = Pt(10)
        ppt.font.bold = True
        ppt.font.color.rgb = COLOR_WHITE
        ppt.space_after = Pt(2)
        for pl in p_lines:
            ppl = tf_par.add_paragraph()
            ppl.text = f"  ▹ {pl}"
            ppl.font.size = Pt(8.5)
            ppl.font.color.rgb = COLOR_TEXT_LIGHT
            ppl.space_after = Pt(2)

    # Right: ARIES Recovery System Card
    add_card(s11, 6.8, 1.65, 5.733, 5.2)
    tb_rec = s11.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.9))
    tf_rec = tb_rec.text_frame
    tf_rec.word_wrap = True

    pr0 = tf_rec.paragraphs[0]
    pr0.text = "🛡️ ARIES CRASH RECOVERY & WAL PROTOCOL"
    pr0.font.size = Pt(12)
    pr0.font.bold = True
    pr0.font.color.rgb = COLOR_EMERALD
    pr0.space_after = Pt(6)

    rec_phases = [
        ("Write-Ahead Logging (WAL) Invariant", "Log records <T, X, V_old, V_new> MUST be flushed to non-volatile disk before dirty data pages are written. Guarantees Atomicity & Durability."),
        ("1. Analysis Phase", "Scans log forward from the most recent fuzzy checkpoint. Reconstructs dirty page table and identifies active uncommitted transactions (Undo List = {T2, T3})."),
        ("2. Redo Phase (Repeating History)", "Scans forward from lowest unwritten LSN. Reapplies all logged operations (both committed and uncommitted) to restore pre-crash database state."),
        ("3. Undo Phase (Rollback)", "Scans backward from crash point. Undoes all changes of active uncommitted transactions T2 and T3, writing Compensating Log Records (CLRs).")
    ]

    for r_title, r_desc in rec_phases:
        prt = tf_rec.add_paragraph()
        prt.text = r_title
        prt.font.size = Pt(10)
        prt.font.bold = True
        prt.font.color.rgb = COLOR_AMBER
        prt.space_after = Pt(2)
        prd = tf_rec.add_paragraph()
        prd.text = r_desc
        prd.font.size = Pt(8.5)
        prd.font.color.rgb = COLOR_TEXT_LIGHT
        prd.space_after = Pt(4)

    add_footer(s11, 11)

    # ==========================================================================
    # SLIDE 12: EMERGING TRENDS (NOSQL & OLAP DATA WAREHOUSE)
    # ==========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "EMERGING TRENDS: NOSQL PARADIGMS & OLAP STAR SCHEMA", "BIG DATA ARCHITECTURE • BASE VS ACID • MULTI-DIMENSIONAL BUSINESS INTELLIGENCE")

    # Left: 4 NoSQL Models Card
    add_card(s12, 0.8, 1.65, 5.8, 5.2)
    tb_nosql = s12.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.4), Inches(4.9))
    tf_nosql = tb_nosql.text_frame
    tf_nosql.word_wrap = True

    pn0 = tf_nosql.paragraphs[0]
    pn0.text = "🌐 4 NOSQL PARADIGMS IN AIRPORT SYSTEMS"
    pn0.font.size = Pt(12)
    pn0.font.bold = True
    pn0.font.color.rgb = COLOR_CYAN
    pn0.space_after = Pt(6)

    nosql_models = [
        ("1. Document Store (MongoDB)", "Stores complete passenger e-tickets as nested JSON documents (Passenger + Flight + Baggage + Payment in 1 read)."),
        ("2. Key-Value Store (Redis)", "Sub-millisecond in-memory flight radar cache ('flight:AI101:status' -> 'On-Time | Gate 12B') and seat locks."),
        ("3. Column-Family (Cassandra)", "High-throughput IoT engine telemetry and flight black-box time-series sensor data."),
        ("4. Graph Database (Neo4j)", "Models airport hub flight route network for Cypher-based shortest flight path traversal (BOM -> DEL -> COK).")
    ]

    for m_title, m_desc in nosql_models:
        pmt = tf_nosql.add_paragraph()
        pmt.text = m_title
        pmt.font.size = Pt(10)
        pmt.font.bold = True
        pmt.font.color.rgb = COLOR_AMBER
        pmt.space_after = Pt(1)
        pmd = tf_nosql.add_paragraph()
        pmd.text = m_desc
        pmd.font.size = Pt(8.5)
        pmd.font.color.rgb = COLOR_TEXT_LIGHT
        pmd.space_after = Pt(4)

    # Right: Data Warehouse Star Schema & OLAP Card
    add_card(s12, 6.8, 1.65, 5.733, 5.2)
    tb_olap = s12.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.9))
    tf_olap = tb_olap.text_frame
    tf_olap.word_wrap = True

    po0 = tf_olap.paragraphs[0]
    po0.text = "📈 OLAP DATA WAREHOUSE: STAR SCHEMA"
    po0.font.size = Pt(12)
    po0.font.bold = True
    po0.font.color.rgb = COLOR_EMERALD
    po0.space_after = Pt(6)

    star_schema_details = [
        ("Central Fact Table: Fact_Flight_Operations", "Measures: tickets_sold, total_revenue, departure_delay_min, fuel_consumed_liters, baggage_weight_kg.\nKeys: time_key, origin_key, dest_key, aircraft_key, segment_key."),
        ("Surrounding Dimension Tables", "• Dim_Time (date, day, month, quarter, year, holiday)\n• Dim_Airport (code, city, state, country, hub_category)\n• Dim_Aircraft (model, manufacturer, seat_capacity)\n• Dim_Passenger_Segment (loyalty_tier, travel_purpose)"),
        ("Multi-Dimensional OLAP Operations", "• Roll-up: Daily ticket revenue -> Monthly -> Annual.\n• Drill-down: Total delay -> Breakdown by Gate / Aircraft.\n• Slice & Dice: Flights departing BOM to DEL in Q3-2026.\n• Pivot: Origin hubs on Y-axis, Months on X-axis.")
    ]

    for s_title, s_desc in star_schema_details:
        pst = tf_olap.add_paragraph()
        pst.text = s_title
        pst.font.size = Pt(10)
        pst.font.bold = True
        pst.font.color.rgb = COLOR_WHITE
        pst.space_after = Pt(1)
        psd = tf_olap.add_paragraph()
        psd.text = s_desc
        psd.font.size = Pt(8.5)
        psd.font.color.rgb = COLOR_TEXT_LIGHT
        psd.space_after = Pt(4)

    add_footer(s12, 12)

    # ==========================================================================
    # SLIDE 13: VOICE AI ARCHITECTURE & DUAL FRONTENDS
    # ==========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13)
    add_header(s13, "VOICE AI ARCHITECTURE & DUAL-FRONTEND SYSTEM", "TWO-WAY SPEECH PIPELINE • MODERN AVIATION WEB PORTAL • STREAMLIT DASHBOARD")

    # Left: Voice Pipeline Architecture
    add_card(s13, 0.8, 1.65, 5.8, 5.2)
    tb_v = s13.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.4), Inches(4.9))
    tf_v = tb_v.text_frame
    tf_v.word_wrap = True

    pv0 = tf_v.paragraphs[0]
    pv0.text = "🎙️ TWO-WAY VOICE AI PIPELINE"
    pv0.font.size = Pt(12)
    pv0.font.bold = True
    pv0.font.color.rgb = COLOR_CYAN
    pv0.space_after = Pt(6)

    v_steps = [
        ("1. Audio Speech Capture", "Captures spoken voice queries via Web Speech API (Microphone button in browser)."),
        ("2. Natural Language Parsing", "NLP classifier categorizes query intent (Flights from City, Baggage Status, Manifests, Route Revenue, Fleet Availability)."),
        ("3. Relational SQL Synthesis", "Synthesizes multi-table 3NF SQL statements with Equi-Joins and parameter bindings."),
        ("4. Dual-Backend Execution", "Executes query on live MySQL server or in-memory SQLite standalone fallback in < 5 ms."),
        ("5. Speech Synthesis Audio Output", "Synthesizes spoken natural answer via browser window.speechSynthesis with replay and speed controls.")
    ]

    for vs_title, vs_desc in v_steps:
        pvt = tf_v.add_paragraph()
        pvt.text = vs_title
        pvt.font.size = Pt(10)
        pvt.font.bold = True
        pvt.font.color.rgb = COLOR_AMBER
        pvt.space_after = Pt(1)
        pvd = tf_v.add_paragraph()
        pvd.text = vs_desc
        pvd.font.size = Pt(8.5)
        pvd.font.color.rgb = COLOR_TEXT_LIGHT
        pvd.space_after = Pt(3)

    # Right: Dual Frontend System
    add_card(s13, 6.8, 1.65, 5.733, 5.2)
    tb_fe = s13.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.9))
    tf_fe = tb_fe.text_frame
    tf_fe.word_wrap = True

    pf0 = tf_fe.paragraphs[0]
    pf0.text = "🖥️ DUAL-FRONTEND WEB ECOSYSTEM"
    pf0.font.size = Pt(12)
    pf0.font.bold = True
    pf0.font.color.rgb = COLOR_EMERALD
    pf0.space_after = Pt(6)

    frontends = [
        ("Frontend 1: Streamlit Operations Dashboard (app.py)", [
            "Voice Concierge tab with microphone recording",
            "Real-time Flight Information Display System (FIDS)",
            "Database table explorer & custom SQL terminal",
            "Interactive Stored Procedure & Trigger execution studio",
            "Comprehensive DBMS Syllabus interactive lab (Units 1-6)"
        ]),
        ("Frontend 2: Aviation Cockpit Web Portal (web_portal/)", [
            "Modern Single-Page Application (SPA) with glassmorphism UI",
            "Live animated airspace radar canvas with vector sweep",
            "Native Web Speech API speech-to-text & audio responses",
            "Searchable FIDS board, table viewer & direct SQL terminal",
            "Lightweight REST API backend (api_server.py) or standalone HTML"
        ]),
        ("Verified Academic Dataset", [
            "24 Airport Hubs | 22 Aircraft | 23 Flights",
            "43 Passengers | 40 Bookings | 30 Payments | 40 Baggage Tags"
        ])
    ]

    for fe_title, fe_items in frontends:
        pft = tf_fe.add_paragraph()
        pft.text = fe_title
        pft.font.size = Pt(10)
        pft.font.bold = True
        pft.font.color.rgb = COLOR_WHITE
        pft.space_after = Pt(1)
        for fi in fe_items:
            pfi = tf_fe.add_paragraph()
            pfi.text = f"  ▹ {fi}"
            pfi.font.size = Pt(8.5)
            pfi.font.color.rgb = COLOR_TEXT_LIGHT
            pfi.space_after = Pt(2)

    add_footer(s13, 13)

    # ==========================================================================
    # SLIDE 14: CONCLUSION, OUTCOMES & THANK YOU
    # ==========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    # Use template slide 8 background if available
    s8_bg_path = os.path.join(ASSETS_DIR, "thank_you_bg.jpg")
    if not os.path.exists(s8_bg_path):
        s8_bg_path = os.path.join(ASSETS_DIR, "thank_you_bg.png")
    if os.path.exists(s8_bg_path):
        s14.shapes.add_picture(s8_bg_path, 0, 0, Inches(13.333), Inches(7.5))
    else:
        set_slide_background(s14)

    # Semi-transparent overlay card for end-sem viva summary
    add_card(s14, 1.2, 1.0, 10.933, 5.5, bg_color=RGBColor(7, 15, 30), border_color=COLOR_CYAN)

    tb_end = s14.shapes.add_textbox(Inches(1.5), Inches(1.2), Inches(10.333), Inches(5.1))
    tf_end = tb_end.text_frame
    tf_end.word_wrap = True

    pe0 = tf_end.paragraphs[0]
    pe0.text = "AIRPORT MANAGEMENT SYSTEM USING DBMS"
    pe0.font.size = Pt(20)
    pe0.font.bold = True
    pe0.font.color.rgb = COLOR_CYAN
    pe0.alignment = PP_ALIGN.CENTER
    pe0.space_after = Pt(2)

    pe1 = tf_end.add_paragraph()
    pe1.text = "END-SEMESTER PROJECT OUTCOMES & ACADEMIC DEFENSE SUMMARY"
    pe1.font.size = Pt(11)
    pe1.font.bold = True
    pe1.font.color.rgb = COLOR_AMBER
    pe1.alignment = PP_ALIGN.CENTER
    pe1.space_after = Pt(12)

    # 4 Achievement Cards inside slide 14
    achievements = [
        "✓ 100% Normalized 3NF/BCNF Schema: Eliminated update anomalies with mathematical proof of Lossless Join.",
        "✓ Full Syllabus Coverage (Units 1 - 6): Implemented 3-Tier Architecture, Codd's Rules, Complex Joins, Normalization, ACID Transactions, Strict 2PL, Parquet Storage, NoSQL, and Data Warehousing.",
        "✓ Real-Time Two-Way Voice AI: Seamless voice-to-SQL translation with zero-latency browser speech synthesis.",
        "✓ Dual Frontend Architecture: Production-ready Streamlit dashboard + high-performance aviation web portal."
    ]
    for ach in achievements:
        pa = tf_end.add_paragraph()
        pa.text = ach
        pa.font.size = Pt(10)
        pa.font.color.rgb = COLOR_WHITE
        pa.space_after = Pt(6)

    pe_div = tf_end.add_paragraph()
    pe_div.text = "────────────────────────────────────────────────────────────────────────────"
    pe_div.font.size = Pt(9)
    pe_div.font.color.rgb = COLOR_CARD_BORDER
    pe_div.alignment = PP_ALIGN.CENTER
    pe_div.space_after = Pt(6)

    # Guide & Team Credits
    pe_credits = tf_end.add_paragraph()
    pe_credits.text = "Project Guide: Dr. Renu Kachhoria\nTeam Members: Shree Ambekar | Suyash Ambi | Varad Arali | Arush Patil | Arya Bagade\nClass: AI&DS-A | Batch: 1 | Vishwakarma Institute of Technology, Pune"
    pe_credits.font.size = Pt(10.5)
    pe_credits.font.bold = True
    pe_credits.font.color.rgb = COLOR_TEXT_LIGHT
    pe_credits.alignment = PP_ALIGN.CENTER
    pe_credits.space_after = Pt(10)

    pe_ty = tf_end.add_paragraph()
    pe_ty.text = "THANK YOU! READY FOR VIVA VOCE & QUESTIONS"
    pe_ty.font.size = Pt(16)
    pe_ty.font.bold = True
    pe_ty.font.color.rgb = COLOR_EMERALD
    pe_ty.alignment = PP_ALIGN.CENTER

    add_footer(s14, 14)

    # Save presentation
    prs.save(PPTX_PATH)
    print(f"Presentation generated successfully: {PPTX_PATH}")
    print(f"Total slides: {len(prs.slides)}")


if __name__ == "__main__":
    create_deck()
