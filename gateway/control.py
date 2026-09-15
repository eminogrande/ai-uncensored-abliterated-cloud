#!/usr/bin/env python3
"""
ABLITERATED.cloud control panel.

A password-protected web page to start and stop your GPU, plus the same
actions as a CLI. Stdlib only - no dependencies, no build step.

  python3 control.py serve          # web panel on 127.0.0.1:8099
  python3 control.py status         # print instance state
  python3 control.py start          # start the GPU
  python3 control.py stop           # stop the GPU (keeps the disk)

Configuration comes from environment variables, never from this file:

  ABL_VAST_KEY       Vast.ai API key                (required)
  ABL_INSTANCE       Vast instance id               (required)
  ABL_PANEL_HASH     sha256 of the panel password   (required for serve)
  ABL_PANEL_PORT     panel port                     (default 8099)

Create the password hash with:

  python3 -c "import hashlib,getpass;print(hashlib.sha256(getpass.getpass().encode()).hexdigest())"
"""
import hashlib
import hmac
import http.server
import json
import os
import secrets
import socketserver
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

VAST_API = "https://console.vast.ai/api/v0"
SESSIONS = {}
SESSION_TTL = 8 * 3600


def config(name, default=None, required=False):
    value = os.environ.get(name, default)
    if required and not value:
        sys.exit(f"missing required environment variable: {name}")
    return value or ""


def vast(path, method="GET", payload=None):
    key = config("ABL_VAST_KEY", required=True)
    url = f"{VAST_API}{path}"
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {key}")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read() or "{}")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")[:300]
        return {"success": False, "error": f"HTTP {exc.code}", "detail": detail}
    except Exception as exc:
        return {"success": False, "error": type(exc).__name__}


def instance_id():
    return config("ABL_INSTANCE", required=True)


def status():
    data = vast(f"/instances/{instance_id()}/?owner=me")
    inst = data.get("instances") or data.get("instance") or {}
    if not inst:
        return {"ok": False, "error": data.get("error", "instance not found"),
                "detail": data.get("detail", "")}
    gpu_hour = float(inst.get("dph_total") or 0)
    disk_hour = float(inst.get("storage_total_cost") or 0)
    running = inst.get("actual_status") == "running"
    return {
        "ok": True,
        "id": inst.get("id"),
        "gpu": inst.get("gpu_name"),
        "actual": inst.get("actual_status"),
        "intended": inst.get("intended_status"),
        "running": running,
        "disk_gb": inst.get("disk_space"),
        "ssh_host": inst.get("ssh_host"),
        "ssh_port": inst.get("ssh_port"),
        "cost_now_hour": round(gpu_hour if running else disk_hour, 4),
        "cost_running_hour": round(gpu_hour, 4),
        "cost_stopped_day": round(disk_hour * 24, 2),
    }


def start():
    return vast(f"/instances/{instance_id()}/", "PUT", {"state": "running"})


def stop():
    return vast(f"/instances/{instance_id()}/", "PUT", {"state": "stopped"})


