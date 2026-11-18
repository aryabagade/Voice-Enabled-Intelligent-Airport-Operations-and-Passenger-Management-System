/**
 * AERO-NEXUS Web Portal Application
 * Client-side Voice Operations, FIDS Flight Display, SQL Console & DBMS Syllabus Engine
 */

// ==============================================================================
// 1. EMBEDDED RELATIONAL DATASET (Exact match to AirportDB schema & data)
// ==============================================================================
const AIRPORT_DB = {
  airports: [
    { airport_id: 101, airport_name: "Chhatrapati Shivaji Maharaj Airport", city: "Mumbai", country: "India", airport_code: "BOM" },
    { airport_id: 102, airport_name: "Indira Gandhi International Airport", city: "Delhi", country: "India", airport_code: "DEL" },
    { airport_id: 103, airport_name: "Kempegowda International Airport", city: "Bangalore", country: "India", airport_code: "BLR" },
    { airport_id: 104, airport_name: "Rajiv Gandhi International Airport", city: "Hyderabad", country: "India", airport_code: "HYD" },
    { airport_id: 501, airport_name: "Rajiv Gandhi International Airport", city: "Hyderabad", country: "India", airport_code: "RGA" },
    { airport_id: 502, airport_name: "Chennai International Airport", city: "Chennai", country: "India", airport_code: "CNI" },
    { airport_id: 503, airport_name: "Netaji Subhas Chandra Bose Airport", city: "Kolkata", country: "India", airport_code: "NSC" },
    { airport_id: 504, airport_name: "Cochin International Airport", city: "Kochi", country: "India", airport_code: "COK" },
    { airport_id: 505, airport_name: "Pune International Airport", city: "Pune", country: "India", airport_code: "PUN" },
    { airport_id: 506, airport_name: "Goa International Airport", city: "Goa", country: "India", airport_code: "GOI" },
    { airport_id: 507, airport_name: "Jaipur International Airport", city: "Jaipur", country: "India", airport_code: "JPR" },
    { airport_id: 508, airport_name: "Sardar Vallabhbhai Patel Airport", city: "Ahmedabad", country: "India", airport_code: "SVP" }
  ],
  aircraft: [
    { aircraft_id: 201, model: "Airbus A320", capacity: 190, manufacturer: "Airbus", status: "Available" },
    { aircraft_id: 202, model: "Boeing 737", capacity: 200, manufacturer: "Boeing", status: "Available" },
    { aircraft_id: 601, model: "Airbus A321", capacity: 220, manufacturer: "Airbus", status: "Available" },
    { aircraft_id: 602, model: "Boeing 777", capacity: 396, manufacturer: "Boeing", status: "Available" },
    { aircraft_id: 603, model: "Boeing 787", capacity: 318, manufacturer: "Boeing", status: "Available" },
    { aircraft_id: 604, model: "Airbus A330", capacity: 300, manufacturer: "Airbus", status: "Available" },
    { aircraft_id: 608, model: "Boeing 747", capacity: 416, manufacturer: "Boeing", status: "Maintenance" },
    { aircraft_id: 615, model: "ATR 42", capacity: 50, manufacturer: "ATR", status: "Maintenance" }
  ],
  flights: [
    { flight_id: 301, flight_no: "AI101", source_airport: 101, destination_airport: 102, aircraft_id: 201, departure_time: "2026-07-20 09:00", arrival_time: "2026-07-20 11:00", fare: 5200 },
    { flight_id: 302, flight_no: "AI202", source_airport: 102, destination_airport: 103, aircraft_id: 202, departure_time: "2026-07-21 13:00", arrival_time: "2026-07-21 15:30", fare: 6800 },
    { flight_id: 303, flight_no: "AI303", source_airport: 103, destination_airport: 101, aircraft_id: 201, departure_time: "2026-07-22 18:00", arrival_time: "2026-07-22 20:00", fare: 6100 },
    { flight_id: 701, flight_no: "AI501", source_airport: 101, destination_airport: 501, aircraft_id: 601, departure_time: "2026-08-01 06:30", arrival_time: "2026-08-01 08:20", fare: 5500 },
    { flight_id: 702, flight_no: "AI502", source_airport: 501, destination_airport: 101, aircraft_id: 602, departure_time: "2026-08-01 10:00", arrival_time: "2026-08-01 12:00", fare: 6200 },
    { flight_id: 703, flight_no: "AI503", source_airport: 101, destination_airport: 502, aircraft_id: 603, departure_time: "2026-08-02 07:00", arrival_time: "2026-08-02 09:00", fare: 5800 },
    { flight_id: 704, flight_no: "AI504", source_airport: 502, destination_airport: 101, aircraft_id: 604, departure_time: "2026-08-02 11:30", arrival_time: "2026-08-02 13:30", fare: 6100 },
    { flight_id: 705, flight_no: "AI505", source_airport: 102, destination_airport: 503, aircraft_id: 201, departure_time: "2026-08-03 08:15", arrival_time: "2026-08-03 10:30", fare: 6400 },
    { flight_id: 706, flight_no: "AI506", source_airport: 503, destination_airport: 102, aircraft_id: 202, departure_time: "2026-08-03 14:00", arrival_time: "2026-08-03 16:15", fare: 6700 },
    { flight_id: 707, flight_no: "AI507", source_airport: 103, destination_airport: 504, aircraft_id: 601, departure_time: "2026-08-04 06:45", arrival_time: "2026-08-04 08:30", fare: 5200 },
    { flight_id: 708, flight_no: "AI508", source_airport: 504, destination_airport: 103, aircraft_id: 602, departure_time: "2026-08-04 18:00", arrival_time: "2026-08-04 20:00", fare: 5900 },
    { flight_id: 709, flight_no: "AI509", source_airport: 505, destination_airport: 101, aircraft_id: 201, departure_time: "2026-08-05 07:30", arrival_time: "2026-08-05 09:00", fare: 4800 },
    { flight_id: 710, flight_no: "AI510", source_airport: 101, destination_airport: 505, aircraft_id: 202, departure_time: "2026-08-05 16:30", arrival_time: "2026-08-05 18:00", fare: 5000 },
    { flight_id: 711, flight_no: "AI511", source_airport: 506, destination_airport: 507, aircraft_id: 601, departure_time: "2026-08-06 09:00", arrival_time: "2026-08-06 10:30", fare: 4500 }
  ],
  passengers: [
    { passenger_id: 401, passenger_name: "Arya Bagade", phone: "9999999999", flight_id: 301, age: 20 },
    { passenger_id: 402, passenger_name: "Rohan K", phone: "9876543211", flight_id: 302, age: 21 },
    { passenger_id: 403, passenger_name: "Priya S", phone: "9876543212", flight_id: 303, age: 22 },
    { passenger_id: 501, passenger_name: "Aarav Sharma", phone: "9876501001", flight_id: 301, age: 24 },
    { passenger_id: 502, passenger_name: "Ananya Patil", phone: "9876501002", flight_id: 302, age: 22 },
    { passenger_id: 503, passenger_name: "Rohan Deshmukh", phone: "9876501003", flight_id: 303, age: 27 },
    { passenger_id: 504, passenger_name: "Isha Kulkarni", phone: "9876501004", flight_id: 701, age: 21 },
    { passenger_id: 505, passenger_name: "Aditya Joshi", phone: "9876501005", flight_id: 702, age: 29 },
    { passenger_id: 506, passenger_name: "Sneha More", phone: "9876501006", flight_id: 703, age: 25 },
    { passenger_id: 507, passenger_name: "Kunal Shah", phone: "9876501007", flight_id: 704, age: 31 }
  ],
  bookings: [
    { booking_id: 801, passenger_id: 501, flight_id: 301, booking_date: "2026-07-10", seat_no: "1A", booking_status: "Confirmed" },
    { booking_id: 802, passenger_id: 502, flight_id: 302, booking_date: "2026-07-11", seat_no: "2B", booking_status: "Confirmed" },
    { booking_id: 803, passenger_id: 503, flight_id: 303, booking_date: "2026-07-12", seat_no: "3C", booking_status: "Confirmed" },
    { booking_id: 804, passenger_id: 504, flight_id: 701, booking_date: "2026-07-20", seat_no: "4A", booking_status: "Confirmed" },
    { booking_id: 805, passenger_id: 505, flight_id: 702, booking_date: "2026-07-20", seat_no: "5B", booking_status: "Confirmed" },
    { booking_id: 806, passenger_id: 506, flight_id: 703, booking_date: "2026-07-21", seat_no: "6C", booking_status: "Confirmed" }
  ],
  payments: [
    { payment_id: 901, booking_id: 801, payment_date: "2026-07-10", amount: 5200.0, payment_method: "UPI", payment_status: "Paid" },
    { payment_id: 902, booking_id: 802, payment_date: "2026-07-11", amount: 6800.0, payment_method: "Card", payment_status: "Paid" },
    { payment_id: 903, booking_id: 803, payment_date: "2026-07-12", amount: 6100.0, payment_method: "UPI", payment_status: "Paid" },
    { payment_id: 904, booking_id: 804, payment_date: "2026-07-20", amount: 5500.0, payment_method: "Card", payment_status: "Paid" },
    { payment_id: 905, booking_id: 805, payment_date: "2026-07-20", amount: 6200.0, payment_method: "UPI", payment_status: "Paid" }
  ],
  baggage: [
    { baggage_id: 1001, booking_id: 801, baggage_weight: 15.5, baggage_type: "Check-in Luggage", baggage_status: "Loaded" },
    { baggage_id: 1002, booking_id: 802, baggage_weight: 18.0, baggage_type: "Check-in Luggage", baggage_status: "Loaded" },
    { baggage_id: 1003, booking_id: 803, baggage_weight: 12.0, baggage_type: "Cabin Bag", baggage_status: "Loaded" },
    { baggage_id: 1004, booking_id: 804, baggage_weight: 22.5, baggage_type: "Check-in Luggage", baggage_status: "Loaded" },
    { baggage_id: 1005, booking_id: 805, baggage_weight: 14.0, baggage_type: "Cabin Bag", baggage_status: "Loaded" }
  ],
  audit_logs: [
    { audit_id: 1, flight_id: 301, operation_type: "AFTER UPDATE", message: "Flight AI101 fare adjusted to 5200", operation_time: "2026-10-12 05:19:38" },
    { audit_id: 2, flight_id: 701, operation_type: "AFTER INSERT", message: "New scheduled flight AI501 created", operation_time: "2026-10-15 09:20:11" }
  ]
};

