"""Local connectivity probe only: never dispatch commands from this server."""

import argparse
from contextlib import suppress
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class PingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/ping":
            self.send_error(404)
            return
        body = b'{"message": "pong from Mac"}'
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    with ThreadingHTTPServer((args.host, args.port), PingHandler) as server:
        print(f"Ping probe listening on {args.host}:{args.port}; Ctrl-C to stop", flush=True)
        with suppress(KeyboardInterrupt):
            server.serve_forever()
