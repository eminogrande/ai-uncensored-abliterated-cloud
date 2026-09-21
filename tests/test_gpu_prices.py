"""Live Vast.ai price table: arithmetic, filters and model coverage."""
import importlib.util
import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
FETCHER = ROOT / "scripts" / "fetch-gpu-prices.py"
PRICES = ROOT / "website" / ".well-known" / "gpu-prices.json"


def load_fetcher():
    spec = importlib.util.spec_from_file_location("fetch_gpu_prices", FETCHER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_published_table_covers_every_model_exactly_once():
    fetcher = load_fetcher()
    document = json.loads(PRICES.read_text())
    labels = {label for label, *_ in fetcher.TIERS}
    assert [tier["label"] for tier in document["tiers"]] == [label for label, *_ in fetcher.TIERS]
    seen = []
    for model_id, params in fetcher.model_tiers():
        label = fetcher.tier_label_for(params)
        assert label in labels, (model_id, label)
        seen.append(label)
    assert len(seen) == sum(tier["covered_models"] for tier in document["tiers"])


def test_tier_boundaries_are_ordered_and_total():
    fetcher = load_fetcher()
    labels = [label for label, *_ in fetcher.TIERS]
    for params in (1, 9, 14, 20, 30, 70, 100, 150, 200, 400, 700, 1000, 3000):
        label = fetcher.tier_label_for(params)
        assert label in labels, params
        # A larger model can never map to a cheaper tier than a smaller one.
        if params > 1:
            assert labels.index(label) >= labels.index(fetcher.tier_label_for(params / 2)), params


def test_size_class_matches_the_vram_window_searched():
    fetcher = load_fetcher()
    document = json.loads(PRICES.read_text())
    by_label = {row["label"]: row for row in document["tiers"]}
    for label, gpus, low, high, disk, _reliability in fetcher.TIERS:
        row = by_label[label]
        assert row["gpus"] == gpus, label
        assert low <= row["vram_per_gpu_mb"] <= high, label
        assert row["disk_gb"] == disk, label


def test_excluded_families_are_reasons_documented_and_matched():
    fetcher = load_fetcher()
    assert fetcher.EXCLUDED_GPU_FAMILIES
    for family, reason in fetcher.EXCLUDED_GPU_FAMILIES:
        assert family and reason and len(reason) > 10
    assert fetcher.excluded({"gpu_name": "RTX 3090"}) is False
    assert fetcher.excluded({"gpu_name": "CMP 170HX"}) is True
    assert fetcher.excluded({"gpu_name": "GTX TITAN X"}) is True
    assert fetcher.excluded({"gpu_name": ""}) is False


def test_check_rejects_tampered_arithmetic():
    fetcher = load_fetcher()
    document = json.loads(PRICES.read_text())
    broken = json.loads(json.dumps(document))
    broken["tiers"][0]["usd_month_24_7"] += 1
    with pytest.raises(AssertionError):
        fetcher.check_document(broken)


def test_check_rejects_missing_or_unsupported_provider():
    fetcher = load_fetcher()
    document = json.loads(PRICES.read_text())
    for mutation in ({"provider": "RunPod"}, {"tiers": []}, {"hours_per_month": 730}):
        broken = json.loads(json.dumps(document))
        broken.update(mutation)
        with pytest.raises(AssertionError):
            fetcher.check_document(broken)


def test_model_size_labels_read_total_parameters():
    fetcher = load_fetcher()
    assert fetcher.total_parameters("30.7B DENSE · 256K CTX") == 30.7
    assert fetcher.total_parameters("2.78T · ANY-TO-ANY") == 2780.0
    assert fetcher.total_parameters("9B class · Long context") == 9.0
    assert fetcher.total_parameters("552B-8B MOE · 1M CTX") == 552.0
    assert fetcher.total_parameters("no size here") is None


def test_published_document_records_its_own_arithmetic():
    document = json.loads(PRICES.read_text())
    assert document["arithmetic"]["total_usd_hour"] == "dph_base (GPU rate) + disk_usd_hour"
    assert document["arithmetic"]["usd_month_24_7"] == "total_usd_hour * 720"
    assert "storage" in document["arithmetic"]["usd_stopped_month"]
    assert document["currency"] == "USD"
    assert document["endpoint"].startswith("https://")
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+00:00", document["generated_at"])
    for note in document["notes"]:
        assert note.strip()