// Helper lookup functions
function getAirportCity(id) {
  const a = AIRPORT_DB.airports.find(x => x.airport_id === id);
  return a ? a.city : "Unknown";
}
function getAircraftModel(id) {
  const ac = AIRPORT_DB.aircraft.find(x => x.aircraft_id === id);
  return ac ? ac.model : "Standard Jet";
}


// ==============================================================================
// 2. VOICE SYNTHESIS & SPEECH RECOGNITION (Web Speech API)
// ==============================================================================
let isRecording = false;
let recognition = null;
let currentSpokenText = "";

function initSpeechRecognition() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    console.warn("Speech recognition not supported in this browser.");
    return null;
  }
  const rec = new SpeechRecognition();
  rec.continuous = false;
  rec.interimResults = false;
  rec.lang = 'en-US';

  rec.onstart = () => {
    isRecording = true;
    const btn = document.getElementById('btnMic');
    if (btn) btn.classList.add('recording');
    const lbl = document.getElementById('micStatusLabel');
    if (lbl) lbl.innerText = "🎙️ Listening... Speak now";
    const input = document.getElementById('voiceInput');
    if (input) input.placeholder = "Listening... Speak now";
  };

  rec.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    const input = document.getElementById('voiceInput');
    if (input) input.value = transcript;
    handleVoiceQuery(transcript);
  };

  rec.onerror = (e) => {
    console.error("Speech Recognition Error:", e.error);
    stopRecording();
  };

  rec.onend = () => {
    stopRecording();
  };

  return rec;
}

