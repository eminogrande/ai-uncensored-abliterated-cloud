#!/usr/bin/env python3
"""
Autopilot: wake the GPU on demand, stop it when nobody is using it.

Runs next to the API gateway. Two jobs:

  wake   - called by the gateway when a request arrives and the GPU is off.
           Starts the instance, waits for it, launches llama-server, opens
           the tunnel. Idempotent: concurrent calls do not stack up.
  reap   - called on a timer. Stops the instance when the last request is
           older than ABL_IDLE_MINUTES.

Environment:
  ABL_VAST_KEY       Vast.ai API key                    (required)
  ABL_INSTANCE       Vast instance id                   (required)
  ABL_IDLE_MINUTES   idle window before stopping        (default 30)
  ABL_MODEL_FILE     GGUF filename on the GPU           (default OBLITERATED Q6_K)
  ABL_CTX            context size                       (default 65536)
  ABL_STATE          activity + lock directory          (default /opt/abliterated)
  ABL_SSH_KEY        key that can reach the GPU         (default ~/.ssh/id_ed25519)
  ABL_LOCAL_PORT     local port the tunnel exposes      (default 8095)
"""
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request

VAST_API = "https://console.vast.ai/api/v0"
STATE = os.environ.get("ABL_STATE", "/opt/abliterated")
ACTIVITY = os.path.join(STATE, "last-activity")
LOCK = os.path.join(STATE, "wake.lock")
LOG = os.path.join(STATE, "autopilot.log")
IDLE_MINUTES = float(os.environ.get("ABL_IDLE_MINUTES", "30"))
MODEL_FILE = os.environ.get("ABL_MODEL_FILE", "Qwen3.8-27B-OBLITERATED-Q6_K.gguf")
CTX = os.environ.get("ABL_CTX", "65536")
SSH_KEY = os.environ.get("ABL_SSH_KEY", os.path.expanduser("~/.ssh/id_ed25519"))
LOCAL_PORT = os.environ.get("ABL_LOCAL_PORT", "8095")
WAKE_TIMEOUT = 900  # 15 minutes: boot, then model load


def log(message):
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S')} {message}"
    print(line, flush=True)
    try:
        with open(LOG, "a") as fh:
            fh.write(line + "\n")
    except OSError:
        pass


def need(name):
    value = os.environ.get(name)
    if not value:
        sys.exit(f"missing required environment variable: {name}")
    return value


def vast(path, method="GET", payload=None):
    url = f"{VAST_API}{path}"
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {need('ABL_VAST_KEY')}")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read() or "{}")
    except urllib.error.HTTPError as exc:
        return {"success": False, "error": f"HTTP {exc.code}",
                "detail": exc.read().decode(errors="replace")[:200]}
    except Exception as exc:
        return {"success": False, "error": type(exc).__name__}


def instance():
    data = vast(f"/instances/{need('ABL_INSTANCE')}/?owner=me")
    return data.get("instances") or data.get("instance") or {}


def touch():
    """Record that someone used the API just now."""
    os.makedirs(STATE, exist_ok=True)
    with open(ACTIVITY, "w") as fh:
        fh.write(str(int(time.time())))


def last_activity():
    try:
        with open(ACTIVITY) as fh:
            return int(fh.read().strip())
    except (OSError, ValueError):
        return 0


def upstream_alive():
    try:
        with urllib.request.urlopen(
            f"http://127.0.0.1:{LOCAL_PORT}/health", timeout=4
        ) as resp:
            return resp.status == 200
    except Exception:
        return False


def ssh_to(host, port, *command):
    return subprocess.run(
        ["ssh", "-o", "StrictHostKeyChecking=accept-new", "-o", "IdentitiesOnly=yes",
         "-o", "ConnectTimeout=15", "-i", SSH_KEY, "-p", str(port), f"root@{host}", *command],
        capture_output=True, text=True, timeout=180,
    )


