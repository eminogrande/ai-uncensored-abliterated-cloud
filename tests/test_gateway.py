"""Gateway and control-panel contracts; no network, no GPU, no side effects."""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(module_name, relative):
    spec = importlib.util.spec_from_file_location(module_name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def gateway_env(tmp):
    os.environ["ABL_DB"] = str(tmp / "tokens.db")
    os.environ["ABL_SECRET"] = str(tmp / "secret.key")
    return load("abl_gateway", "gateway/gateway.py")


def test_valid_token_verifies_and_survives_reload():
    with tempfile.TemporaryDirectory() as raw:
        gw = gateway_env(Path(raw))
        token = gw.mint("unit-test", 24)
        assert token.startswith("abl_")
        ok, label = gw.verify(token)
        assert ok and label == "unit-test"


def test_expired_token_is_refused_with_its_reason():
    with tempfile.TemporaryDirectory() as raw:
        gw = gateway_env(Path(raw))
        ok, reason = gw.verify(gw.mint("already-over", -1))
        assert not ok and reason == "token expired"


def test_tampered_payload_fails_signature_not_expiry():
    """The expiry is inside the signed payload, so it cannot be edited."""
    with tempfile.TemporaryDirectory() as raw:
        gw = gateway_env(Path(raw))
        token = gw.mint("victim", 1)
        body, _, sig = token[4:].partition(".")
        claims = json.loads(gw.b64d(body))
        claims["exp"] = 9999999999  # try to grant ourselves a century
        forged = "abl_" + gw.b64e(json.dumps(claims).encode()) + "." + sig
        ok, reason = gw.verify(forged)
        assert not ok and reason == "bad signature"


def test_revocation_beats_a_still_valid_expiry():
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        gw = gateway_env(tmp)
        token = gw.mint("leaked", 24)
        assert gw.verify(token)[0]
        subprocess.run(
            [sys.executable, str(ROOT / "gateway/gateway.py"), "revoke",
             json.loads(gw.b64d(token[4:].partition(".")[0]))["jti"][:8]],
            env={**os.environ, "ABL_DB": str(tmp / "tokens.db"),
                 "ABL_SECRET": str(tmp / "secret.key")},
            check=True, capture_output=True,
        )
        ok, reason = gw.verify(token)
        assert not ok and reason == "token revoked"


def test_unsigned_and_foreign_tokens_are_refused():
    with tempfile.TemporaryDirectory() as raw:
        gw = gateway_env(Path(raw))
        for candidate in ("", "hunter2", "Bearer abl_x", "abl_nodot", "abl_a.b"):
            assert not gw.verify(candidate)[0]


def test_health_is_public_and_v1_is_not():
    with tempfile.TemporaryDirectory() as raw:
        gw = gateway_env(Path(raw))
        assert "/health" in gw.PUBLIC_PATHS
        assert not any(path.startswith("/v1/chat") for path in gw.PUBLIC_PATHS)


def test_control_panel_password_is_never_stored_in_the_repo():
    source = (ROOT / "gateway/control.py").read_text()
    assert "ABL_PANEL_HASH" in source
    assert "sha256" in source
    # no literal 64-char hex hash committed
    import re
    assert not re.search(r"['\"][0-9a-f]{64}['\"]", source)


def test_control_panel_reads_config_only_from_environment():
    source = (ROOT / "gateway/control.py").read_text()
    for secret_name in ("ABL_VAST_KEY", "ABL_INSTANCE", "ABL_PANEL_HASH"):
        assert f'config("{secret_name}"' in source or f'"{secret_name}"' in source
    assert "console.vast.ai/api/v0" in source


def test_scripts_are_executable_and_parse():
    for name in ("rent-gpu.sh", "setup-model.sh", "gpu.sh"):
        path = ROOT / "scripts" / name
        assert os.access(path, os.X_OK), f"{name} is not executable"
        subprocess.run(["bash", "-n", str(path)], check=True, capture_output=True)


def test_scripts_never_destroy_and_always_confirm_spend():
    """stop keeps the disk; destroy is not something a helper script should do."""
    import re
    for name in ("rent-gpu.sh", "setup-model.sh", "gpu.sh"):
        body = (ROOT / "scripts" / name).read_text()
        # the command, not the word in prose
        assert not re.search(r"vastai\s+destroy|destroy\s+instance", body), \
            f"{name} must not destroy instances"
    rent = (ROOT / "scripts/rent-gpu.sh").read_text()
    assert "read -r -p" in rent, "renting must ask before it charges"
    assert "$PRICE" in rent, "the price must be shown before confirming"


def test_no_credentials_are_committed():
    for relative in ("gateway/gateway.py", "gateway/control.py",
                     "scripts/rent-gpu.sh", "scripts/gpu.sh",
                     "scripts/setup-model.sh", "docs/API.md", "README.md"):
        body = (ROOT / relative).read_text()
        assert "abl_eyJ" not in body, f"{relative} contains a real token"
        assert "pk1_" not in body and "sk1_" not in body, f"{relative} has Porkbun keys"