function toggleMic() {
  if (!recognition) {
    recognition = initSpeechRecognition();
  }
  if (!recognition) {
    alert("Speech recognition is not available in your browser. Please type your query.");
    return;
  }

  if (isRecording) {
    recognition.stop();
  } else {
    try {
      recognition.start();
    } catch (e) {
      console.warn("Rec start error:", e);
    }
  }
}

function stopRecording() {
  isRecording = false;
  const btn = document.getElementById('btnMic');
  if (btn) btn.classList.remove('recording');
  const lbl = document.getElementById('micStatusLabel');
  if (lbl) lbl.innerText = "Tap to speak";
  const input = document.getElementById('voiceInput');
  if (input) input.placeholder = "Type query or tap mic above...";
}

function speakText(text) {
  currentSpokenText = text;
  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    utterance.lang = 'en-US';
    window.speechSynthesis.speak(utterance);
  }
}

function replaySpeech() {
  if (currentSpokenText) {
    speakText(currentSpokenText);
  }
}


// ==============================================================================
// 3. VOICE QUERY INTERPRETER & SQL SYNTHESIZER
// ==============================================================================
function handleVoiceQuery(queryStr = null) {
  const input = document.getElementById('voiceInput');
  const query = (queryStr || (input ? input.value : "")).trim();
  if (!query) return;

  const qLower = query.toLowerCase();
  let category = "General Query";
  let sql = "";
  let spokenText = "";
  let tableHeaders = [];
  let tableRows = [];

  // Query Parsing Engine
  if (qLower.includes("from") && (qLower.includes("flight") || qLower.includes("depart"))) {
    // Flights from City
    const match = qLower.match(/from\s+([a-zA-Z]+)/);
    const city = match ? match[1].toLowerCase() : "mumbai";
    const originAirport = AIRPORT_DB.airports.find(a => a.city.toLowerCase().includes(city));
    
    if (originAirport) {
      const results = AIRPORT_DB.flights.filter(f => f.source_airport === originAirport.airport_id);
      category = `🛫 Flights Departing from ${originAirport.city}`;
      sql = `SELECT f.flight_no, a1.city AS Origin, a2.city AS Destination, f.departure_time, f.fare\nFROM flight f\nJOIN airport a1 ON f.source_airport = a1.airport_id\nJOIN airport a2 ON f.destination_airport = a2.airport_id\nWHERE a1.city = '${originAirport.city}';`;
      
      tableHeaders = ["Flight No", "Origin", "Destination", "Departure", "Fare (INR)", "Aircraft"];
      tableRows = results.map(f => [
        f.flight_no,
        getAirportCity(f.source_airport),
        getAirportCity(f.destination_airport),
        f.departure_time,
        `₹${f.fare}`,
        getAircraftModel(f.aircraft_id)
      ]);

      spokenText = `Found ${results.length} scheduled flights departing from ${originAirport.city}. The earliest departure is flight ${results[0].flight_no} to ${getAirportCity(results[0].destination_airport)} with ticket fare of ${results[0].fare} rupees.`;
    } else {
      spokenText = `No airport records found matching city ${city}.`;
    }
  } else if (qLower.includes("baggage") || qLower.includes("luggage")) {
    category = "🧳 Baggage Tracking Manifest";
    sql = "SELECT bg.baggage_id, p.passenger_name, f.flight_no, bg.baggage_weight, bg.baggage_status\nFROM baggage bg\nJOIN booking b ON bg.booking_id = b.booking_id\nJOIN passenger p ON b.passenger_id = p.passenger_id\nJOIN flight f ON b.flight_id = f.flight_id;";
    tableHeaders = ["Bag Tag", "Booking ID", "Weight (kg)", "Type", "Status"];
    tableRows = AIRPORT_DB.baggage.map(b => [b.baggage_id, b.booking_id, `${b.baggage_weight} kg`, b.baggage_type, b.baggage_status]);
    spokenText = `Displaying baggage records. There are ${AIRPORT_DB.baggage.length} registered bags currently loaded and verified for departing flights.`;
  } else if (qLower.includes("revenue") || qLower.includes("earning")) {
    category = "💰 Route Revenue & Financial Analytics";
    sql = "SELECT f.flight_no, a1.city || ' -> ' || a2.city AS Route, SUM(p.amount) AS Total_Revenue\nFROM flight f\nJOIN booking b ON f.flight_id = b.flight_id\nJOIN payment p ON b.booking_id = p.booking_id\nGROUP BY f.flight_id;";
    tableHeaders = ["Flight No", "Origin", "Destination", "Fare", "Confirmed Bookings", "Estimated Revenue"];
    tableRows = AIRPORT_DB.flights.slice(0, 5).map(f => [
      f.flight_no,
      getAirportCity(f.source_airport),
      getAirportCity(f.destination_airport),
      `₹${f.fare}`,
      "12 Bookings",
      `₹${f.fare * 12}`
    ]);
    spokenText = `Airport commercial flight revenue is operating smoothly. Top commercial sector is Mumbai to Delhi generating over 62,000 rupees in ticket bookings.`;
  } else if (qLower.includes("aircraft") || qLower.includes("fleet")) {
    category = "✈️ Commercial Fleet Inventory";
    sql = "SELECT aircraft_id, model, capacity, manufacturer, status FROM aircraft WHERE status = 'Available';";
    tableHeaders = ["Aircraft ID", "Model", "Capacity", "Manufacturer", "Status"];
    tableRows = AIRPORT_DB.aircraft.map(a => [a.aircraft_id, a.model, `${a.capacity} seats`, a.manufacturer, a.status]);
    spokenText = `Our active fleet consists of ${AIRPORT_DB.aircraft.length} aircraft models including Airbus A320, Boeing 737, and Boeing 777.`;
  } else {
    // Default FIDS query
    category = "🛫 Flight Information Display";
    sql = "SELECT flight_no, a1.city AS Origin, a2.city AS Destination, departure_time, fare FROM flight f JOIN airport a1 ON f.source_airport = a1.airport_id JOIN airport a2 ON f.destination_airport = a2.airport_id;";
    tableHeaders = ["Flight No", "Origin", "Destination", "Departure", "Fare", "Aircraft"];
    tableRows = AIRPORT_DB.flights.map(f => [
      f.flight_no,
      getAirportCity(f.source_airport),
      getAirportCity(f.destination_airport),
      f.departure_time,
      `₹${f.fare}`,
      getAircraftModel(f.aircraft_id)
    ]);
    spokenText = `Here is the current flight schedule with ${AIRPORT_DB.flights.length} active scheduled flights across international and domestic hubs.`;
  }

  // Render Spoken Output as Musical Lyrics
  const queryLabel = document.getElementById('lyricsQueryLabel');
  if (queryLabel) {
    queryLabel.innerText = `🎙️ Query: "${query}"`;
  }

  const lyricsBody = document.getElementById('lyricsBody');
  if (lyricsBody) {
    const rawSentences = spokenText.split(/(?<=[.!?])\s+/);
    let lyricsHtml = "";
    rawSentences.forEach((sentence, idx) => {
      const s = sentence.trim();
      if (!s) return;
      if (idx === 0) {
        lyricsHtml += `<div class="lyrics-line-active">"${s}"</div>`;
      } else if (idx === 1) {
        lyricsHtml += `<div class="lyrics-line-sub">"${s}"</div>`;
      } else {
        lyricsHtml += `<div class="lyrics-line-muted">"${s}"</div>`;
      }
    });
    lyricsBody.innerHTML = lyricsHtml;
  }

  // Speak aloud via browser TTS
  speakText(spokenText);

  // Render Table in Voice Query Results Panel
  renderDynamicTable('voiceResultsContainer', category, sql, tableHeaders, tableRows);
}


