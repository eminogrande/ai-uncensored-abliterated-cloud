"""Autopilot idle/wake logic. No network, no GPU, no spend."""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_autopilot(tmp, idle_minutes="30", instance="12345"):
    os.environ.update({
        "ABL_STATE": str(tmp),
        "ABL_IDLE_MINUTES": idle_minutes,
        "ABL_VAST_KEY": "test-key-not-real",
        "ABL_INSTANCE": instance,
    })
    spec = importlib.util.spec_from_file_location("abl_autopilot", ROOT / "gateway/autopilot.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def set_activity(tmp, minutes_ago):
    (tmp / "last-activity").write_text(str(int(time.time() - minutes_ago * 60)))


def test_idle_window_is_respected_exactly():
    """A GPU used 29 minutes ago must not be stopped; 31 minutes ago must."""
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        ap = load_autopilot(tmp, idle_minutes="30")
        ap.instance = lambda: {"actual_status": "running", "id": 1}

        stopped = []
        ap.vast = lambda path, method="GET", payload=None: (
            stopped.append(payload) or {"success": True}
        )

        set_activity(tmp, 29)
        assert ap.reap()["state"] == "busy"
        assert not stopped, "stopped a GPU that was still in use"

        set_activity(tmp, 31)
        assert ap.reap()["state"] == "stopped"
        assert stopped == [{"state": "stopped"}]


def test_a_wake_in_progress_is_never_reaped():
    """Stopping mid-wake would strand a paid boot."""
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        ap = load_autopilot(tmp, idle_minutes="30")
        ap.instance = lambda: {"actual_status": "running", "id": 1}
        stopped = []
        ap.vast = lambda path, method="GET", payload=None: (
            stopped.append(payload) or {"success": True}
        )
        set_activity(tmp, 99)
        (tmp / "wake.lock").write_text(str(int(time.time())))
        assert "wake in progress" in ap.reap()["state"]
        assert not stopped


def test_reap_does_nothing_when_already_stopped():
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        ap = load_autopilot(tmp)
        ap.instance = lambda: {"actual_status": "exited", "id": 1}
        calls = []
        ap.vast = lambda *a, **k: calls.append(a) or {"success": True}
        set_activity(tmp, 999)
        assert ap.reap()["state"] == "already stopped"
        assert not calls, "sent a stop to an already stopped instance"


def test_wake_is_a_noop_when_the_model_already_serves():
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        ap = load_autopilot(tmp)
        ap.upstream_alive = lambda: True
        calls = []
        ap.vast = lambda *a, **k: calls.append(a) or {"success": True}
        assert ap.wake()["state"] == "already running"
        assert not calls, "started a GPU that was already serving"


def test_concurrent_wakes_do_not_stack():
    """Two requests arriving at once must not both boot the GPU."""
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        ap = load_autopilot(tmp)
        ap.upstream_alive = lambda: False
        (tmp / "wake.lock").write_text(str(int(time.time())))
        calls = []
        ap.vast = lambda *a, **k: calls.append(a) or {"success": True}
        result = ap.wake()
        assert result["state"] == "waking"
        assert not calls, "a second wake started another boot"


def test_wake_touches_activity_so_it_is_not_immediately_reaped():
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        ap = load_autopilot(tmp)
        ap.upstream_alive = lambda: True
        ap.wake()
        assert (tmp / "last-activity").exists()
        assert time.time() - ap.last_activity() < 5


def test_missing_activity_file_does_not_crash_or_stop():
    """A fresh install has no activity file; that must not read as 'idle forever'
    while a wake is running, and must not crash."""
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        ap = load_autopilot(tmp)
        assert ap.last_activity() == 0
        ap.instance = lambda: {"actual_status": "exited", "id": 1}
        ap.vast = lambda *a, **k: {"success": True}
        assert ap.reap()["ok"] is True


def test_gateway_wake_hook_is_optional():
    """Without ABL_AUTOPILOT set, the gateway must behave exactly as before."""
    source = (ROOT / "gateway/gateway.py").read_text()
    assert 'AUTOPILOT = os.environ.get("ABL_AUTOPILOT", "")' in source
    assert "if AUTOPILOT and not _upstream_alive():" in source


def test_autopilot_never_destroys():
    source = (ROOT / "gateway/autopilot.py").read_text()
    assert "destroy" not in source.lower().replace("destroyed", "")
    assert '{"state": "stopped"}' in source
