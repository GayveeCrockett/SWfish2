"""Reef Search backend tests - SWSA Habitat (fruit tanks) + theme iteration."""
import os
import pytest
import requests

BASE_URL = os.environ.get("EXPO_PUBLIC_BACKEND_URL", "https://fish-search-app.preview.emergentagent.com").rstrip("/")


@pytest.fixture
def api():
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    return s


# ---- Health ----
class TestHealth:
    def test_root(self, api):
        r = api.get(f"{BASE_URL}/api/")
        assert r.status_code == 200
        data = r.json()
        assert "fish_count" in data
        assert data["fish_count"] >= 92


# ---- /api/filters returns fruit names ----
class TestFilters:
    def test_filters_swsa_habitats_are_fruits(self, api):
        r = api.get(f"{BASE_URL}/api/filters")
        assert r.status_code == 200
        data = r.json()
        assert "swsa_habitats" in data
        assert sorted(data["swsa_habitats"]) == ["banana", "kiwi", "mango", "strawberry"]

    def test_filters_other_groups_present(self, api):
        r = api.get(f"{BASE_URL}/api/filters")
        data = r.json()
        for k in ["colors", "diets", "habitats", "conservation", "can_eat", "poison"]:
            assert k in data and len(data[k]) > 0


# ---- SWSA fruit counts ----
class TestSwsaFruitCounts:
    @pytest.mark.parametrize("fruit,expected", [
        ("banana", 7),
        ("mango", 13),
        ("kiwi", 48),
        ("strawberry", 24),
    ])
    def test_count(self, api, fruit, expected):
        r = api.get(f"{BASE_URL}/api/fishes", params={"swsa_habitats": fruit})
        assert r.status_code == 200
        data = r.json()
        assert data["count"] == expected, f"expected {expected} for {fruit}, got {data['count']}"
        for f in data["fishes"]:
            assert f["swsa_fruit"] == fruit
            assert fruit in [s.lower() for s in f["swsa_habitats"]]

    def test_banana_contents(self, api):
        r = api.get(f"{BASE_URL}/api/fishes", params={"swsa_habitats": "banana"})
        names = sorted([f["name"] for f in r.json()["fishes"]])
        expected = sorted([
            "clown fish", "koi", "flame angelfish", "freckletail lyretail",
            "black spot angelfish", "king angelfish", "asfur angelfish",
        ])
        assert names == expected


# ---- Fish detail ----
class TestFishDetail:
    def test_clown_fish_id_1(self, api):
        r = api.get(f"{BASE_URL}/api/fishes/1")
        assert r.status_code == 200
        f = r.json()
        assert f["name"] == "clown fish"
        assert f["swsa_fruit"] == "banana"
        assert f["swsa_habitats"] == ["banana"]
        assert f["image_url"].startswith("https://customer-assets.emergentagent.com/")
        assert "clown" in f["image_url"]

    def test_404(self, api):
        r = api.get(f"{BASE_URL}/api/fishes/999")
        assert r.status_code == 404


# ---- Regression: other filters still work ----
class TestRegression:
    def test_search_by_name(self, api):
        r = api.get(f"{BASE_URL}/api/fishes", params={"q": "clown"})
        assert r.status_code == 200
        names = [f["name"] for f in r.json()["fishes"]]
        assert "clown fish" in names

    def test_color_filter(self, api):
        r = api.get(f"{BASE_URL}/api/fishes", params={"colors": "red"})
        assert r.status_code == 200
        assert r.json()["count"] > 0

    def test_diet_filter(self, api):
        r = api.get(f"{BASE_URL}/api/fishes", params={"diets": "carnivore"})
        assert r.status_code == 200
        assert r.json()["count"] > 0

    def test_combined_swsa_and_color(self, api):
        r = api.get(f"{BASE_URL}/api/fishes", params=[("swsa_habitats", "banana"), ("colors", "orange")])
        assert r.status_code == 200
        # all returned fish must be banana tank AND have orange
        for f in r.json()["fishes"]:
            assert f["swsa_fruit"] == "banana"
            assert "orange" in f["colors"]