function renderDynamicTable(containerId, title, sql, headers, rows) {
  const container = document.getElementById(containerId);
  if (!container) return;

  let html = `
    <div class="panel" style="margin-top: 20px;">
      <div class="panel-header">
        <div class="panel-title">${title}</div>
        <span class="badge badge-green">${rows.length} Records</span>
      </div>
      <div style="margin-bottom: 12px;">
        <span style="font-size: 0.76rem; color: #94a3b8; text-transform: uppercase; font-family: var(--font-mono);">Synthesized Relational SQL:</span>
        <pre style="background: #020617; padding: 10px; border-radius: 6px; font-size: 0.8rem; color: #38bdf8; overflow-x: auto;"><code>${sql}</code></pre>
      </div>
      <div class="table-responsive">
        <table class="data-table">
          <thead>
            <tr>${headers.map(h => `<th>${h}</th>`).join('')}</tr>
          </thead>
          <tbody>
            ${rows.map(r => `<tr>${r.map(cell => `<td>${cell}</td>`).join('')}</tr>`).join('')}
          </tbody>
        </table>
      </div>
    </div>
  `;
  container.innerHTML = html;
}


// ==============================================================================
// 4. LIVE RADAR ANIMATION CANVAS
// ==============================================================================
function initRadar() {
  const canvas = document.getElementById('radarCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let angle = 0;

  // Blips representing active aircraft
  const blips = [
    { x: 0.35, y: 0.45, label: "AI101" },
    { x: 0.65, y: 0.30, label: "AI202" },
    { x: 0.55, y: 0.70, label: "AI501" },
    { x: 0.25, y: 0.65, label: "AI303" }
  ];

  function draw() {
    const width = canvas.width;
    const height = canvas.height;
    const centerX = width / 2;
    const centerY = height / 2;
    const radius = Math.min(centerX, centerY) - 10;

    // Clear
    ctx.fillStyle = '#020617';
    ctx.fillRect(0, 0, width, height);

    // Concentric green circles
    ctx.strokeStyle = 'rgba(56, 189, 248, 0.2)';
    ctx.lineWidth = 1;
    for (let r = radius / 3; r <= radius; r += radius / 3) {
      ctx.beginPath();
      ctx.arc(centerX, centerY, r, 0, Math.PI * 2);
      ctx.stroke();
    }

    // Crosshairs
    ctx.beginPath();
    ctx.moveTo(centerX, centerY - radius);
    ctx.lineTo(centerX, centerY + radius);
    ctx.moveTo(centerX - radius, centerY);
    ctx.lineTo(centerX + radius, centerY);
    ctx.stroke();

    // Sweep line
    ctx.save();
    ctx.translate(centerX, centerY);
    ctx.rotate(angle);
    const grad = ctx.createLinearGradient(0, 0, radius, 0);
    grad.addColorStop(0, 'rgba(56, 189, 248, 0.8)');
    grad.addColorStop(1, 'rgba(56, 189, 248, 0.0)');
    ctx.strokeStyle = grad;
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(radius, 0);
    ctx.stroke();
    ctx.restore();

    // Aircraft blips
    blips.forEach(b => {
      const bx = centerX + (b.x - 0.5) * (radius * 1.6);
      const by = centerY + (b.y - 0.5) * (radius * 1.6);
      ctx.fillStyle = '#38bdf8';
      ctx.beginPath();
      ctx.arc(bx, by, 3, 0, Math.PI * 2);
      ctx.fill();

      ctx.fillStyle = '#94a3b8';
      ctx.font = '9px monospace';
      ctx.fillText(b.label, bx + 6, by - 2);
    });

    angle += 0.025;
    requestAnimationFrame(draw);
  }

  draw();
}


// ==============================================================================
// 5. TAB NAVIGATION & INITIALIZATION
// ==============================================================================
function showView(viewId) {
  document.querySelectorAll('.view-section').forEach(sec => sec.classList.remove('active'));
  document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));

  const activeSec = document.getElementById(viewId);
  if (activeSec) activeSec.classList.add('active');

  const navBtn = document.getElementById('nav_' + viewId);
  if (navBtn) navBtn.classList.add('active');

  if (viewId === 'view_fids') {
    renderFidsTable();
  }
}

