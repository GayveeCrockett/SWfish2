"""Backend tests for the Reef Search FastAPI.

Tests hit the deployed URL inferred from the frontend env via /api prefix.
"""
import os
import sys
import json
from pathlib import Path

import requests

# Resolve backend URL from frontend env
FRONTEND_ENV = Path("/app/frontend/.env")
BASE_URL = None
for line in FRONTEND_ENV.read_text().splitlines():
    if line.startswith("EXPO_PUBLIC_BACKEND_URL="):
        BASE_URL = line.split("=", 1)[1].strip().strip('"')
        break

assert BASE_URL, "EXPO_PUBLIC_BACKEND_URL must be set in /app/frontend/.env"
API = BASE_URL.rstrip("/") + "/api"

print(f"Testing API at: {API}\n")

failures = []
passes = []


def record(name, ok, msg=""):
    if ok:
        passes.append(name)
        print(f"PASS  {name}")
    else:
        failures.append((name, msg))
        print(f"FAIL  {name}: {msg}")


def test_root():
    r = requests.get(f"{API}/", timeout=30)
    if r.status_code != 200:
        record("GET /api/ status", False, f"status={r.status_code} body={r.text[:200]}")
        return
    data = r.json()
    fc = data.get("fish_count")
    record("GET /api/ status 200", True)
    if isinstance(fc, int) and fc >= 410:
        record(f"GET /api/ fish_count>=410 (got {fc})", True)
    else:
        record("GET /api/ fish_count>=410", False, f"got fish_count={fc}")


def test_achilles():
    r = requests.get(f"{API}/fishes", params={"q": "achilles"}, timeout=30)
    if r.status_code != 200:
        record("GET /api/fishes?q=achilles status", False, f"status={r.status_code}")
        return
    data = r.json()
    fishes = data.get("fishes", [])
    if len(fishes) != 1:
        record("achilles search returns exactly 1 fish", False, f"got {len(fishes)} fishes: {[f.get('name') for f in fishes]}")
        # Try to still validate the achilles tang record if present
        match = next((f for f in fishes if f.get("name", "").lower() == "achilles tang"), None)
        if not match:
            return
    else:
        match = fishes[0]
        record("achilles search returns exactly 1 fish", True)

    expectations = {
        "name": "achilles tang",
        "diet": "Omnivore",
        "longevity": "15 years",
        "conservation_status": "LC",
        "poison_toxin": "no",
        "scientific_name": "Acanthurus achilles",
    }
    for field, expected in expectations.items():
        actual = match.get(field)
        if actual == expected:
            record(f"achilles.{field} == {expected!r}", True)
        else:
            record(f"achilles.{field}", False, f"expected {expected!r}, got {actual!r}")

    nifty = (match.get("nifty_facts") or "").lower()
    if "scalpel" in nifty:
        record("achilles.nifty_facts contains 'scalpel'", True)
    else:
        record("achilles.nifty_facts contains 'scalpel'", False, f"nifty_facts={match.get('nifty_facts')!r}")

    colors = [c.lower() for c in (match.get("colors") or [])]
    for needed in ["black", "blue", "orange"]:
        if needed in colors:
            record(f"achilles.colors contains '{needed}'", True)
        else:
            record(f"achilles.colors contains '{needed}'", False, f"colors={match.get('colors')}")

    # Save id for later
    return match.get("id")


def test_clown():
    r = requests.get(f"{API}/fishes", params={"q": "clown"}, timeout=30)
    if r.status_code != 200:
        record("GET /api/fishes?q=clown status", False, f"status={r.status_code}")
        return
    data = r.json()
    fishes = data.get("fishes", [])
    if len(fishes) >= 5:
        record(f"clown search returns >=5 (got {len(fishes)})", True)
    else:
        record("clown search returns >=5", False, f"got {len(fishes)}: {[f.get('name') for f in fishes]}")

    clown = next((f for f in fishes if f.get("name", "").lower() == "clown fish"), None)
    if clown is None:
        record("clown search includes 'clown fish'", False, f"names={[f.get('name') for f in fishes]}")
        return
    record("clown search includes 'clown fish'", True)
    img = clown.get("image_url", "")
    if "customer-assets" in img:
        record("clown fish image_url contains 'customer-assets'", True)
    else:
        record("clown fish image_url contains 'customer-assets'", False, f"image_url={img!r}")


