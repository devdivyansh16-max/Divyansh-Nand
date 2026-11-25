#!/usr/bin/env python3
"""Serve the Hack Computer Lab dashboard and its local build action."""
import json
import subprocess
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REQUIRED_FILES = (
    "hdl/CPU.hdl",
    "hdl/Memory.hdl",
    "hdl/Computer.hdl",
    "assembler.py",
    "Box.asm",
    "Box.hack",
    "Add.asm",
    "Max.asm",
    "Rect.asm",
    "Pong.asm",
)


class DashboardHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def _send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/api/status":
            self._send_json(200, {
                "files": {name: (ROOT / name).is_file() for name in REQUIRED_FILES},
                "official": (ROOT / "official").is_dir(),
            })
            return
        if self.path == "/":
            self.path = "/dashboard.html"
        super().do_GET()

    def do_POST(self):
        if self.path != "/api/build":
            self._send_json(404, {"error": "Unknown dashboard action."})
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length < 1 or length > 4096:
                raise ValueError("Request body must be between 1 and 4096 bytes.")
            request = json.loads(self.rfile.read(length))
            k = request.get("k")
            if isinstance(k, bool) or not isinstance(k, int) or not 0 <= k <= 99:
                raise ValueError("K must be a whole number from 0 to 99.")
        except (ValueError, json.JSONDecodeError) as error:
            self._send_json(400, {"error": str(error)})
            return

        try:
            result = subprocess.run(
                [sys.executable, "run_all.py", str(k)],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                timeout=90,
                check=False,
            )
        except subprocess.TimeoutExpired:
            self._send_json(504, {"error": "Build timed out after 90 seconds."})
            return

        self._send_json(200, {
            "ok": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        })

    def log_message(self, format, *args):
        print("%s - %s" % (self.address_string(), format % args))


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    server = ThreadingHTTPServer(("127.0.0.1", port), DashboardHandler)
    print("Hack Computer Lab dashboard: http://127.0.0.1:%s" % port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nDashboard server stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
