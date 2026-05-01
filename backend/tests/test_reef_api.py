"""Backend API tests for Reef Search."""
import os
import pytest
import requests

BASE_URL = os.environ.get("EXPO_PUBLIC_BACKEND_URL", "https://fish-search-app.preview.emergentagent.com").rstrip("/")


@pytest.fixture
def client():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s


# Health
def test_root(client):
    r = client.get(f"{BASE_URL}/api/")
    assert r.status_code == 200
    data = r.json()
    assert "fish_count" in data
    assert data["fish_count"] == 89


# Filters
def test_filters(client):
    r = client.get(f"{BASE_URL}/api/filters")
    assert r.status_code == 200
    data = r.json()
    for k in ["colors", "diets", "habitats", "conservation", "can_eat", "poison"]:
        assert k in data and isinstance(data[k], list) and len(data[k]) > 0


# List all
def test_list_all_fishes(client):
    r = client.get(f"{BASE_URL}/api/fishes")
    assert r.status_code == 200
    d = r.json()
    assert d["count"] == 89
    assert len(d["fishes"]) == 89
    f0 = d["fishes"][0]
    for k in ["id", "name", "diet", "colors", "habitats", "conservation_status", "poison_toxin", "can_eat"]:
        assert k in f0


# Search by name
def test_search_clown(client):
    r = client.get(f"{BASE_URL}/api/fishes", params={"q": "clown"})
    assert r.status_code == 200
    d = r.json()
    assert d["count"] >= 1
    for f in d["fishes"]:
        assert "clown" in f["name"].lower()


# Multi-filter colors + diet
def test_multi_filter(client):
    r = client.get(f"{BASE_URL}/api/fishes", params=[("colors", "orange"), ("diets", "omnivore")])
    assert r.status_code == 200
    d = r.json()
    for f in d["fishes"]:
        assert "orange" in [c.lower() for c in f["colors"]]
        assert f["diet"].lower() == "omnivore"


# Poison filter
def test_poison_yes(client):
    r = client.get(f"{BASE_URL}/api/fishes", params={"poison": "yes"})
    assert r.status_code == 200
    d = r.json()
    assert d["count"] >= 1
    for f in d["fishes"]:
        assert f["poison_toxin"].lower() == "yes"


# Get single fish
def test_get_fish_1(client):
    r = client.get(f"{BASE_URL}/api/fishes/1")
    assert r.status_code == 200
    f = r.json()
    assert f["id"] == "1"
    for k in ["name", "diet", "longevity", "conservation_status", "poison_toxin", "habitats", "can_eat", "colors"]:
        assert k in f


# 404
def test_get_fish_404(client):
    r = client.get(f"{BASE_URL}/api/fishes/99999")
    assert r.status_code == 404