def test_filters():
    r = requests.get(f"{API}/filters", timeout=30)
    if r.status_code != 200:
        record("GET /api/filters status", False, f"status={r.status_code}")
        return
    data = r.json()
    required_keys = ["colors", "diets", "swsa_habitats", "conservation", "can_eat", "poison", "habitats"]
    for k in required_keys:
        if k not in data:
            record(f"filters has key '{k}'", False, f"keys={list(data.keys())}")
            continue
        if not isinstance(data[k], list) or len(data[k]) == 0:
            record(f"filters['{k}'] non-empty list", False, f"value={data[k]!r}")
        else:
            record(f"filters['{k}'] non-empty list ({len(data[k])} items)", True)

    diets = data.get("diets", [])
    for d in ["Omnivore", "Carnivore", "Herbivore"]:
        if d in diets:
            record(f"filters.diets contains {d!r}", True)
        else:
            record(f"filters.diets contains {d!r}", False, f"diets={diets}")

    conservation = data.get("conservation", [])
    if "LC" in conservation:
        record("filters.conservation contains 'LC'", True)
    else:
        record("filters.conservation contains 'LC'", False, f"conservation={conservation}")

    can_eat = data.get("can_eat", [])
    for ce in ["Technically", "NO!"]:
        if ce in can_eat:
            record(f"filters.can_eat contains {ce!r}", True)
        else:
            record(f"filters.can_eat contains {ce!r}", False, f"can_eat={can_eat}")


def test_swsa_turtle_reef():
    r = requests.get(f"{API}/fishes", params={"swsa_habitats": "turtle reef"}, timeout=30)
    if r.status_code != 200:
        record("GET /api/fishes?swsa_habitats=turtle+reef status", False, f"status={r.status_code}")
        return
    data = r.json()
    fishes = data.get("fishes", [])
    if len(fishes) >= 5:
        record(f"turtle reef filter returns >=5 (got {len(fishes)})", True)
    else:
        record("turtle reef filter returns >=5", False, f"got {len(fishes)}")

    bad = []
    for f in fishes:
        habs = [h.lower() for h in (f.get("swsa_habitats") or [])]
        if "turtle reef" not in habs:
            bad.append((f.get("name"), f.get("swsa_habitats")))
    if not bad:
        record("All returned fish have 'turtle reef' in swsa_habitats", True)
    else:
        record("All returned fish have 'turtle reef' in swsa_habitats", False, f"violations: {bad[:5]}")


def test_get_by_id():
    r = requests.get(f"{API}/fishes/1", timeout=30)
    if r.status_code != 200:
        record("GET /api/fishes/1 status", False, f"status={r.status_code}")
        return
    fish = r.json()
    if fish.get("name", "").lower() == "achilles tang":
        record("GET /api/fishes/1 returns achilles tang", True)
    else:
        record("GET /api/fishes/1 returns achilles tang", False, f"name={fish.get('name')!r}")

    fields = ["id", "name", "scientific_name", "diet", "longevity",
              "conservation_status", "poison_toxin", "habitats", "swsa_habitats",
              "nifty_facts", "can_eat", "colors", "description", "image_url"]
    missing = []
    for fld in fields:
        if fld not in fish:
            missing.append(fld)
    if missing:
        record("GET /api/fishes/1 has all fields present", False, f"missing={missing}")
    else:
        record("GET /api/fishes/1 has all standard fields present", True)

    # Check values are populated for the key ones
    important = ["name", "scientific_name", "diet", "longevity", "conservation_status",
                 "poison_toxin", "nifty_facts", "can_eat", "description"]
    empties = [k for k in important if not (fish.get(k) or "").strip()]
    if empties:
        record("GET /api/fishes/1 important text fields populated", False, f"empty fields: {empties}")
    else:
        record("GET /api/fishes/1 important text fields populated", True)


if __name__ == "__main__":
    print("=" * 60)
    print("1) GET /api/")
    print("=" * 60)
    test_root()

    print("\n" + "=" * 60)
    print("2) GET /api/fishes?q=achilles")
    print("=" * 60)
    test_achilles()

    print("\n" + "=" * 60)
    print("3) GET /api/fishes?q=clown")
    print("=" * 60)
    test_clown()

    print("\n" + "=" * 60)
    print("4) GET /api/filters")
    print("=" * 60)
    test_filters()

    print("\n" + "=" * 60)
    print("5) GET /api/fishes?swsa_habitats=turtle+reef")
    print("=" * 60)
    test_swsa_turtle_reef()

    print("\n" + "=" * 60)
    print("6) GET /api/fishes/1")
    print("=" * 60)
    test_get_by_id()

    print("\n" + "=" * 60)
    print(f"RESULTS: {len(passes)} passed, {len(failures)} failed")
    print("=" * 60)
    if failures:
        for name, msg in failures:
            print(f"  FAIL  {name}: {msg}")
        sys.exit(1)
    sys.exit(0)