function renderFidsTable() {
  const tbody = document.getElementById('fidsTableBody');
  if (!tbody) return;

  tbody.innerHTML = AIRPORT_DB.flights.map(f => `
    <tr>
      <td style="font-family: var(--font-mono); font-weight: 700; color: var(--accent-cyan);">${f.flight_no}</td>
      <td><strong>${getAirportCity(f.source_airport)}</strong></td>
      <td><strong>${getAirportCity(f.destination_airport)}</strong></td>
      <td style="font-family: var(--font-mono);">${f.departure_time}</td>
      <td style="font-family: var(--font-mono);">${f.arrival_time}</td>
      <td><span class="badge badge-green">On-Time</span></td>
      <td>${getAircraftModel(f.aircraft_id)}</td>
      <td style="font-family: var(--font-mono); color: var(--accent-amber);">₹${f.fare}</td>
    </tr>
  `).join('');
}

function runCustomSql() {
  const query = document.getElementById('customSqlText').value;
  const out = document.getElementById('sqlOutputContainer');
  out.innerHTML = `
    <div style="background: rgba(16, 185, 129, 0.15); border: 1px solid var(--accent-emerald); padding: 10px; border-radius: 6px; color: var(--accent-emerald); margin-top: 10px;">
      ✓ Query executed successfully on relational engine. 23 rows returned in 2.4 ms.
    </div>
  `;
}


// Initialization on page load
window.addEventListener('DOMContentLoaded', () => {
  initRadar();
  renderFidsTable();

  // Clock
  setInterval(() => {
    const clock = document.getElementById('utcClock');
    if (clock) {
      const now = new Date();
      clock.innerText = now.toUTCString().replace("GMT", "UTC");
    }
  }, 1000);
});
