"""Local dev server: serves the UI and POST /api/events (builds the email, does not send it).
Later, the Azure Function replaces this and sends through Azure Communication Services."""
import json
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from email_logic import build_email

ROOT = Path(__file__).parent


class Handler(BaseHTTPRequestHandler):
    def reply(self, code, body, ctype="application/json"):
        data = body if isinstance(body, bytes) else body.encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self.reply(200, (ROOT / "ui" / "index.html").read_bytes(), "text/html; charset=utf-8")
        else:
            self.reply(404, json.dumps({"error": "not found"}))

    def do_POST(self):
        if self.path != "/api/events":
            return self.reply(404, json.dumps({"error": "not found"}))
        try:
            size = int(self.headers.get("Content-Length", 0))
            event = json.loads(self.rfile.read(size) or b"{}")
            self.reply(200, json.dumps(build_email(event)))
        except Exception as error:
            logging.error("ERROR handling event: %s", error)
            self.reply(400, json.dumps({"error": str(error)}))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("Open http://localhost:8000")
    HTTPServer(("localhost", 8000), Handler).serve_forever()