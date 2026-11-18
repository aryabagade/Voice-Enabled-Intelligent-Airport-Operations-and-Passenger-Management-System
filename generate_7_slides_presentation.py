import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(SCRIPT_DIR, "presentation_assets")
PPTX_PATH = os.path.join(SCRIPT_DIR, "Airport_Management_System_EndSem_Presentation.pptx")
PPTX_7SLIDES_PATH = os.path.join(SCRIPT_DIR, "Airport_Management_System_7_Slides.pptx")

# Palette constants
COLOR_BG = RGBColor(7, 15, 30)            # #070F1E Deep Dark Navy
COLOR_CARD_BG = RGBColor(15, 29, 56)       # #0F1D38 Card Navy
COLOR_CARD_BORDER = RGBColor(30, 58, 102)  # #1E3A66 Border Navy
COLOR_CODE_BG = RGBColor(10, 20, 40)       # #0A1428 Dark Code Box
COLOR_CYAN = RGBColor(56, 189, 248)        # #38BDF8 Cyan Accent
COLOR_BLUE = RGBColor(37, 99, 235)         # #2563EB Blue
COLOR_AMBER = RGBColor(245, 158, 11)       # #F59E0B Amber
COLOR_EMERALD = RGBColor(16, 185, 129)     # #10B981 Green
COLOR_PURPLE = RGBColor(168, 85, 247)      # #A855F7 Purple
COLOR_CORAL = RGBColor(244, 63, 94)        # #F43F5E Coral/Pink
COLOR_WHITE = RGBColor(255, 255, 255)
COLOR_TEXT_LIGHT = RGBColor(226, 232, 240) # #E2E8F0
COLOR_TEXT_MUTED = RGBColor(148, 163, 184) # #94A3B8

