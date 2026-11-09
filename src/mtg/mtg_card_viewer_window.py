#!/usr/bin/env python3
"""Windows embedded viewer for individual MTG cards."""

import sys
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path

import webview

from .mtg_card_viewer_server import CardViewerHandler, HOST


class EmbeddedCardViewerHandler(CardViewerHandler):
    page_path = (
        Path(sys._MEIPASS) / "mtg_card_viewer.html"
        if getattr(sys, "frozen", False)
        else CardViewerHandler.page_path
    )


def main() -> None:
    """Start the Windows embedded card viewer."""
    server = ThreadingHTTPServer((HOST, 0), EmbeddedCardViewerHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        webview.settings["ALLOW_DOWNLOADS"] = True
        url = f"http://{HOST}:{server.server_port}/"
        webview.create_window(
            "MTG Card Viewer",
            url,
            width=450,
            height=800,
            min_size=(450, 800),
            resizable=False
        )
        webview.start(gui="edgechromium")
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


if __name__ == "__main__":
    main()
