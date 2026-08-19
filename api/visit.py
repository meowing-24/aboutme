from http.server import BaseHTTPRequestHandler
import json
import requests
import os
from datetime import datetime

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")


class handler(BaseHTTPRequestHandler):

    def do_POST(self):

        length = int(self.headers.get("content-length", 0))
        raw_body = self.rfile.read(length)

        try:
            body = json.loads(raw_body.decode())
        except:
            body = {}

        ip = self.headers.get(
            "x-forwarded-for",
            self.client_address[0]
        )

        user_agent = self.headers.get(
            "user-agent",
            "Unknown"
        )

        event = body.get("event", "visit")

        message = (
            f"Event: {event}\n"
            f"IP: {ip}\n"
            f"User-Agent: {user_agent}\n"
            f"Time: {datetime.utcnow().isoformat()} UTC\n"
        )

        if event == "location":
            lat = body.get("latitude")
            lon = body.get("longitude")

            message += (
                f"Latitude: {lat}\n"
                f"Longitude: {lon}\n"
            )

        if WEBHOOK_URL:
            requests.post(
                WEBHOOK_URL,
                json={"content": message},
                timeout=5
            )

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")
