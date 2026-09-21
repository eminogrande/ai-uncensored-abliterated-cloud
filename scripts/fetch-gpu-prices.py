#!/usr/bin/env python3
"""Refresh the public self-hosting price table from live Vast.ai offers.

Read-only. No account key is used, nothing is rented, started or stopped.
Writes `website/.well-known/gpu-prices.json`, which the website build renders
into the model-size cost table.

    python3 -I scripts/fetch-gpu-prices.py            # refresh
    python3 -I scripts/fetch-gpu-prices.py --check     # verify committed data

The arithmetic is documented in the output file so the numbers can be checked
by hand:

    disk_usd_hour  = storage_cost_usd_per_gb_month / 720
    total_usd_hour = dph_base (GPU) + disk_usd_hour
    day            = total_usd_hour * 24
    month_24_7     = total_usd_hour * 720
    month_2h_day   = dph_base * 60 + storage_cost * disk_gb
    stopped_month  = storage_cost * disk_gb        (disk only, GPU stopped)

Verified against the retained operator instance 49433042 (A100 PCIe 40 GB,
120 GB disk, storage_cost 0.20/GB-month): 0.6 + 0.2 * 120 / 720 = 0.633333,
which equals the provider's own `dph_total`.
"""
from __future__ import annotations

import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "website" / ".well-known" / "gpu-prices.json"
POSTS = ROOT / "website" / "blog" / "posts.json"
API = "https://console.vast.ai/api/v0/bundles/"
HOURS_PER_MONTH = 720
ATTEMPTS = 3

# A tier is one model-size class: the cheapest supported single or multi-GPU
# offer that can hold the weights plus context headroom. Ranges are the VRAM
# window searched; `disk_gb` is the container disk requested for the model
# file, runtime and a second model swap.
TIERS = [
    ("Up to 14B", 1, 8192, 16384, 40, 0.98),
    ("27-35B", 1, 24576, 49152, 70, 0.98),
    ("70-80B", 1, 49152, 73728, 92, 0.97),
    ("118-120B MoE", 1, 73728, 131072, 120, 0.98),
    ("180-400B MoE", 2, 73728, 131072, 450, 0.98),
    ("550B-1T", 4, 73728, 131072, 800, 0.98),
    ("1T and larger", 8, 65536, 131072, 1600, 0.98),
]

# Excluded GPU families, with the reason kept next to the name so the filter
# can be audited instead of guessed at. These cards either cannot run the
# current llama.cpp CUDA build (pre-Pascal architectures) or are mining-only
# silicon sold without display or vendor support.
EXCLUDED_GPU_FAMILIES = [
    ("GTX TITAN", "Maxwell, no supported CUDA build"),
    ("Titan Xp", "Pascal, no supported CUDA build"),
    ("Titan V", "Volta datacentre card, not offered for serving"),
    ("Titan X", "Maxwell, no supported CUDA build"),
    ("Tesla P100", "Pascal datacentre card, no display output"),
    ("Tesla P40", "Pascal datacentre card, no display output"),
    ("Tesla M40", "Maxwell, no supported CUDA build"),
    ("CMP 170HX", "mining-only silicon, no vendor support"),
    ("Quadro P", "Pascal workstation, no supported CUDA build"),
    ("GTX 10", "Pascal and older, no supported CUDA build"),
    ("GTX 16", "Turing consumer, unsupported by current llama.cpp builds"),
    ("K80", "Kepler, no supported CUDA build"),
    ("M40", "Maxwell, no supported CUDA build"),
]


def total_parameters(kicker: str) -> float | None:
    """Read the total parameter count out of a post kicker such as 30.7B or 2.78T."""
    match = re.match(r"^([\d.]+)\s*([BT])\b", kicker)
    if not match:
        return None
    value = float(match.group(1))
    return value * 1000 if match.group(2) == "T" else value


def weight_gb_at_q4(params_b: float) -> float:
    """Approximate Q4_K_M size: 4.5 bits per parameter plus container overhead."""
    return params_b * 4.5 / 8


