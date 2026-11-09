#!/usr/bin/env python3
"""HTTP server for the individual card viewer."""

import json
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from .mtg_card_search import fetch_card_by_name, fetch_card_by_set_number, search_cards_by_name


HOST = "127.0.0.1"
PORT = 0  # Use any available port


class CardViewerHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the card viewer."""
    
    page_path = Path(__file__).parent.parent.parent / "mtg_card_viewer.html"
    
    def do_GET(self):
        """Handle GET requests."""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        if path == "/" or path == "":
            self.serve_html()
        elif path == "/api/card/search":
            self.handle_card_search(parsed_url)
        elif path == "/api/card/set":
            self.handle_card_by_set(parsed_url)
        elif path == "/api/search":
            self.handle_search(parsed_url)
        else:
            self.send_error(404)
    
    def serve_html(self):
        """Serve the HTML page."""
        try:
            html_content = self.page_path.read_text(encoding="utf-8")
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.send_header("Content-length", len(html_content.encode("utf-8")))
            self.end_headers()
            self.wfile.write(html_content.encode("utf-8"))
        except Exception as e:
            self.send_error(500, str(e))
    
    def handle_card_search(self, parsed_url):
        """Handle card search by name."""
        query_params = parse_qs(parsed_url.query)
        name = query_params.get("name", [""])[0]
        
        if not name:
            self.send_json_response({"error": "Card name required"}, 400)
            return
        
        try:
            # Debug: print received name
            print(f"[DEBUG] Received search query: {repr(name)}")
            card = fetch_card_by_name(name)
            if card:
                print(f"[DEBUG] Found card: {card.get('name')}")
                self.send_json_response({"card": card})
            else:
                print(f"[DEBUG] Card not found for: {repr(name)}")
                self.send_json_response({"error": f"Card not found: {name}"}, 404)
        except RuntimeError as e:
            print(f"[DEBUG] RuntimeError: {e}")
            self.send_json_response({"error": str(e)}, 400)
        except Exception as e:
            print(f"[DEBUG] Unexpected error: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            self.send_json_response({"error": f"Unexpected error: {e}"}, 500)
    
    def handle_card_by_set(self, parsed_url):
        """Handle card search by set and collector number."""
        query_params = parse_qs(parsed_url.query)
        set_code = query_params.get("set", [""])[0]
        collector_number = query_params.get("collector", [""])[0]
        
        if not set_code or not collector_number:
            self.send_json_response({"error": "Set code and collector number required"}, 400)
            return
        
        try:
            card = fetch_card_by_set_number(set_code, collector_number)
            if card:
                self.send_json_response({"card": card})
            else:
                self.send_json_response({"error": f"Card not found: {set_code} {collector_number}"}, 404)
        except RuntimeError as e:
            self.send_json_response({"error": str(e)}, 400)
    
    def handle_search(self, parsed_url):
        """Handle card search with suggestions."""
        query_params = parse_qs(parsed_url.query)
        query = query_params.get("q", [""])[0]
        
        if not query or len(query) < 2:
            self.send_json_response({"results": []})
            return
        
        try:
            print(f"[DEBUG] Search suggestions for: {repr(query)}")
            cards = search_cards_by_name(query, limit=20)
            print(f"[DEBUG] Found {len(cards)} suggestions")
            self.send_json_response({"results": cards})
        except RuntimeError as e:
            print(f"[DEBUG] RuntimeError in search: {e}")
            self.send_json_response({"error": str(e)}, 400)
        except Exception as e:
            print(f"[DEBUG] Unexpected error in search: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            self.send_json_response({"error": f"Unexpected error: {e}"}, 500)
    
    def send_json_response(self, data, status_code=200):
        """Send a JSON response."""
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        json_bytes = json_str.encode("utf-8")
        
        self.send_response(status_code)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.send_header("Content-length", len(json_bytes))
        self.end_headers()
        self.wfile.write(json_bytes)
    
    def log_message(self, format, *args):
        """Suppress default logging."""
        pass