PAGE = """<!doctype html>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ABLITERATED.cloud control</title>
<style>
  body{font:17px/1.6 system-ui,-apple-system,sans-serif;max-width:640px;
       margin:0 auto;padding:32px 20px;color:#171717;background:#fff}
  h1{font-size:22px;margin:0 0 4px}
  .sub{color:#525252;margin:0 0 28px}
  .card{border:1px solid #d8d8d8;border-radius:10px;padding:20px;margin:0 0 20px}
  .row{display:flex;justify-content:space-between;padding:7px 0;
       border-bottom:1px solid #f0f0f0}
  .row:last-child{border:0}
  .k{color:#525252}
  .v{font-weight:600;font-variant-numeric:tabular-nums}
  .dot{display:inline-block;width:9px;height:9px;border-radius:50%;
       margin-right:7px;vertical-align:middle}
  .on{background:#16a34a}.off{background:#a3a3a3}.wait{background:#ea580c}
  button{font:inherit;font-weight:600;padding:13px 22px;border-radius:8px;
         border:1px solid #171717;background:#171717;color:#fff;cursor:pointer;
         margin-right:10px}
  button.ghost{background:#fff;color:#171717}
  button:disabled{opacity:.4;cursor:not-allowed}
  input{font:inherit;padding:11px 13px;border:1px solid #d8d8d8;
        border-radius:8px;width:100%;box-sizing:border-box}
  .msg{padding:11px 14px;border-radius:8px;margin:16px 0;display:none}
  .err{background:#fef2f2;color:#991b1b;border:1px solid #fecaca}
  .ok{background:#f0fdf4;color:#166534;border:1px solid #bbf7d0}
  .note{color:#525252;font-size:15px}
  code{background:#f5f5f5;padding:2px 6px;border-radius:4px;font-size:14px}
</style>
<h1>ABLITERATED.cloud</h1>
<p class="sub">Start and stop your GPU. Costs accrue only while it runs.</p>

<div id="login" class="card">
  <p style="margin:0 0 12px"><strong>Password</strong></p>
  <input id="pw" type="password" autofocus onkeydown="if(event.key==='Enter')login()">
  <div id="loginmsg" class="msg err"></div>
  <p style="margin:16px 0 0"><button onclick="login()">Unlock</button></p>
</div>

<div id="panel" style="display:none">
  <div class="card">
    <div class="row"><span class="k">State</span>
      <span class="v"><span id="dot" class="dot off"></span><span id="state">...</span></span></div>
    <div class="row"><span class="k">GPU</span><span class="v" id="gpu">-</span></div>
    <div class="row"><span class="k">Costing now</span><span class="v" id="cost">-</span></div>
    <div class="row"><span class="k">Instance</span><span class="v" id="iid">-</span></div>
  </div>
  <div id="msg" class="msg"></div>
  <p>
    <button id="startb" onclick="act('start')">Start GPU</button>
    <button id="stopb" class="ghost" onclick="act('stop')">Stop GPU</button>
  </p>
  <p class="note">Stopping keeps your disk and the downloaded model, and ends
  GPU billing. The disk keeps costing a small amount per day. Starting can wait
  for a free card - the state shows <code>scheduling</code> until it boots.</p>
</div>

<script>
let token = null;
function show(el, cls, text){
  const m = document.getElementById(el);
  m.className = 'msg ' + cls; m.textContent = text; m.style.display = 'block';
}
async function login(){
  const r = await fetch('/api/login', {method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({password: document.getElementById('pw').value})});
  const d = await r.json();
  if(!d.token){ show('loginmsg','err', d.error || 'Wrong password'); return; }
  token = d.token;
  document.getElementById('login').style.display='none';
  document.getElementById('panel').style.display='block';
  refresh(); setInterval(refresh, 5000);
}
async function refresh(){
  const r = await fetch('/api/status', {headers:{'Authorization':'Bearer '+token}});
  const d = await r.json();
  if(!d.ok){ show('msg','err', d.error || 'Cannot read state'); return; }
  const running = d.running, scheduling = d.intended==='running' && !running;
  document.getElementById('state').textContent =
    running ? 'running' : (scheduling ? 'scheduling' : 'stopped');
  document.getElementById('dot').className =
    'dot ' + (running ? 'on' : (scheduling ? 'wait' : 'off'));
  document.getElementById('gpu').textContent = d.gpu || '-';
  document.getElementById('cost').textContent =
    running ? ('$' + d.cost_running_hour + '/hour')
            : ('$' + d.cost_stopped_day + '/day (disk only)');
  document.getElementById('iid').textContent = d.id;
  document.getElementById('startb').disabled = running || scheduling;
  document.getElementById('stopb').disabled = !running && !scheduling;
}
async function act(what){
  document.getElementById('startb').disabled = true;
  document.getElementById('stopb').disabled = true;
  const r = await fetch('/api/'+what, {method:'POST',
    headers:{'Authorization':'Bearer '+token}});
  const d = await r.json();
  show('msg', d.success ? 'ok' : 'err',
       d.success ? (what==='start' ? 'Start requested. This can take a few minutes.'
                                   : 'Stop requested.')
                 : (d.detail || d.error || 'Request failed'));
  setTimeout(refresh, 1500);
}
</script>
"""


class Handler(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, format, *args):
        sys.stderr.write(f"{self.address_string()} {format % args}\n")

    def _send(self, code, body, ctype="application/json"):
        raw = body if isinstance(body, bytes) else body.encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "no-referrer")
        self.end_headers()
        self.wfile.write(raw)

    def _authed(self):
        header = self.headers.get("Authorization", "")
        token = header[7:].strip() if header.startswith("Bearer ") else ""
        expires = SESSIONS.get(token)
        if not expires or expires < time.time():
            SESSIONS.pop(token, None)
            self._send(401, json.dumps({"ok": False, "error": "session expired"}))
            return False
        return True

    def do_GET(self):
        if self.path == "/":
            return self._send(200, PAGE, "text/html; charset=utf-8")
        if self.path == "/api/status":
            if not self._authed():
                return
            return self._send(200, json.dumps(status()))
        self._send(404, json.dumps({"error": "not found"}))

    def do_POST(self):
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b"{}"
        if self.path == "/api/login":
            expected = config("ABL_PANEL_HASH", required=True)
            try:
                supplied = json.loads(raw).get("password", "")
            except Exception:
                supplied = ""
            digest = hashlib.sha256(supplied.encode()).hexdigest()
            time.sleep(0.4)  # blunt the edge off guessing
            if not hmac.compare_digest(digest, expected):
                return self._send(401, json.dumps({"error": "Wrong password"}))
            token = secrets.token_urlsafe(32)
            SESSIONS[token] = time.time() + SESSION_TTL
            return self._send(200, json.dumps({"token": token}))
        if self.path in ("/api/start", "/api/stop"):
            if not self._authed():
                return
            result = start() if self.path.endswith("start") else stop()
            return self._send(200, json.dumps(result))
        self._send(404, json.dumps({"error": "not found"}))


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


def main():
    action = sys.argv[1] if len(sys.argv) > 1 else "status"
    if action == "serve":
        port = int(config("ABL_PANEL_PORT", "8099"))
        config("ABL_PANEL_HASH", required=True)
        with Server(("127.0.0.1", port), Handler) as srv:
            print(f"control panel on http://127.0.0.1:{port}", flush=True)
            srv.serve_forever()
    elif action == "status":
        state = status()
        if not state.get("ok"):
            sys.exit(f"error: {state.get('error')} {state.get('detail','')}")
        label = "running" if state["running"] else state["actual"]
        print(f"instance {state['id']} ({state['gpu']}): {label}")
        print(f"  intended:  {state['intended']}")
        print(f"  disk:      {state['disk_gb']} GB")
        print(f"  cost:      ${state['cost_running_hour']}/h running, "
              f"${state['cost_stopped_day']}/day stopped")
        if state["running"]:
            print(f"  ssh:       ssh -p {state['ssh_port']} root@{state['ssh_host']}")
    elif action == "start":
        print(json.dumps(start(), indent=2))
    elif action == "stop":
        print(json.dumps(stop(), indent=2))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