def model_tiers() -> list[tuple[str, float]]:
    """(label, total parameters in billions) for every published model post."""
    posts = json.loads(POSTS.read_text())
    rows = []
    for post in posts:
        params = total_parameters(post.get("kicker", ""))
        if params is not None:
            rows.append((post["model_id"], params))
    return rows


def short_name(model_id: str) -> str:
    name = model_id.split("/")[-1]
    for suffix in ("-GGUF", "-FP8", "-NVFP4", "-W4A16", "-Q6_K", "-Q5_K_M", "-Q4_K_M"):
        name = name.replace(suffix, "")
    return name[:34]


def tier_label_for(params_b: float) -> str:
    weights = weight_gb_at_q4(params_b)
    if weights <= 48:
        return "Up to 14B" if weights <= 10 else "27-35B" if weights <= 24 else "70-80B"
    if weights <= 82:
        return "118-120B MoE"
    if weights <= 190:
        return "180-400B MoE"
    return "550B-1T" if weights <= 380 else "1T and larger"


def fetch_offers(gpus: int, low_mb: int, high_mb: int, disk_gb: int, reliability: float) -> list[dict]:
    query = {
        "gpu_ram": {"gte": low_mb, "lte": high_mb},
        "num_gpus": {"gte": gpus},
        "rentable": {"eq": True},
        "rented": {"eq": False},
        "reliability": {"gte": reliability},
        "disk_space": {"gte": disk_gb},
    }
    url = API + "?" + urllib.parse.urlencode({"q": json.dumps(query)})
    last_error: Exception | None = None
    for attempt in range(ATTEMPTS):
        try:
            with urllib.request.urlopen(url, timeout=120) as response:
                return json.loads(response.read()).get("offers", [])
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
            last_error = error
            time.sleep(3 * (attempt + 1))
    raise SystemExit(f"Vast.ai offer search failed after {ATTEMPTS} attempts: {last_error}")


def excluded(offer: dict) -> bool:
    name = offer.get("gpu_name") or ""
    return any(family in name for family, _ in EXCLUDED_GPU_FAMILIES)


def build_row(label: str, gpus: int, low_mb: int, high_mb: int, disk_gb: int, reliability: float) -> dict:
    offers = [offer for offer in fetch_offers(gpus, low_mb, high_mb, disk_gb, reliability) if not excluded(offer)]
    offers.sort(key=lambda offer: offer.get("dph_total") or 0)
    if not offers:
        raise SystemExit(f"No supported offer matched tier {label!r}; the marketplace changed.")
    best = offers[0]
    gpu_hour = float(best["dph_base"])
    storage_gb_month = float(best.get("storage_cost") or 0)
    disk_hour = storage_gb_month * disk_gb / HOURS_PER_MONTH
    total_hour = gpu_hour + disk_hour
    # Round once, from the exact values, so every published number is the same
    # precision the arithmetic produced rather than a re-rounded artefact.
    return {
        "label": label,
        "gpus": int(best.get("num_gpus") or gpus),
        "vram_per_gpu_mb": int(best.get("gpu_ram") or 0),
        "disk_gb": disk_gb,
        "gpu_name": best["gpu_name"],
        "offer_id": int(best["id"]),
        "location": best.get("geolocation") or "unknown",
        "reliability": round(float(best.get("reliability") or 0), 4),
        "gpu_usd_hour": gpu_hour,
        "disk_usd_hour": disk_hour,
        "total_usd_hour": total_hour,
        "usd_day": total_hour * 24,
        "usd_month_24_7": total_hour * HOURS_PER_MONTH,
        "usd_month_2h_day": gpu_hour * 60 + storage_gb_month * disk_gb,
        "usd_stopped_month": storage_gb_month * disk_gb,
        "offers_in_tier": len(offers),
    }