FONT_HEADING = "Segoe UI"
FONT_BODY = "Segoe UI"
FONT_CODE = "Consolas"

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # Blank slide

    exact_slide_1_path = os.path.join(ASSETS_DIR, "exact_slide_1.jpg")
    exact_slide_7_path = os.path.join(ASSETS_DIR, "exact_slide_7.jpg")
    vit_logo_path = os.path.join(ASSETS_DIR, "vit_logo.png")

    # =========================================================================
    # SLIDE 1: EXACT ORIGINAL TITLE SLIDE
    # =========================================================================
    print("Building Slide 1: Exact Original Title Slide...")
    slide1 = prs.slides.add_slide(blank_layout)
    if os.path.exists(exact_slide_1_path):
        slide1.shapes.add_picture(exact_slide_1_path, Inches(0), Inches(0), width=Inches(13.333), height=Inches(7.5))
    else:
        print("Warning: exact_slide_1.jpg not found!")

    # Helper functions for common slide elements
    def add_slide_scaffolding(slide, slide_num, title, subtitle, member_badge_text, member_badge_color=COLOR_CYAN):
        # Background fill
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = COLOR_BG
        bg.line.fill.background()

        # Top banner background bar
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(0.25), Inches(12.333), Inches(0.42))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = RGBColor(11, 23, 46)
        top_bar.line.color.rgb = COLOR_CARD_BORDER
        top_bar.line.width = Pt(1)

        # Top banner text - Left (VIT Pune)
        tb_left = slide.shapes.add_textbox(Inches(0.6), Inches(0.25), Inches(7.0), Inches(0.42))
        tf_l = tb_left.text_frame
        tf_l.word_wrap = True
        tf_l.margin_top = Inches(0.06)
        tf_l.margin_bottom = Inches(0)
        tf_l.margin_left = Inches(0.08)
        p_l = tf_l.paragraphs[0]
        p_l.text = "VISHWAKARMA INSTITUTE OF TECHNOLOGY, PUNE"
        p_l.font.name = FONT_HEADING
        p_l.font.size = Pt(10)
        p_l.font.bold = True
        p_l.font.color.rgb = COLOR_WHITE
        run_dept = p_l.add_run()
        run_dept.text = "  |  Department of Artificial Intelligence & Data Science"
        run_dept.font.bold = False
        run_dept.font.color.rgb = COLOR_TEXT_MUTED
        run_dept.font.size = Pt(9.5)

        # Top banner text - Right (Course)
        tb_right = slide.shapes.add_textbox(Inches(7.8), Inches(0.25), Inches(4.9), Inches(0.42))
        tf_r = tb_right.text_frame
        tf_r.word_wrap = True
        tf_r.margin_top = Inches(0.06)
        tf_r.margin_bottom = Inches(0)
        tf_r.margin_right = Inches(0.08)
        p_r = tf_r.paragraphs[0]
        p_r.alignment = PP_ALIGN.RIGHT
        p_r.text = "DBMS COURSE PROJECT (CS2227/ML2302)  |  AIDS-A (BATCH 1)"
        p_r.font.name = FONT_HEADING
        p_r.font.size = Pt(9.5)
        p_r.font.bold = True
        p_r.font.color.rgb = COLOR_CYAN

        # Title & Subtitle Box
        title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.72), Inches(8.0), Inches(0.85))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        tf_t.margin_top = Inches(0.02)
        tf_t.margin_left = Inches(0.05)
        tf_t.margin_bottom = Inches(0)
        p_t = tf_t.paragraphs[0]
        p_t.text = title
        p_t.font.name = FONT_HEADING
        p_t.font.size = Pt(17)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_WHITE

        p_sub = tf_t.add_paragraph()
        p_sub.text = subtitle
        p_sub.font.name = FONT_BODY
        p_sub.font.size = Pt(10.5)
        p_sub.font.color.rgb = COLOR_TEXT_MUTED
        p_sub.space_before = Pt(3)

        # Member Allocation Badge (Prominent Right Side)
        badge_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.6), Inches(0.76), Inches(4.233), Inches(0.72))
        badge_box.fill.solid()
        badge_box.fill.fore_color.rgb = RGBColor(16, 32, 64)
        badge_box.line.color.rgb = member_badge_color
        badge_box.line.width = Pt(1.5)
        tf_b = badge_box.text_frame
        tf_b.word_wrap = True
        tf_b.margin_top = Inches(0.08)
        tf_b.margin_bottom = Inches(0.05)
        tf_b.margin_left = Inches(0.12)
        tf_b.margin_right = Inches(0.12)
        p_b1 = tf_b.paragraphs[0]
        p_b1.text = "INDIVIDUAL TASK ALLOCATION & OWNERSHIP"
        p_b1.font.name = FONT_HEADING
        p_b1.font.size = Pt(8.5)
        p_b1.font.bold = True
        p_b1.font.color.rgb = member_badge_color

        p_b2 = tf_b.add_paragraph()
        p_b2.text = member_badge_text
        p_b2.font.name = FONT_HEADING
        p_b2.font.size = Pt(11.5)
        p_b2.font.bold = True
        p_b2.font.color.rgb = COLOR_WHITE
        p_b2.space_before = Pt(2)

        # Footer Bar
        footer_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(7.0), Inches(12.333), Inches(0.32))
        footer_bar.fill.solid()
        footer_bar.fill.fore_color.rgb = RGBColor(11, 23, 46)
        footer_bar.line.color.rgb = COLOR_CARD_BORDER
        footer_bar.line.width = Pt(1)

        tb_foot = slide.shapes.add_textbox(Inches(0.6), Inches(7.0), Inches(12.133), Inches(0.32))
        tf_foot = tb_foot.text_frame
        tf_foot.word_wrap = True
        tf_foot.margin_top = Inches(0.05)
        tf_foot.margin_bottom = Inches(0)
        p_foot = tf_foot.paragraphs[0]
        p_foot.text = "Airport Management System Using DBMS  |  Team: Shree Ambekar • Varad Arali • Suyash Ambi • Arush Patil • Arya Bagade"
        p_foot.font.name = FONT_BODY
        p_foot.font.size = Pt(9)
        p_foot.font.color.rgb = COLOR_TEXT_MUTED

        run_sn = p_foot.add_run()
        run_sn.text = f"  |  Slide {slide_num} of 7"
        run_sn.font.bold = True
        run_sn.font.color.rgb = COLOR_CYAN

    def add_card(slide, x, y, w, h, title, title_color=COLOR_CYAN, border_color=COLOR_CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_CARD_BG
        card.line.color.rgb = border_color
        card.line.width = Pt(1.2)

        # Header title box
        t_box = slide.shapes.add_textbox(Inches(x + 0.12), Inches(y + 0.08), Inches(w - 0.24), Inches(0.35))
        tf = t_box.text_frame
        tf.word_wrap = True
        tf.margin_top = Inches(0)
        tf.margin_left = Inches(0)
        tf.margin_bottom = Inches(0)
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = FONT_HEADING
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = title_color
        return card

    # =========================================================================
    # SLIDE 2: MEMBER 1 – SHREE AMBEKAR
    # Problem Definition, Requirements Analysis, EER Diagram & Weak Entities
    # =========================================================================
    print("Building Slide 2: Member 1 – Shree Ambekar...")
    slide2 = prs.slides.add_slide(blank_layout)
    add_slide_scaffolding(
        slide2, 2,
        "PROBLEM DEFINITION & REQUIREMENTS SPECIFICATION",
        "Aviation Operational Challenges • System Requirements • EER Modeling • Weak Entity Architecture",
        "MEMBER 1: SHREE AMBEKAR",
        COLOR_AMBER
    )

    # Left Column: Card 1 (Problem Definition) & Card 2 (Requirement Analysis)
    add_card(slide2, 0.5, 1.62, 5.9, 2.55, "1. AIRPORT DATA CHALLENGES & PROBLEM DEFINITION", COLOR_AMBER)
    tb2_1 = slide2.shapes.add_textbox(Inches(0.62), Inches(2.02), Inches(5.66), Inches(2.05))
    tf2_1 = tb2_1.text_frame
    tf2_1.word_wrap = True
    tf2_1.margin_top = Inches(0); tf2_1.margin_left = Inches(0); tf2_1.margin_bottom = Inches(0)

    bullets2_1 = [
        ("The Aviation Operational Dilemma: ", "Airports coordinate thousands of interdependent flights, fleet allocations, passenger manifests, and payments under strict zero-downtime safety constraints."),
        ("Data Fragmentation Pitfalls: ", "Legacy file-based and decoupled spreadsheets cause duplicate records, schedule desynchronization, orphan payments, and lack of referential integrity."),
        ("Frequent Runtime Mutations: ", "Gate reassignment, weather delays, and booking cancellations require instantaneous relational updates across multiple operational tiers."),
        ("Core Problem Statement: ", "To architect a robust, centralized 6-table Relational Database Management System (DBMS) that enforces ACID transaction safety, eliminates anomalies, and enables sub-second query resolution.")
    ]
    for i, (b_title, b_desc) in enumerate(bullets2_1):
        p = tf2_1.paragraphs[0] if i == 0 else tf2_1.add_paragraph()
        p.font.size = Pt(9.5)
        p.font.name = FONT_BODY
        p.space_after = Pt(4)
        r1 = p.add_run(); r1.text = "• " + b_title; r1.font.bold = True; r1.font.color.rgb = COLOR_WHITE
        r2 = p.add_run(); r2.text = b_desc; r2.font.color.rgb = COLOR_TEXT_LIGHT

    add_card(slide2, 0.5, 4.28, 5.9, 2.62, "2. SYSTEM REQUIREMENT SPECIFICATION (FR & NFR)", COLOR_CYAN)
    tb2_2 = slide2.shapes.add_textbox(Inches(0.62), Inches(4.68), Inches(5.66), Inches(2.15))
    tf2_2 = tb2_2.text_frame
    tf2_2.word_wrap = True
    tf2_2.margin_top = Inches(0); tf2_2.margin_left = Inches(0); tf2_2.margin_bottom = Inches(0)

    bullets2_2 = [
        ("Functional Requirements (FR):", ""),
        ("  • FR1 Hub & Fleet: ", "Maintain 24 airport hubs (IATA unique codes) and 22 aircraft with capacities."),
        ("  • FR2 Flight Operations: ", "Schedule 23 commercial routes linking origin, destination, and fleet assets."),
        ("  • FR3 Reservations: ", "Record 43 passengers and 40 confirmed bookings with unique seat allocations."),
        ("  • FR4 Billing & Audit: ", "Reconcile 30 multi-channel payments and track schedule modification audits."),
        ("Non-Functional Requirements (NFR):", ""),
        ("  • Data Integrity: ", "100% referential integrity with foreign key cascade/restrict constraints."),
        ("  • Sub-Second Latency: ", "B-Tree indexed retrieval of flight schedules and manifests in < 1 ms.")
    ]
    for i, (b_title, b_desc) in enumerate(bullets2_2):
        p = tf2_2.paragraphs[0] if i == 0 else tf2_2.add_paragraph()
        p.font.size = Pt(9.2)
        p.font.name = FONT_BODY
        p.space_after = Pt(2)
        if b_desc == "":
            r = p.add_run(); r.text = b_title; r.font.bold = True; r.font.color.rgb = COLOR_CYAN
        else:
            r1 = p.add_run(); r1.text = b_title; r1.font.bold = True; r1.font.color.rgb = COLOR_WHITE
            r2 = p.add_run(); r2.text = b_desc; r2.font.color.rgb = COLOR_TEXT_LIGHT

    # Right Column: Card 3 (EER & Weak Entities) & Card 4 (Documentation & Architecture)
    add_card(slide2, 6.7, 1.62, 6.133, 2.75, "3. EER MODELING & WEAK ENTITY ARCHITECTURE", COLOR_EMERALD)
    tb2_3 = slide2.shapes.add_textbox(Inches(6.82), Inches(2.02), Inches(5.89), Inches(2.25))
    tf2_3 = tb2_3.text_frame
    tf2_3.word_wrap = True
    tf2_3.margin_top = Inches(0); tf2_3.margin_left = Inches(0); tf2_3.margin_bottom = Inches(0)

    bullets2_3 = [
        ("Enhanced ER (EER) Abstraction: ", "Applied specialization and generalization hierarchies to model distinct airport entity classifications (Domestic vs International hubs, Fleet model variants)."),
        ("Participation Constraints: ", "Total participation (double-line) enforced between Booking and Flight—every reservation must correspond to an active scheduled route; partial participation for Aircraft."),
        ("Weak Entity Domain Analysis: ", "In airport operations, transaction records (e.g., Payment and Baggage manifests) represent existence-dependent Weak Entities:"),
        ("  • Identification Dependency: ", "A Payment cannot exist autonomously; it requires an identifying parent relationship to a confirmed Booking (booking_id)."),
        ("  • Partial Key Discriminator: ", "Transactions rely on composite foreign key linkage to establish primary identification."),
        ("  • Cascading Integrity: ", "Cancellation of a booking propagates deterministic state transitions to dependent billing and baggage allocations.")
    ]
    for i, (b_title, b_desc) in enumerate(bullets2_3):
        p = tf2_3.paragraphs[0] if i == 0 else tf2_3.add_paragraph()
        p.font.size = Pt(9.2)
        p.font.name = FONT_BODY
        p.space_after = Pt(3)
        r1 = p.add_run(); r1.text = ("• " if not b_title.startswith("  ") else "") + b_title
        r1.font.bold = True; r1.font.color.rgb = COLOR_WHITE if not b_title.startswith("  ") else COLOR_EMERALD
        r2 = p.add_run(); r2.text = b_desc; r2.font.color.rgb = COLOR_TEXT_LIGHT

    add_card(slide2, 6.7, 4.48, 6.133, 2.42, "4. PROJECT DOCUMENTATION & ARCHITECTURAL SCOPE", COLOR_PURPLE)
    tb2_4 = slide2.shapes.add_textbox(Inches(6.82), Inches(4.88), Inches(5.89), Inches(1.95))
    tf2_4 = tb2_4.text_frame
    tf2_4.word_wrap = True
    tf2_4.margin_top = Inches(0); tf2_4.margin_left = Inches(0); tf2_4.margin_bottom = Inches(0)

    bullets2_4 = [
        ("Software Requirements Specification (SRS): ", "Authored comprehensive IEEE 830-compliant project documentation formalizing functional scope, entity schemas, and data flow."),
        ("3-Schema ANSI/SPARC Framework: ", "Mapped operational layers across 3 distinct tiers:"),
        ("  • External Level: ", "Role-based views for Passenger self-service, Gate Agents, and Flight Dispatchers."),
        ("  • Conceptual Level: ", "Normalized 6-table unified relational schema with primary/foreign key graphs."),
        ("  • Internal Level: ", "InnoDB physical data files, clustered B+Tree indexes, and WAL logging.")
    ]
    for i, (b_title, b_desc) in enumerate(bullets2_4):
        p = tf2_4.paragraphs[0] if i == 0 else tf2_4.add_paragraph()
        p.font.size = Pt(9.2)
        p.font.name = FONT_BODY
        p.space_after = Pt(3)
        r1 = p.add_run(); r1.text = ("• " if not b_title.startswith("  ") else "") + b_title
        r1.font.bold = True; r1.font.color.rgb = COLOR_WHITE if not b_title.startswith("  ") else COLOR_PURPLE
        r2 = p.add_run(); r2.text = b_desc; r2.font.color.rgb = COLOR_TEXT_LIGHT

    # =========================================================================
    # SLIDE 3: MEMBER 2 – VARAD ARALI
    # ER Diagram, Relational Schema & Normalization (1NF to BCNF)
    # =========================================================================
    print("Building Slide 3: Member 2 – Varad Arali...")
    slide3 = prs.slides.add_slide(blank_layout)
    add_slide_scaffolding(
        slide3, 3,
        "CONCEPTUAL ER MODELING & RELATIONAL NORMALIZATION",
        "Entity-Relationship Graph • Relational Schema Synthesis • 1NF to BCNF Normalization • Anomaly Elimination",
        "MEMBER 2: VARAD ARALI",
        COLOR_CYAN
    )

    # Left Column: Card 1 (ER Diagram & Relationships) & Card 2 (Relational Schema Mapping)
    add_card(slide3, 0.5, 1.62, 5.9, 2.55, "1. ENTITY-RELATIONSHIP (ER) ARCHITECTURE", COLOR_CYAN)
    tb3_1 = slide3.shapes.add_textbox(Inches(0.62), Inches(2.02), Inches(5.66), Inches(2.05))
    tf3_1 = tb3_1.text_frame
    tf3_1.word_wrap = True
    tf3_1.margin_top = Inches(0); tf3_1.margin_left = Inches(0); tf3_1.margin_bottom = Inches(0)

    bullets3_1 = [
        ("Core Relational Entities: ", "Modeled 6 foundational operational tables: Airport, Aircraft, Flight, Passenger, Booking, and Payment."),
        ("Cardinality Ratios & Identifying Roles: ", ""),
        ("  • Airport (1) ➔ Flight (N): ", "Dual foreign key: 'Departs From' (source) and 'Arrives At' (destination)."),
        ("  • Aircraft (1) ➔ Flight (N): ", "'Operated By' foreign key linking aircraft asset capacity."),
        ("  • Passenger (1) ➔ Booking (N): ", "'Makes Reservation' connecting travelers to bookings."),
        ("  • Flight (1) ➔ Booking (N): ", "'Allocated On' mapping passengers to seat reservations."),
        ("  • Booking (1) ➔ Payment (N): ", "'Settled By' linking financial reconciliation to tickets.")
    ]
    for i, (b_title, b_desc) in enumerate(bullets3_1):
        p = tf3_1.paragraphs[0] if i == 0 else tf3_1.add_paragraph()
        p.font.size = Pt(9.2)
        p.font.name = FONT_BODY
        p.space_after = Pt(2.5)
        if b_desc == "":
            r = p.add_run(); r.text = b_title; r.font.bold = True; r.font.color.rgb = COLOR_CYAN
        else:
            r1 = p.add_run(); r1.text = ("• " if not b_title.startswith("  ") else "") + b_title
            r1.font.bold = True; r1.font.color.rgb = COLOR_WHITE
            r2 = p.add_run(); r2.text = b_desc; r2.font.color.rgb = COLOR_TEXT_LIGHT

    add_card(slide3, 0.5, 4.28, 5.9, 2.62, "2. RELATIONAL SCHEMA SYNTHESIS & KEYS", COLOR_AMBER)
    tb3_2 = slide3.shapes.add_textbox(Inches(0.62), Inches(4.68), Inches(5.66), Inches(2.15))
    tf3_2 = tb3_2.text_frame
    tf3_2.word_wrap = True
    tf3_2.margin_top = Inches(0); tf3_2.margin_left = Inches(0); tf3_2.margin_bottom = Inches(0)

    schemas = [
        ("Airport", "(airport_id [PK], airport_name, city, country, airport_code [UQ])"),
        ("Aircraft", "(aircraft_id [PK], model, capacity, manufacturer, status)"),
        ("Flight", "(flight_id [PK], flight_no [UQ], source_airport [FK], dest_airport [FK], aircraft_id [FK], departure_time, arrival_time, fare)"),
        ("Passenger", "(passenger_id [PK], passenger_name, phone, flight_id [FK], age)"),
        ("Booking", "(booking_id [PK], passenger_id [FK], flight_id [FK], booking_date, seat_no, booking_status)"),
        ("Payment", "(payment_id [PK], booking_id [FK], payment_date, amount, payment_method, payment_status)")
    ]
    p_head = tf3_2.paragraphs[0]
    p_head.text = "Mathematical Relation Definitions (Underlined PK, [FK] References):"
    p_head.font.size = Pt(9.5); p_head.font.bold = True; p_head.font.color.rgb = COLOR_AMBER; p_head.space_after = Pt(3)

    for tbl, atts in schemas:
        p = tf3_2.add_paragraph()
        p.font.size = Pt(8.8)
        p.font.name = FONT_CODE
        p.space_after = Pt(2)
        r1 = p.add_run(); r1.text = f"• {tbl} "; r1.font.bold = True; r1.font.color.rgb = COLOR_WHITE
        r2 = p.add_run(); r2.text = atts; r2.font.color.rgb = COLOR_TEXT_LIGHT

    # Right Column: Card 3 (Normalization 1NF to BCNF) & Card 4 (Anomaly Elimination)
    add_card(slide3, 6.7, 1.62, 6.133, 2.75, "3. STEP-BY-STEP NORMALIZATION (1NF ➔ BCNF)", COLOR_EMERALD)
    tb3_3 = slide3.shapes.add_textbox(Inches(6.82), Inches(2.02), Inches(5.89), Inches(2.25))
    tf3_3 = tb3_3.text_frame
    tf3_3.word_wrap = True
    tf3_3.margin_top = Inches(0); tf3_3.margin_left = Inches(0); tf3_3.margin_bottom = Inches(0)

    bullets3_3 = [
        ("1NF (First Normal Form): ", "Ensured all attribute values are atomic and indivisible. Eliminated repeating phone numbers and multi-seat reservation arrays by creating discrete passenger and booking tuple instances."),
        ("2NF (Second Normal Form): ", "Eliminated Partial Dependencies. Verified that every non-prime attribute is fully functionally dependent on the entire Primary Key. Candidate keys in Booking and Flight fully determine all respective attributes."),
        ("3NF (Third Normal Form): ", "Eliminated Transitive Dependencies (X ➔ Y, Y ➔ Z). City and country depend strictly on airport_id, not duplicated inside Flight. Aircraft manufacturer depends solely on aircraft_id."),
        ("BCNF (Boyce-Codd Normal Form): ", "Enforced that for every non-trivial functional dependency X ➔ Y, the determinant X is strictly a Super Key. All six entities satisfy BCNF criteria with zero redundant functional dependencies.")
    ]
    for i, (b_title, b_desc) in enumerate(bullets3_3):
        p = tf3_3.paragraphs[0] if i == 0 else tf3_3.add_paragraph()
        p.font.size = Pt(9.2)
        p.font.name = FONT_BODY
        p.space_after = Pt(3.5)
        r1 = p.add_run(); r1.text = "• " + b_title; r1.font.bold = True; r1.font.color.rgb = COLOR_WHITE
        r2 = p.add_run(); r2.text = b_desc; r2.font.color.rgb = COLOR_TEXT_LIGHT

    add_card(slide3, 6.7, 4.48, 6.133, 2.42, "4. ANOMALY ELIMINATION & LOSSLESS DECOMPOSITION", COLOR_PURPLE)
    tb3_4 = slide3.shapes.add_textbox(Inches(6.82), Inches(4.88), Inches(5.89), Inches(1.95))
    tf3_4 = tb3_4.text_frame
    tf3_4.word_wrap = True
    tf3_4.margin_top = Inches(0); tf3_4.margin_left = Inches(0); tf3_4.margin_bottom = Inches(0)

    bullets3_4 = [
        ("Insertion Anomaly Resolved: ", "New fleet assets (e.g., Boeing 787) can be registered into Aircraft without prematurely inventing unassigned flight schedules."),
        ("Deletion Anomaly Resolved: ", "Cancelling a passenger reservation in Booking deletes the ticket without erasing the underlying scheduled flight route or aircraft asset."),
        ("Update Anomaly Resolved: ", "Rescheduling flight AI101 requires modifying exactly ONE tuple in Flight; the update propagates instantaneously to all 40 dependent bookings."),
        ("Lossless Join Property: ", "Decomposition satisfies: (R1 ∩ R2) ➔ R1 or (R1 ∩ R2) ➔ R2, guaranteeing zero spurious tuples upon relational natural joins.")
    ]
    for i, (b_title, b_desc) in enumerate(bullets3_4):
        p = tf3_4.paragraphs[0] if i == 0 else tf3_4.add_paragraph()
        p.font.size = Pt(9.2)
        p.font.name = FONT_BODY
        p.space_after = Pt(3)
        r1 = p.add_run(); r1.text = "• " + b_title; r1.font.bold = True; r1.font.color.rgb = COLOR_WHITE
        r2 = p.add_run(); r2.text = b_desc; r2.font.color.rgb = COLOR_TEXT_LIGHT

    # =========================================================================
    # SLIDE 4: MEMBER 3 – SUYASH AMBI
    # Database Implementation: DDL, Table Creation, PK/FK & Data Population
    # =========================================================================
    print("Building Slide 4: Member 3 – Suyash Ambi...")
    slide4 = prs.slides.add_slide(blank_layout)
    add_slide_scaffolding(
        slide4, 4,
        "DATABASE IMPLEMENTATION: DDL, CONSTRAINTS & DATA POPULATION",
        "Physical Schema DDL • Referential Integrity & Foreign Keys • Systematic Constraints • Production Data Loading",
        "MEMBER 3: SUYASH AMBI",
        COLOR_EMERALD
    )

    # Left Column: Card 1 (DDL Statements) & Card 2 (PK & FK Actions)
    add_card(slide4, 0.5, 1.62, 5.9, 2.65, "1. DDL SCHEMA DEFINITIONS (6 CORE TABLES)", COLOR_EMERALD)
    tb4_1 = slide4.shapes.add_textbox(Inches(0.62), Inches(2.02), Inches(5.66), Inches(2.15))
    tf4_1 = tb4_1.text_frame
    tf4_1.word_wrap = True
    tf4_1.margin_top = Inches(0); tf4_1.margin_left = Inches(0); tf4_1.margin_bottom = Inches(0)

    code_ddl = """-- Physical DDL Implementation (InnoDB Engine)
CREATE TABLE Airport (
  airport_id INT PRIMARY KEY,
  airport_name VARCHAR(100) NOT NULL,
  city VARCHAR(50) NOT NULL, country VARCHAR(50) NOT NULL,
  airport_code CHAR(3) UNIQUE NOT NULL
) ENGINE=InnoDB;

CREATE TABLE Flight (
  flight_id INT PRIMARY KEY,
  flight_no VARCHAR(10) UNIQUE NOT NULL,
  source_airport INT NOT NULL, destination_airport INT NOT NULL,
  aircraft_id INT NOT NULL, departure_time DATETIME NOT NULL,
  arrival_time DATETIME NOT NULL, fare DECIMAL(10,2) NOT NULL,
  FOREIGN KEY (source_airport) REFERENCES Airport(airport_id),
  FOREIGN KEY (destination_airport) REFERENCES Airport(airport_id),
  FOREIGN KEY (aircraft_id) REFERENCES Aircraft(aircraft_id)
) ENGINE=InnoDB;"""
    p4_1 = tf4_1.paragraphs[0]
    p4_1.text = code_ddl
    p4_1.font.name = FONT_CODE
    p4_1.font.size = Pt(8.2)
    p4_1.font.color.rgb = COLOR_TEXT_LIGHT

    add_card(slide4, 0.5, 4.38, 5.9, 2.52, "2. PRIMARY KEYS & REFERENTIAL FOREIGN KEYS", COLOR_CYAN)
    tb4_2 = slide4.shapes.add_textbox(Inches(0.62), Inches(4.78), Inches(5.66), Inches(2.05))
    tf4_2 = tb4_2.text_frame
    tf4_2.word_wrap = True
    tf4_2.margin_top = Inches(0); tf4_2.margin_left = Inches(0); tf4_2.margin_bottom = Inches(0)

    bullets4_2 = [
        ("Explicit Primary Keys: ", "Configured non-nullable, unique surrogate identifiers (airport_id, aircraft_id, flight_id, passenger_id, booking_id, payment_id)."),
        ("Foreign Key Cascades & Restrictions: ", ""),
        ("  • Airport ➔ Flight: ", "ON DELETE RESTRICT prevents accidental deletion of active airport hubs."),
        ("  • Aircraft ➔ Flight: ", "ON DELETE CASCADE / RESTRICT protects schedule routing."),
        ("  • Booking ➔ Payment: ", "ON DELETE CASCADE ensures cancelled tickets automatically cascade to settlement records without orphaned transactions.")
    ]
    for i, (b_title, b_desc) in enumerate(bullets4_2):
        p = tf4_2.paragraphs[0] if i == 0 else tf4_2.add_paragraph()
        p.font.size = Pt(9.2)
        p.font.name = FONT_BODY
        p.space_after = Pt(2.5)
        if b_desc == "":
            r = p.add_run(); r.text = b_title; r.font.bold = True; r.font.color.rgb = COLOR_CYAN
        else:
            r1 = p.add_run(); r1.text = ("• " if not b_title.startswith("  ") else "") + b_title
            r1.font.bold = True; r1.font.color.rgb = COLOR_WHITE
            r2 = p.add_run(); r2.text = b_desc; r2.font.color.rgb = COLOR_TEXT_LIGHT

    # Right Column: Card 3 (Integrity Constraints) & Card 4 (Database Population)
    add_card(slide4, 6.7, 1.62, 6.133, 2.65, "3. SYSTEMATIC INTEGRITY CONSTRAINTS", COLOR_AMBER)
    tb4_3 = slide4.shapes.add_textbox(Inches(6.82), Inches(2.02), Inches(5.89), Inches(2.15))
    tf4_3 = tb4_3.text_frame
    tf4_3.word_wrap = True
    tf4_3.margin_top = Inches(0); tf4_3.margin_left = Inches(0); tf4_3.margin_bottom = Inches(0)

    bullets4_3 = [
        ("Domain Constraints (CHECK): ", "Enforces valid numeric ranges:"),
        ("  • Aircraft.capacity: ", "CHECK (capacity > 0) guarantees physical passenger seating."),
        ("  • Flight.fare: ", "CHECK (fare >= 0.00) protects against negative pricing glitches."),
        ("  • Passenger.age: ", "CHECK (age >= 0 AND age <= 120) verifies demographic validity."),
        ("Candidate & Uniqueness Constraints: ", "UNIQUE (airport_code) enforces 3-letter IATA standard (BOM, DEL); UNIQUE (flight_no) prevents duplicate commercial callsigns."),
        ("Default Values: ", "status DEFAULT 'Available' on Aircraft; booking_status DEFAULT 'Confirmed'.")
    ]
    for i, (b_title, b_desc) in enumerate(bullets4_3):
        p = tf4_3.paragraphs[0] if i == 0 else tf4_3.add_paragraph()
        p.font.size = Pt(9.2)
        p.font.name = FONT_BODY
        p.space_after = Pt(2.5)
        r1 = p.add_run(); r1.text = ("• " if not b_title.startswith("  ") else "") + b_title
        r1.font.bold = True; r1.font.color.rgb = COLOR_WHITE if not b_title.startswith("  ") else COLOR_AMBER
        r2 = p.add_run(); r2.text = b_desc; r2.font.color.rgb = COLOR_TEXT_LIGHT

    add_card(slide4, 6.7, 4.38, 6.133, 2.52, "4. DATABASE POPULATION & PRODUCTION DATASET", COLOR_PURPLE)
    tb4_4 = slide4.shapes.add_textbox(Inches(6.82), Inches(4.78), Inches(5.89), Inches(2.05))
    tf4_4 = tb4_4.text_frame
    tf4_4.word_wrap = True
    tf4_4.margin_top = Inches(0); tf4_4.margin_left = Inches(0); tf4_4.margin_bottom = Inches(0)

    bullets4_4 = [
        ("Verified Academic Dataset Metrics (Loaded via INSERT SQL):", ""),
        ("  • 24 Airports: ", "Major domestic/international hubs (BOM, DEL, BLR, HYD, PUN, GOI, CCU, COK...)."),
        ("  • 22 Aircraft: ", "Fleet assets spanning Airbus A320/A321/A350 and Boeing 737/777/787."),
        ("  • 23 Flights: ", "Active commercial routes connecting hubs with timestamps and tariffs."),
        ("  • 43 Passengers: ", "Demographic records with verified contact numbers and ages."),
        ("  • 40 Bookings: ", "Confirmed ticket reservations with assigned seats (1A, 2B, 3C...)."),
        ("  • 30 Payments: ", "Multi-channel settlement audit logs (UPI, Credit Cards, NetBanking)."),
        ("Zero Constraint Violations: ", "Successfully executed across MySQL 8.0 and SQLite engines.")
    ]
    for i, (b_title, b_desc) in enumerate(bullets4_4):
        p = tf4_4.paragraphs[0] if i == 0 else tf4_4.add_paragraph()
        p.font.size = Pt(9.2)
        p.font.name = FONT_BODY
        p.space_after = Pt(2)
        if b_desc == "":
            r = p.add_run(); r.text = b_title; r.font.bold = True; r.font.color.rgb = COLOR_PURPLE
        else:
            r1 = p.add_run(); r1.text = ("• " if not b_title.startswith("  ") else "") + b_title
            r1.font.bold = True; r1.font.color.rgb = COLOR_WHITE
            r2 = p.add_run(); r2.text = b_desc; r2.font.color.rgb = COLOR_TEXT_LIGHT

    # =========================================================================
    # SLIDE 5: MEMBER 4 – ARUSH PATIL
    # SQL Queries and Testing: DQL, Joins, Subqueries & Views
    # =========================================================================
    print("Building Slide 5: Member 4 – Arush Patil...")
    slide5 = prs.slides.add_slide(blank_layout)
    add_slide_scaffolding(
        slide5, 5,
        "ADVANCED SQL OPERATIONS: DQL, JOINS, SUBQUERIES & VIEWS",
        "Multi-Table Relational Joins • Correlated Subqueries • Analytic Views • Execution Performance & Testing",
        "MEMBER 4: ARUSH PATIL",
        COLOR_BLUE
    )

    # Left Column: Card 1 (Complex Joins) & Card 2 (Correlated Subqueries)
    add_card(slide5, 0.5, 1.62, 5.9, 2.65, "1. COMPLEX MULTI-TABLE SQL JOINS", COLOR_CYAN)
    tb5_1 = slide5.shapes.add_textbox(Inches(0.62), Inches(2.02), Inches(5.66), Inches(2.15))
    tf5_1 = tb5_1.text_frame
    tf5_1.word_wrap = True
    tf5_1.margin_top = Inches(0); tf5_1.margin_left = Inches(0); tf5_1.margin_bottom = Inches(0)

    code_join = """-- 3-Way Inner Join: Live Flight Information Display (FIDS)
SELECT f.flight_no, a1.city AS Source, a2.city AS Destination,
       ac.model AS Aircraft, f.departure_time, f.fare
FROM Flight f
JOIN Airport a1 ON f.source_airport = a1.airport_id
JOIN Airport a2 ON f.destination_airport = a2.airport_id
JOIN Aircraft ac ON f.aircraft_id = ac.aircraft_id
ORDER BY f.departure_time ASC;

-- Left Outer Join: Fleet Utilization (Identifies Idle Aircraft)
SELECT ac.aircraft_id, ac.model, ac.capacity
FROM Aircraft ac
LEFT JOIN Flight f ON ac.aircraft_id = f.aircraft_id
WHERE f.flight_id IS NULL;"""
    p5_1 = tf5_1.paragraphs[0]
    p5_1.text = code_join
    p5_1.font.name = FONT_CODE
    p5_1.font.size = Pt(8.1)
    p5_1.font.color.rgb = COLOR_TEXT_LIGHT

    add_card(slide5, 0.5, 4.38, 5.9, 2.52, "2. CORRELATED & NESTED SUBQUERIES", COLOR_AMBER)
    tb5_2 = slide5.shapes.add_textbox(Inches(0.62), Inches(4.78), Inches(5.66), Inches(2.05))
    tf5_2 = tb5_2.text_frame
    tf5_2.word_wrap = True
    tf5_2.margin_top = Inches(0); tf5_2.margin_left = Inches(0); tf5_2.margin_bottom = Inches(0)

    code_sub = """-- Correlated Subquery: Flights With Fare Higher than Route Average
SELECT flight_no, fare, departure_time FROM Flight f1
WHERE fare > (SELECT AVG(fare) FROM Flight f2 
              WHERE f1.source_airport = f2.source_airport);

-- Subquery with EXISTS: Frequent Flyers with Premium Bookings
SELECT passenger_name, phone FROM Passenger p
WHERE EXISTS (
  SELECT 1 FROM Booking b JOIN Payment pay ON b.booking_id = pay.booking_id
  WHERE b.passenger_id = p.passenger_id AND pay.amount > 6500.00
);"""
    p5_2 = tf5_2.paragraphs[0]
    p5_2.text = code_sub
    p5_2.font.name = FONT_CODE
    p5_2.font.size = Pt(8.1)
    p5_2.font.color.rgb = COLOR_TEXT_LIGHT

    # Right Column: Card 3 (Analytic Views) & Card 4 (Query Execution & Testing)
    add_card(slide5, 6.7, 1.62, 6.133, 2.65, "3. PRE-COMPILED DATABASE VIEWS", COLOR_EMERALD)
    tb5_3 = slide5.shapes.add_textbox(Inches(6.82), Inches(2.02), Inches(5.89), Inches(2.15))
    tf5_3 = tb5_3.text_frame
    tf5_3.word_wrap = True
    tf5_3.margin_top = Inches(0); tf5_3.margin_left = Inches(0); tf5_3.margin_bottom = Inches(0)

    bullets5_3 = [
        ("Security Abstraction & Query Simplification Views:", ""),
        ("  • v_flight_schedule: ", "Decouples raw foreign keys into passenger-readable origin/destination cities, flight callsigns, and departure timestamps."),
        ("  • v_passenger_manifest: ", "Joins Passenger, Booking, and Flight for boarding gate agents without exposing sensitive billing data."),
        ("  • v_revenue_summary: ", "Aggregates route financial performance:"),
        ("    CREATE VIEW v_revenue_summary AS", ""),
        ("    SELECT f.flight_no, COUNT(b.booking_id) AS Total_Bookings, ", ""),
        ("           SUM(p.amount) AS Total_Revenue, AVG(p.amount) AS Avg_Yield", ""),
        ("    FROM Flight f JOIN Booking b ON f.flight_id = b.flight_id", ""),
        ("    JOIN Payment p ON b.booking_id = p.booking_id GROUP BY f.flight_no;", "")
    ]
    for i, (b_title, b_desc) in enumerate(bullets5_3):
        p = tf5_3.paragraphs[0] if i == 0 else tf5_3.add_paragraph()
        if b_title.startswith("    "):
            p.font.name = FONT_CODE
            p.font.size = Pt(7.8)
            p.font.color.rgb = COLOR_EMERALD
            p.text = b_title
            p.space_after = Pt(1)
        elif b_desc == "":
            p.font.size = Pt(9.2); p.font.bold = True; p.font.color.rgb = COLOR_EMERALD; p.text = b_title; p.space_after = Pt(2)
        else:
            p.font.size = Pt(9.2); p.font.name = FONT_BODY; p.space_after = Pt(2.5)
            r1 = p.add_run(); r1.text = ("• " if not b_title.startswith("  ") else "") + b_title; r1.font.bold = True; r1.font.color.rgb = COLOR_WHITE
            r2 = p.add_run(); r2.text = b_desc; r2.font.color.rgb = COLOR_TEXT_LIGHT

    add_card(slide5, 6.7, 4.38, 6.133, 2.52, "4. QUERY EXECUTION TESTING & PERFORMANCE", COLOR_PURPLE)
    tb5_4 = slide5.shapes.add_textbox(Inches(6.82), Inches(4.78), Inches(5.89), Inches(2.05))
    tf5_4 = tb5_4.text_frame
    tf5_4.word_wrap = True
    tf5_4.margin_top = Inches(0); tf5_4.margin_left = Inches(0); tf5_4.margin_bottom = Inches(0)

    bullets5_4 = [
        ("Sub-Millisecond Query Latency: ", "Average multi-table join execution verified at < 0.8 ms across indexed Primary and Foreign Key attributes."),
        ("Aggregate Operational Testing: ", "Successfully executed and verified SUM(amount), COUNT(booking_id), and AVG(fare) with HAVING COUNT(*) >= 2 groupings."),
        ("Set Operations Tested: ", "Executed UNION and EXCEPT queries to isolate routes with high passenger loads versus idle schedules."),
        ("Referential Validation: ", "100% data retrieval accuracy verified across all 43 passengers and 40 bookings with zero join dropouts or null dereferences.")
    ]
    for i, (b_title, b_desc) in enumerate(bullets5_4):
        p = tf5_4.paragraphs[0] if i == 0 else tf5_4.add_paragraph()
        p.font.size = Pt(9.2)
        p.font.name = FONT_BODY
        p.space_after = Pt(3)
        r1 = p.add_run(); r1.text = "• " + b_title; r1.font.bold = True; r1.font.color.rgb = COLOR_WHITE
        r2 = p.add_run(); r2.text = b_desc; r2.font.color.rgb = COLOR_TEXT_LIGHT

    # =========================================================================
    # SLIDE 6: MEMBER 5 – ARYA BAGADE
    # Voice AI, Programmable PL/SQL, Triggers & Full-Stack Applications
    # =========================================================================
    print("Building Slide 6: Member 5 – Arya Bagade...")
    slide6 = prs.slides.add_slide(blank_layout)
    add_slide_scaffolding(
        slide6, 6,
        "VOICE AI, PROGRAMMABLE PL/SQL & FULL-STACK INTERFACES",
        "Two-Way Web Speech AI • ACID Stored Procedures • Automated Triggers • Streamlit App & Aviation Portal",
        "MEMBER 5: ARYA BAGADE",
        COLOR_CORAL
    )

    # Left Column: Card 1 (Two-Way Voice AI) & Card 2 (Stored Procedures & Triggers)
    add_card(slide6, 0.5, 1.62, 5.9, 2.65, "1. TWO-WAY VOICE AI PIPELINE (WEB SPEECH API)", COLOR_CORAL)
    tb6_1 = slide6.shapes.add_textbox(Inches(0.62), Inches(2.02), Inches(5.66), Inches(2.15))
    tf6_1 = tb6_1.text_frame
    tf6_1.word_wrap = True
    tf6_1.margin_top = Inches(0); tf6_1.margin_left = Inches(0); tf6_1.margin_bottom = Inches(0)

    bullets6_1 = [
        ("Speech-to-Text (STT) Capture: ", "Microphone speech recognition using HTML5 Web Speech API with real-time waveform equalization and hands-free input."),
        ("Natural Language Query Engine: ", "Intelligent semantic parser mapping spoken queries into optimized 3NF SQL queries:"),
        ("  • 'Flights from Mumbai' ➔ ", "SELECT ... WHERE a1.city = 'Mumbai' ORDER BY departure_time"),
        ("  • 'Passengers on flight 301' ➔ ", "SELECT ... WHERE f.flight_id = 301 JOIN Booking b"),
        ("  • 'Show total revenue' ➔ ", "SELECT SUM(amount) FROM Payment WHERE payment_status = 'Paid'"),
        ("Text-to-Speech (TTS) Voice Synthesis: ", "Browser-native audio synthesizer delivering spoken output with customizable speech rate and audio replay.")
    ]
    for i, (b_title, b_desc) in enumerate(bullets6_1):
        p = tf6_1.paragraphs[0] if i == 0 else tf6_1.add_paragraph()
        p.font.size = Pt(9.1)
        p.font.name = FONT_BODY
        p.space_after = Pt(2.5)
        r1 = p.add_run(); r1.text = ("• " if not b_title.startswith("  ") else "") + b_title
        r1.font.bold = True; r1.font.color.rgb = COLOR_WHITE if not b_title.startswith("  ") else COLOR_CORAL
        r2 = p.add_run(); r2.text = b_desc; r2.font.color.rgb = COLOR_TEXT_LIGHT

    add_card(slide6, 0.5, 4.38, 5.9, 2.52, "2. PROGRAMMABLE PL/SQL: PROCEDURES & TRIGGERS", COLOR_AMBER)
    tb6_2 = slide6.shapes.add_textbox(Inches(0.62), Inches(4.78), Inches(5.66), Inches(2.05))
    tf6_2 = tb6_2.text_frame
    tf6_2.word_wrap = True
    tf6_2.margin_top = Inches(0); tf6_2.margin_left = Inches(0); tf6_2.margin_bottom = Inches(0)

    bullets6_2 = [
        ("sp_book_flight (Atomic ACID Transaction): ", "Checks seat availability to prevent double-booking; manages START TRANSACTION, creates Passenger, Booking, and Payment records with SAVEPOINT and ROLLBACK guarantees."),
        ("sp_reschedule_flight: ", "Executes controlled departure and arrival time updates."),
        ("trg_after_flight_update (SQL Audit Trigger): ", ""),
        ("  CREATE TRIGGER trg_after_flight_update AFTER UPDATE ON Flight", ""),
        ("  FOR EACH ROW BEGIN", ""),
        ("    INSERT INTO flight_audit (flight_id, operation_type, message, change_time)", ""),
        ("    VALUES (NEW.flight_id, 'RESCHEDULE', CONCAT('From: ', OLD.departure_time, ' To: ', NEW.departure_time), NOW());", ""),
        ("  END;", "")
    ]
    for i, (b_title, b_desc) in enumerate(bullets6_2):
        p = tf6_2.paragraphs[0] if i == 0 else tf6_2.add_paragraph()
        if b_title.startswith("  CREATE") or b_title.startswith("  FOR") or b_title.startswith("    INSERT") or b_title.startswith("    VALUES") or b_title.startswith("  END;"):
            p.font.name = FONT_CODE; p.font.size = Pt(7.8); p.font.color.rgb = COLOR_AMBER; p.text = b_title; p.space_after = Pt(1)
        elif b_desc == "":
            p.font.size = Pt(9.1); p.font.bold = True; p.font.color.rgb = COLOR_AMBER; p.text = b_title; p.space_after = Pt(2)
        else:
            p.font.size = Pt(9.1); p.font.name = FONT_BODY; p.space_after = Pt(2.5)
            r1 = p.add_run(); r1.text = "• " + b_title; r1.font.bold = True; r1.font.color.rgb = COLOR_WHITE
            r2 = p.add_run(); r2.text = b_desc; r2.font.color.rgb = COLOR_TEXT_LIGHT

    # Right Column: Card 3 (Application Interfaces) & Card 4 (End-to-End Workflow)
    add_card(slide6, 6.7, 1.62, 6.133, 2.65, "3. STREAMLIT APPLICATION & AVIATION WEB PORTAL", COLOR_CYAN)
    tb6_3 = slide6.shapes.add_textbox(Inches(6.82), Inches(2.02), Inches(5.89), Inches(2.15))
    tf6_3 = tb6_3.text_frame
    tf6_3.word_wrap = True
    tf6_3.margin_top = Inches(0); tf6_3.margin_left = Inches(0); tf6_3.margin_bottom = Inches(0)

    bullets6_3 = [
        ("Streamlit Web Dashboard (app.py): ", "Interactive airport management suite featuring:"),
        ("  • Mobile Voice Search Console: ", "Pulsing coral-pink mic orb with concentric sound waves, floating particles, and status bar (Wi-Fi, 12:00)."),
        ("  • Karaoke / Lyrics-Style Spoken Output: ", "Real-time spoken response presented line-by-line with glowing highlights and bouncing equalizer soundwaves."),
        ("  • Quick Voice Option Chips: ", "One-click chips for Flights from Mumbai, Inbound Delhi, Manifest AI101, and Route Revenue."),
        ("Modern Aviation Web Portal (web_portal/): ", "High-performance SPA with glassmorphism cockpit UI, live animated radar airspace, and custom SQL console."),
        ("Dual-Backend Architecture: ", "Zero-setup engine connecting to live MySQL server with automatic seamless fallback to standalone SQLite (AirportDB.sql).")
    ]
    for i, (b_title, b_desc) in enumerate(bullets6_3):
        p = tf6_3.paragraphs[0] if i == 0 else tf6_3.add_paragraph()
        p.font.size = Pt(9.1)
        p.font.name = FONT_BODY
        p.space_after = Pt(2.5)
        r1 = p.add_run(); r1.text = ("• " if not b_title.startswith("  ") else "") + b_title
        r1.font.bold = True; r1.font.color.rgb = COLOR_WHITE if not b_title.startswith("  ") else COLOR_CYAN
        r2 = p.add_run(); r2.text = b_desc; r2.font.color.rgb = COLOR_TEXT_LIGHT

    add_card(slide6, 6.7, 4.38, 6.133, 2.52, "4. END-TO-END VOICE-TO-DATABASE WORKFLOW PIPELINE", COLOR_EMERALD)
    tb6_4 = slide6.shapes.add_textbox(Inches(6.82), Inches(4.78), Inches(5.89), Inches(2.05))
    tf6_4 = tb6_4.text_frame
    tf6_4.word_wrap = True
    tf6_4.margin_top = Inches(0); tf6_4.margin_left = Inches(0); tf6_4.margin_bottom = Inches(0)

    bullets6_4 = [
        ("Visual Architectural Pipeline Flow:", ""),
        ("  [User Speaks into Mic: 'Flights from Mumbai']", ""),
        ("        ↓  (HTML5 Web Speech API Microphone Capture)", ""),
        ("  [Voice Query Engine: Intent Recognition & Parameter Extraction]", ""),
        ("        ↓  (Generates 3NF Multi-Table SQL Join Query)", ""),
        ("  [Relational DBMS Core: MySQL / SQLite Engine Execution]", ""),
        ("        ↓  (Sub-Millisecond Query Resolution)", ""),
        ("  ┌───────────────────────────────────┴───────────────────────────────────┐", ""),
        ("  ▼                                                                       ▼", ""),
        ("  [Interactive Sortable Data Table]             [Synchronized Lyrics Spoken Audio (TTS)]", "")
    ]
    for i, (line, _) in enumerate(bullets6_4):
        p = tf6_4.paragraphs[0] if i == 0 else tf6_4.add_paragraph()
        if line.startswith("Visual"):
            p.font.size = Pt(9.2); p.font.bold = True; p.font.color.rgb = COLOR_EMERALD; p.text = line; p.space_after = Pt(2)
        else:
            p.font.name = FONT_CODE; p.font.size = Pt(7.8); p.font.color.rgb = COLOR_TEXT_LIGHT; p.text = line; p.space_after = Pt(1)

    # =========================================================================
    # SLIDE 7: EXACT ORIGINAL THANK YOU SLIDE
    # =========================================================================
    print("Building Slide 7: Exact Original Thank You Slide...")
    slide7 = prs.slides.add_slide(blank_layout)
    if os.path.exists(exact_slide_7_path):
        slide7.shapes.add_picture(exact_slide_7_path, Inches(0), Inches(0), width=Inches(13.333), height=Inches(7.5))
    else:
        print("Warning: exact_slide_7.jpg not found!")

    # Save to both paths
    prs.save(PPTX_7SLIDES_PATH)
    prs.save(PPTX_PATH)
    print(f"Successfully generated 7-slide deck at:\n1. {PPTX_7SLIDES_PATH}\n2. {PPTX_PATH}")

if __name__ == "__main__":
    create_deck()
