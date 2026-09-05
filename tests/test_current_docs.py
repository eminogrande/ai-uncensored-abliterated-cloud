"""Current documentation contracts; no network or GPU side effects."""
import json
import re
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_snapshot_is_complete_stopped_and_billed():
    snapshot = json.loads((ROOT / "docs/evidence/2026-09-05-status.json").read_text())
    assert snapshot["total_instances"] == 1
    assert snapshot["running_instances"] == 0
    assert snapshot["instance"]["actual_status"] == "exited"
    assert snapshot["instance"]["intended_status"] == "stopped"
    rate = snapshot["billing_usd_hour"]
    assert rate["gpu"] == 0
    assert rate["disk"] > 0
    assert round(Decimal(str(rate["disk"])) * 24 * 30, 2) == Decimal("24.00")
    assert snapshot["modal"]["decommissioned"] is False
    assert snapshot["auto_stop_verified"] is False
    assert snapshot["inference_tested_this_audit"] is False
    assert not ({"credit", "jupyter_token", "api_key", "public_ipaddr"} & snapshot.keys())


def test_current_license_and_dependency_scope():
    assert (ROOT / "LICENSE").read_text().startswith("MIT License\n")
    package = json.loads((ROOT / "package.json").read_text())
    lock = json.loads((ROOT / "package-lock.json").read_text())
    assert package["license"] == lock["packages"][""]["license"] == "MIT"
    assert package["version"] == lock["version"] == lock["packages"][""]["version"]
    assert not package.get("dependencies")
    assert not package.get("devDependencies")
    assert (ROOT / "archive/licenses/Apache-2.0.txt").is_file()
    assert "license = \"MIT\"" in (ROOT / "pyproject.toml").read_text()


def test_front_door_is_not_modal_or_a_guarantee():
    readme = (ROOT / "README.md").read_text()
    assert "Vast.ai + llama.cpp" in readme
    assert "still billed while stopped" in readme
    assert "No universal zero-refusal guarantee" in readme
    assert "No validated 262k workload" in readme
    assert "archive/modal/README.md" in readme
    assert not (ROOT / "modal_gateway.py").exists()
    assert (ROOT / "archive/modal/modal_gateway.py").exists()
    assert (ROOT / "archive/modal/README.original.md").exists()


def test_current_relative_document_links_resolve():
    paths = [ROOT / "README.md", ROOT / "SECURITY.md", *sorted((ROOT / "docs").glob("*.md"))]
    errors = []
    for path in paths:
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
            if "://" in target or target.startswith(("#", "mailto:")):
                continue
            target = target.split("#", 1)[0]
            if target and not (path.parent / target).exists():
                errors.append(f"{path.relative_to(ROOT)}: {target}")
    assert not errors, "\n".join(errors)


def test_shutdown_documentation_does_not_use_destroy_as_stop():
    operations = (ROOT / "docs/OPERATIONS.md").read_text()
    assert "vastai stop instance 49433042" in operations
    assert "vastai destroy instance" not in operations
    assert "no verified automatic idle shutdown" in operations
    assert "GPU compute stops; storage billing continues" in operations


def test_generated_costs_match_provider_evidence():
    import runpy
    builder = runpy.run_path(str(ROOT / "scripts/build-blog.py"))
    status = json.loads((ROOT / "website/.well-known/project-status.json").read_text())
    evidence = json.loads((ROOT / "docs/evidence/2026-09-05-vast-recheck.json").read_text())
    rates = status["current"]["running_quote_usd_per_hour"]
    assert rates == {"gpu": evidence["rates_usd"]["gpu_hour"],
                     "disk": evidence["rates_usd"]["disk_hour"],
                     "total": evidence["rates_usd"]["running_hour"]}
    assert status["snapshot_at"] == evidence["checked_at"]
    assert status["current"]["actual_status"] == evidence["instance"]["actual_status"]
    assert [cost for _, cost in builder["cost_rows"](status)] == ["$0.63333", "$15.20", "$456.00", "$24.00", "$60.00"]
    block = builder["render_costs"](status)
    for file in [ROOT / "README.md", ROOT / "website/index.md", ROOT / "website/llms.txt", ROOT / "website/llms-full.txt"]:
        assert block in file.read_text(), file


def test_cost_generator_rejects_inconsistent_rates():
    import runpy
    import pytest
    builder = runpy.run_path(str(ROOT / "scripts/build-blog.py"))
    status = {"current": {"running_quote_usd_per_hour": {"gpu": 0.6, "disk": 0.03, "total": 0.6}}}
    with pytest.raises(ValueError, match="inconsistent"):
        builder["cost_rows"](status)


def test_archived_files_match_manifest():
    import hashlib
    manifest = json.loads((ROOT / "archive/modal/MANIFEST.json").read_text())
    for row in manifest["files"]:
        file = ROOT / row["archived_path"]
        assert hashlib.sha256(file.read_bytes()).hexdigest() == row["archived_sha256"], file
