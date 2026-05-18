"""Fish data loaded from the parsed Reef Search PDF dataset.

Static dataset built from `parse_pdf.py` (~340 species across the SWSA exhibits).
SWSA habitat is now a list of tank/gallery/reef tags (e.g. "Turtle Reef",
"Coral Reef", "Tank A", "Tank B", "Gallery 6", "Gallery 7", "Shark Tank",
"Tank 1"..."Tank 5"). The optional clown-fish image override stays in place.
"""
from typing import List, Dict, Any
import json
from pathlib import Path

ROOT = Path(__file__).parent
_DATASET_PATH = ROOT / "fish_dataset.json"
_IMAGES_PATH = ROOT / "fish_images.json"

RAW_FISH: List[Dict[str, Any]] = json.loads(_DATASET_PATH.read_text())

# The orange clownfish (most common reef clown fish) keeps the user-uploaded image
_IMAGE_OVERRIDES: Dict[str, str] = {
    "orange clownfish": "https://customer-assets.emergentagent.com/job_fish-search-app/artifacts/9vuy2m5y_clown.jpg",
    "clown fish": "https://customer-assets.emergentagent.com/job_fish-search-app/artifacts/9vuy2m5y_clown.jpg",
}

try:
    _WIKI_IMAGES: Dict[str, str] = json.loads(_IMAGES_PATH.read_text())
except FileNotFoundError:
    _WIKI_IMAGES = {}


def _normalize_diet(raw: str) -> str:
    # `parse_pdf.py` already normalises diet, but we keep this as a safety net.
    r = (raw or "").lower().strip()
    if r in {"omnivore", "carnivore", "herbivore", "planktivore",
             "zooplankton", "zooxanthellae", "filter feeder"}:
        return r
    return r


def _parse_colors(desc: str) -> List[str]:
    if not desc:
        return []
    return [c.strip().lower() for c in desc.split(",") if c.strip()]


def _parse_swsa(raw) -> List[str]:
    if isinstance(raw, list):
        return [str(x).strip() for x in raw if str(x).strip()]
    if not raw:
        return []
    return [c.strip() for c in str(raw).split(",") if c.strip()]


def _parse_habitats(raw: str) -> List[str]:
    if not raw:
        return []
    return [raw.strip()]


def build_fishes() -> List[Dict[str, Any]]:
    result = []
    for idx, f in enumerate(RAW_FISH):
        name = f.get("name", "")
        image_url = _IMAGE_OVERRIDES.get(name) or _WIKI_IMAGES.get(name, "")
        swsa = _parse_swsa(f.get("swsa_hab"))
        result.append({
            "id": str(idx + 1),
            "name": name,
            "diet": _normalize_diet(f.get("diet", "")),
            "longevity": f.get("longevity", "") or "Unknown",
            "conservation_status": f.get("conservation_status", "") or "Unknown",
            "poison_toxin": (f.get("poison_toxin") or "no").lower(),
            "habitats": _parse_habitats(f.get("natural_hab", "")),
            "swsa_habitats": swsa,
            "swsa_fruit": swsa[0] if swsa else "",
            "natural_hab_raw": f.get("natural_hab", ""),
            "swsa_hab_raw": ", ".join(swsa),
            "nifty_facts": (f.get("nifty_facts") or "").strip(),
            "can_eat": f.get("can_eat", "") or "Unknown",
            "colors": _parse_colors(f.get("description", "")),
            "description": f.get("description", ""),
            "image_url": image_url,
        })
    return result


FISHES: List[Dict[str, Any]] = build_fishes()


def all_filter_options() -> Dict[str, List[str]]:
    colors, diets, habitats, swsa, conservation, can_eat, poison = (
        set(), set(), set(), set(), set(), set(), set()
    )
    for f in FISHES:
        for c in f["colors"]:
            colors.add(c)
        if f["diet"]:
            diets.add(f["diet"])
        for h in f["habitats"]:
            if h:
                habitats.add(h)
        for h in f["swsa_habitats"]:
            swsa.add(h)
        if f["conservation_status"]:
            conservation.add(f["conservation_status"])
        if f["can_eat"]:
            can_eat.add(f["can_eat"])
        poison.add(f["poison_toxin"])
    return {
        "colors": sorted(colors),
        "diets": sorted(diets),
        "habitats": sorted(habitats),
        "swsa_habitats": sorted(swsa),
        "conservation": sorted(conservation),
        "can_eat": sorted(can_eat),
        "poison": sorted(poison),
    }