def open_tunnel(host, port):
    subprocess.run(["pkill", "-f", f"L 127.0.0.1:{LOCAL_PORT}"], capture_output=True)
    subprocess.Popen(
        ["ssh", "-o", "StrictHostKeyChecking=accept-new", "-o", "IdentitiesOnly=yes",
         "-o", "ExitOnForwardFailure=yes", "-o", "ServerAliveInterval=15",
         "-i", SSH_KEY, "-N", "-L", f"127.0.0.1:{LOCAL_PORT}:127.0.0.1:8080",
         "-p", str(port), f"root@{host}"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        start_new_session=True,
    )


def wake():
    """Bring the GPU and the model up. Safe to call repeatedly."""
    os.makedirs(STATE, exist_ok=True)
    touch()

    if upstream_alive():
        return {"ok": True, "state": "already running"}

    # A wake in progress holds the lock; do not start a second one.
    try:
        fd = os.open(LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.write(fd, str(int(time.time())).encode())
        os.close(fd)
    except FileExistsError:
        try:
            age = time.time() - os.path.getmtime(LOCK)
        except OSError:
            age = 0
        if age < WAKE_TIMEOUT:
            return {"ok": True, "state": "waking", "seconds_in_progress": int(age)}
        os.unlink(LOCK)  # stale lock from a crashed attempt
        return wake()

    try:
        inst = instance()
        if inst.get("actual_status") != "running":
            log("waking: requesting start")
            result = vast(f"/instances/{need('ABL_INSTANCE')}/", "PUT", {"state": "running"})
            if not result.get("success", True):
                log(f"waking: start refused: {result}")
                return {"ok": False, "error": result.get("msg") or result.get("detail", "start failed")}

        deadline = time.time() + WAKE_TIMEOUT
        while time.time() < deadline:
            inst = instance()
            if inst.get("actual_status") == "running" and inst.get("ssh_host"):
                break
            time.sleep(10)
        else:
            log("waking: timed out waiting for the instance")
            return {"ok": False, "error": "instance did not start in time"}

        host, port = inst["ssh_host"], inst["ssh_port"]
        log(f"waking: instance up at {host}:{port}, starting llama-server")
        started = ssh_to(
            host, port,
            f"pkill -f llama-server || true; sleep 1; "
            f"nohup /root/llama.cpp/build/bin/llama-server "
            f"-m /root/models/{MODEL_FILE} --host 127.0.0.1 --port 8080 "
            f"-ngl 999 -c {CTX} -fa on --jinja --reasoning off "
            f"> /root/server.log 2>&1 & sleep 5; echo launched",
        )
        if started.returncode != 0:
            log(f"waking: ssh failed: {started.stderr[:200]}")
            return {"ok": False, "error": "could not reach the GPU over ssh"}

        open_tunnel(host, port)
        for _ in range(60):  # model load can take a few minutes
            if upstream_alive():
                log("waking: model is serving")
                touch()
                return {"ok": True, "state": "ready"}
            time.sleep(5)
        log("waking: server did not answer in time")
        return {"ok": False, "error": "model did not come up in time"}
    finally:
        try:
            os.unlink(LOCK)
        except OSError:
            pass


def reap():
    """Stop the GPU when it has been idle long enough."""
    inst = instance()
    if inst.get("actual_status") != "running":
        return {"ok": True, "state": "already stopped"}

    if os.path.exists(LOCK):
        return {"ok": True, "state": "wake in progress, not reaping"}

    idle_seconds = time.time() - last_activity()
    if idle_seconds < IDLE_MINUTES * 60:
        return {"ok": True, "state": "busy",
                "idle_minutes": round(idle_seconds / 60, 1)}

    log(f"reaping: idle for {idle_seconds/60:.1f} minutes, stopping")
    subprocess.run(["pkill", "-f", f"L 127.0.0.1:{LOCAL_PORT}"], capture_output=True)
    result = vast(f"/instances/{need('ABL_INSTANCE')}/", "PUT", {"state": "stopped"})
    ok = result.get("success", True)
    log(f"reaping: stop {'requested' if ok else 'failed'}")
    return {"ok": ok, "state": "stopped" if ok else "stop failed", "detail": result}


def status():
    inst = instance()
    running = inst.get("actual_status") == "running"
    idle_seconds = time.time() - last_activity()
    return {
        "instance": inst.get("id"),
        "gpu": inst.get("gpu_name"),
        "state": inst.get("actual_status"),
        "serving": upstream_alive(),
        "idle_minutes": round(idle_seconds / 60, 1) if last_activity() else None,
        "stops_in_minutes": (round(IDLE_MINUTES - idle_seconds / 60, 1)
                             if running and last_activity() else None),
        "waking": os.path.exists(LOCK),
        "cost_per_hour": round(float(inst.get("dph_total") or 0), 4) if running else 0,
    }


if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "status"
    handlers = {"wake": wake, "reap": reap, "status": status, "touch": touch}
    if action not in handlers:
        sys.exit(__doc__)
    result = handlers[action]()
    print(json.dumps(result, indent=2) if result is not None else "ok")