def build_document() -> dict:
    tiers = []
    for label, gpus, low_mb, high_mb, disk_gb, reliability in TIERS:
        tiers.append(build_row(label, gpus, low_mb, high_mb, disk_gb, reliability))
        time.sleep(1)  # be a polite client of the public search endpoint

    models = model_tiers()
    by_tier: dict[str, list[str]] = {label: [] for label, *_ in TIERS}
    for model_id, params in models:
        by_tier[tier_label_for(params)].append(model_id)
    for row in tiers:
        names = [short_name(name) for name in by_tier[row["label"]]]
        row["example_models"] = names[:3]
        row["covered_models"] = len(names)
        row["more_models"] = max(0, len(names) - 3)
    return {
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "provider": "Vast.ai",
        "endpoint": API,
        "method": "GET public bundles search, read-only. No account key, no instance created, started or stopped.",
        "currency": "USD",
        "hours_per_month": HOURS_PER_MONTH,
        "arithmetic": {
            "disk_usd_hour": "storage_cost_usd_per_gb_month / 720",
            "total_usd_hour": "dph_base (GPU rate) + disk_usd_hour",
            "usd_day": "total_usd_hour * 24",
            "usd_month_24_7": "total_usd_hour * 720",
            "usd_month_2h_day": "dph_base * 60 + storage_cost * disk_gb",
            "usd_stopped_month": "storage_cost * disk_gb",
        },
        "filters": {
            "rentable": True,
            "rented": False,
            "reliability_gte": 0.98,
            "tier_70_80b_reliability_gte": 0.97,
            "excluded_gpu_families": [
                {"family": family, "reason": reason} for family, reason in EXCLUDED_GPU_FAMILIES
            ],
        },
        "tiers": tiers,
        "notes": [
            "Prices are live marketplace quotes for the cheapest matching offer at the moment of the fetch, not a reservation or a quote for your account.",
            "Offers change by the minute and can disappear while you read the table; the fetch timestamp is the only honest date.",
            "GPU time is billed while running, even without requests. Storage is billed continuously, including while the instance is stopped.",
            "Bandwidth, taxes and other provider services are excluded.",
            "A tier is a size class for Q4-style GGUF weights plus context headroom, not a compatibility guarantee. Check the model card and the runtime before renting.",
        ],
    }


def check_document(document: dict) -> None:
    assert document["provider"] == "Vast.ai", "unexpected provider"
    assert document["hours_per_month"] == 720, "unexpected month length"
    assert len(document["tiers"]) == len(TIERS), "tier count changed"
    labels = [row["label"] for row in document["tiers"]]
    assert labels == [label for label, *_ in TIERS], "tier order changed"
    for row in document["tiers"]:
        # Every published figure must be re-derivable from the components the
        # table shows. Tolerate at most one cent of rounding, nothing more.
        recomputed_hour = row["gpu_usd_hour"] + row["disk_usd_hour"]
        assert abs(recomputed_hour - row["total_usd_hour"]) <= 1e-5, row["label"]
        for key, exact in (
            ("usd_day", recomputed_hour * 24),
            ("usd_month_24_7", recomputed_hour * HOURS_PER_MONTH),
            ("usd_month_2h_day", row["gpu_usd_hour"] * 60 + row["usd_stopped_month"]),
        ):
            assert abs(exact - row[key]) <= 0.01, (row["label"], key, row[key], exact)
        assert row["gpus"] >= 1 and row["vram_per_gpu_mb"] > 0 and row["disk_gb"] > 0, row["label"]
        assert row["gpu_usd_hour"] > 0 and row["offers_in_tier"] >= 1, row["label"]
        assert 0 < row["reliability"] <= 1, row["label"]
        # A tier may legitimately have no published model yet. The size class is
        # the row's subject, so examples are optional and never invented.
    datetime.fromisoformat(document["generated_at"])
    covered = sum(row["covered_models"] for row in document["tiers"])
    assert covered == len(model_tiers()), (covered, len(model_tiers()))


def main() -> None:
    if "--check" in sys.argv:
        check_document(json.loads(OUTPUT.read_text()))
        print(f"Checked {len(json.loads(OUTPUT.read_text())['tiers'])} price tiers in {OUTPUT.name}.")
        return
    document = build_document()
    check_document(document)
    OUTPUT.write_text(json.dumps(document, indent=2) + "\n")
    print(f"Wrote {len(document['tiers'])} price tiers to {OUTPUT.relative_to(ROOT)}.")


if __name__ == "__main__":
    main()
