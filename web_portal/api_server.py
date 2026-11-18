"""
Lightweight API & Web Portal Server for AERO-NEXUS
Runs on Python standard library (http.server) with optional FastAPI/Flask support.
Allows users to launch the advanced frontend website with a single command:
    python web_portal/api_server.py
"""

import os
import sys
import json
import http.server
import socketserver
import urllib.parse

# Add parent directory to sys.path to access db_manager and syllabus_engine
PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PARENT_DIR)

import db_manager
import voice_query_engine
import syllabus_engine

PORT = 8080
WEB_DIR = os.path.dirname(os.path.abspath(__file__))


class AirportRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def do_POST(self):
        # API endpoints
        parsed = urllib.parse.urlparse(self.path)
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)

        try:
            req_json = json.loads(post_data.decode('utf-8')) if post_data else {}
        except Exception:
            req_json = {}

        if parsed.path == '/api/voice-query':
            self.handle_voice_query_api(req_json)
        elif parsed.path == '/api/execute-sql':
            self.handle_sql_api(req_json)
        elif parsed.path == '/api/syllabus':
            self.handle_syllabus_api(req_json)
        else:
            self.send_error(404, "Endpoint not found")

    def handle_voice_query_api(self, req_json):
        query = req_json.get('query', 'Flights from Mumbai')
        conn, is_mysql, _ = db_manager.get_db_connection(force_sqlite=True)
        res = voice_query_engine.process_query(query, conn, is_mysql=is_mysql)
        
        # Convert df to records
        df_records = []
        if res["dataframe"] is not None and not res["dataframe"].empty:
            df_records = res["dataframe"].to_dict(orient="records")

        response = {
            "category": res["category"],
            "sql": res["sql"],
            "spoken_text": res["spoken_text"],
            "summary": res["summary"],
            "records": df_records,
            "status": res["status"]
        }
        self.send_json_response(response)

    def handle_sql_api(self, req_json):
        query = req_json.get('sql', 'SELECT * FROM flight LIMIT 5;')
        conn, is_mysql, _ = db_manager.get_db_connection(force_sqlite=True)
        df, err = db_manager.execute_query(conn, query, is_mysql=is_mysql)
        
        if err:
            self.send_json_response({"error": err, "records": []}, status=400)
        else:
            self.send_json_response({"records": df.to_dict(orient="records"), "count": len(df)})

    def handle_syllabus_api(self, req_json):
        unit = req_json.get('unit', 'all')
        data = {
            "unit1": syllabus_engine.Unit1DataModeling.get_integrity_constraints(),
            "unit4": syllabus_engine.Unit4NormalizationAndStorage.get_normalization_breakdown(),
            "unit5": syllabus_engine.Unit5TransactionsAndConcurrency.test_conflict_serializability(),
            "unit6": syllabus_engine.Unit6NoSQLAndDataWarehouse.get_nosql_multi_model_representations()
        }
        self.send_json_response(data)

    def send_json_response(self, data, status=200):
        body = json.dumps(data).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()


def start_server():
    os.chdir(WEB_DIR)
    with socketserver.TCPServer(("", PORT), AirportRequestHandler) as httpd:
        print(f"============================================================")
        print(f"✈️ AERO-NEXUS Airport Operations Web Portal is Running!")
        print(f"👉 Local URL: http://localhost:{PORT}")
        print(f"Serving files from: {WEB_DIR}")
        print(f"Press Ctrl+C to stop the server.")
        print(f"============================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down portal server...")
            httpd.server_close()


if __name__ == '__main__':
    start_server()
