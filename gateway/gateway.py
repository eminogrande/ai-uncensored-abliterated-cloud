#!/usr/bin/env python3
"""
ABLITERATED.cloud API gateway.

OpenAI-compatible reverse proxy in front of a llama.cpp server, with bearer
tokens that can expire. Stdlib only - no dependencies.

Tokens are HMAC-signed and stateless-verifiable, but also recorded in a SQLite
file so they can be listed and revoked.

  abl_<base64url(payload)>.<base64url(hmac-sha256)>

payload = {"jti": str, "exp": int|null, "label": str}

exp = null means never expires (owner token).
"""
import base64
import hashlib
import hmac
import http.server
import json
import os
import socketserver
import sqlite3
import sys
import time
import urllib.error
import urllib.request
import uuid

UPSTREAM = os.environ.get("ABL_UPSTREAM", "http://127.0.0.1:8080")
DB_PATH = os.environ.get("ABL_DB", "/opt/abliterated/tokens.db")
SECRET_PATH = os.environ.get("ABL_SECRET", "/opt/abliterated/secret.key")
PORT = int(os.environ.get("ABL_PORT", "8090"))
# Endpoints served without a token.
PUBLIC_PATHS = {"/health", "/v1/health"}


def secret():
    if not os.path.exists(SECRET_PATH):
        os.makedirs(os.path.dirname(SECRET_PATH), exist_ok=True)
        with open(os.open(SECRET_PATH, os.O_CREAT | os.O_WRONLY, 0o600), "wb") as fh:
            fh.write(os.urandom(32))
    with open(SECRET_PATH, "rb") as fh:
        return fh.read()


def db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS tokens ("
        "jti TEXT PRIMARY KEY, label TEXT, created INTEGER, "
        "expires INTEGER, revoked INTEGER DEFAULT 0, last_used INTEGER, calls INTEGER DEFAULT 0)"
    )
    conn.commit()
    return conn


def b64e(raw):
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")


def b64d(text):
    return base64.urlsafe_b64decode(text + "=" * (-len(text) % 4))


def mint(label, hours):
    jti = uuid.uuid4().hex
    exp = None if hours is None else int(time.time() + hours * 3600)
    payload = json.dumps({"jti": jti, "exp": exp, "label": label}, separators=(",", ":"))
    body = b64e(payload.encode())
    sig = b64e(hmac.new(secret(), body.encode(), hashlib.sha256).digest())
    conn = db()
    conn.execute(
        "INSERT INTO tokens (jti, label, created, expires) VALUES (?,?,?,?)",
        (jti, label, int(time.time()), exp),
    )
    conn.commit()
    conn.close()
    return f"abl_{body}.{sig}"


def verify(token):
    if not token.startswith("abl_") or "." not in token:
        return False, "malformed token"
    body, _, sig = token[4:].partition(".")
    expected = b64e(hmac.new(secret(), body.encode(), hashlib.sha256).digest())
    if not hmac.compare_digest(sig, expected):
        return False, "bad signature"
    try:
        claims = json.loads(b64d(body))
    except Exception:
        return False, "bad payload"
    exp = claims.get("exp")
    if exp is not None and time.time() > exp:
        return False, "token expired"
    conn = db()
    row = conn.execute("SELECT revoked FROM tokens WHERE jti=?", (claims["jti"],)).fetchone()
    if row is None:
        conn.close()
        return False, "unknown token"
    if row[0]:
        conn.close()
        return False, "token revoked"
    conn.execute(
        "UPDATE tokens SET last_used=?, calls=calls+1 WHERE jti=?",
        (int(time.time()), claims["jti"]),
    )
    conn.commit()
    conn.close()
    return True, claims.get("label", "")


class Handler(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):  # quieter logs, no token material
        sys.stderr.write(f"{self.address_string()} {fmt % args}\n")

    def _deny(self, code, message):
        body = json.dumps({"error": {"message": message, "type": "invalid_request_error"}}).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _auth_ok(self):
        if self.path in PUBLIC_PATHS:
            return True
        header = self.headers.get("Authorization", "")
        if not header.startswith("Bearer "):
            self._deny(401, "Missing bearer token. Use: Authorization: Bearer abl_...")
            return False
        ok, reason = verify(header[7:].strip())
        if not ok:
            self._deny(401, reason)
            return False
        return True

    def _proxy(self, method):
        if not self._auth_ok():
            return
        length = int(self.headers.get("Content-Length") or 0)
        payload = self.rfile.read(length) if length else None
        req = urllib.request.Request(UPSTREAM + self.path, data=payload, method=method)
        for name in ("Content-Type", "Accept"):
            if self.headers.get(name):
                req.add_header(name, self.headers[name])
        try:
            with urllib.request.urlopen(req, timeout=600) as upstream:
                self.send_response(upstream.status)
                for key, value in upstream.headers.items():
                    if key.lower() in ("content-type", "cache-control"):
                        self.send_header(key, value)
                self.send_header("Transfer-Encoding", "chunked")
                self.end_headers()
                while chunk := upstream.read(2048):  # stream SSE through unbuffered
                    self.wfile.write(b"%X\r\n%s\r\n" % (len(chunk), chunk))
                    self.wfile.flush()
                self.wfile.write(b"0\r\n\r\n")
        except urllib.error.HTTPError as exc:
            detail = exc.read()
            self.send_response(exc.code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(detail)))
            self.end_headers()
            self.wfile.write(detail)
        except Exception as exc:
            self._deny(502, f"upstream unavailable: {type(exc).__name__}")

    def do_GET(self):
        self._proxy("GET")

    def do_POST(self):
        self._proxy("POST")


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "mint":
        label = sys.argv[2] if len(sys.argv) > 2 else "unnamed"
        hours = None if len(sys.argv) > 3 and sys.argv[3] == "never" else float(sys.argv[3] if len(sys.argv) > 3 else 24)
        print(mint(label, hours))
        return
    if len(sys.argv) > 1 and sys.argv[1] == "list":
        now = int(time.time())
        for jti, label, created, expires, revoked, last, calls in db().execute(
            "SELECT jti,label,created,expires,revoked,last_used,calls FROM tokens ORDER BY created DESC"
        ):
            if revoked:
                state = "REVOKED"
            elif expires is None:
                state = "never expires"
            elif expires < now:
                state = "EXPIRED"
            else:
                state = f"{(expires - now) / 3600:.1f}h left"
            seen = time.strftime("%Y-%m-%d %H:%M", time.gmtime(last)) if last else "never used"
            print(f"{jti[:8]}  {label:<24} {state:<16} calls={calls:<5} last={seen}")
        return
    if len(sys.argv) > 2 and sys.argv[1] == "revoke":
        conn = db()
        cur = conn.execute("UPDATE tokens SET revoked=1 WHERE jti LIKE ?", (sys.argv[2] + "%",))
        conn.commit()
        print(f"revoked {cur.rowcount}")
        return
    with Server(("127.0.0.1", PORT), Handler) as srv:
        print(f"gateway on 127.0.0.1:{PORT} -> {UPSTREAM}", flush=True)
        srv.serve_forever()


if __name__ == "__main__":
    main()
