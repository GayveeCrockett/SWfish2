"""Fish data loaded from the parsed Reef Search PDF dataset.

Verbatim PDF dataset built by `parse_verbatim.py`. All text fields are taken
literally from the source PDF (Sea World San Antonio: Explorer's Reef). The
backend does NO normalization or internet enrichment for text — only image
URLs are mapped through user-uploaded artifacts.
"""
from typing import List, Dict, Any
import json
from pathlib import Path

ROOT = Path(__file__).parent
_DATASET_PATH = ROOT / "fish_dataset.json"
_IMAGES_PATH = ROOT / "fish_images.json"
_SCI_PATH = ROOT / "scientific_names.json"

RAW_FISH: List[Dict[str, Any]] = json.loads(_DATASET_PATH.read_text())

try:
    _PDF_SCIENTIFIC: Dict[str, str] = json.loads(_SCI_PATH.read_text())
except FileNotFoundError:
    _PDF_SCIENTIFIC = {}

# Per-species image overrides (user uploads, mapped by common name).
_IMAGE_OVERRIDES: Dict[str, str] = {
    "orange clownfish": "https://customer-assets.emergentagent.com/job_fish-search-app/artifacts/9vuy2m5y_clown.jpg",
    "clown fish": "https://customer-assets.emergentagent.com/job_fish-search-app/artifacts/9vuy2m5y_clown.jpg",
    "agitated carpet anemone": "https://customer-assets.emergentagent.com/job_fish-search-app/artifacts/eyaq3k2z_Stichodactyla.jpg",
    "bicolor fox face": "https://customer-assets.emergentagent.com/job_fish-search-app/artifacts/9ex9ira3_Siganus%20uspi.jpg",
    "bignose unicorn tang": "https://customer-assets.emergentagent.com/job_fish-search-app/artifacts/u55sb0po_Naso%20vlamingii.webp",
    "black boring sea urchin": "https://customer-assets.emergentagent.com/job_fish-search-app/artifacts/0rt9clim_Echinometra%20mathaei.webp",
    "black brittlestar": "https://customer-assets.emergentagent.com/job_fish-search-app/artifacts/rgnqc4d6_Ophiocoma%20echinata.jpg",
}

# Manual scientific-name overrides — applied AFTER PDF lookup. Use these to
# correct OCR quirks or to set a canonical species for a generic PDF entry.
_SCIENTIFIC_NAMES: Dict[str, str] = {
    "turban snail": "Turbo marmoratus",
    "moon coral": "Acanthastrea faviaformis",
}

try:
    _WIKI_IMAGES: Dict[str, str] = json.loads(_IMAGES_PATH.read_text())
except FileNotFoundError:
    _WIKI_IMAGES = {}


def _parse_colors(desc: str) -> List[str]:
    if not desc:
        return []
    return [c.strip().lower() for c in desc.split(",") if c.strip()]


def _parse_swsa(raw) -> List[str]:
    """Split swsa habitat string like '2, turtle reef' into individual tags."""
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
    seen_sci: Dict[str, int] = {}  # canonical sci (lowercase) -> index in result
    for f in RAW_FISH:
        name = f.get("name", "")
        image_url = _IMAGE_OVERRIDES.get(name.lower()) or _IMAGE_OVERRIDES.get(name) or _WIKI_IMAGES.get(name, "")
        scientific = (
            _SCIENTIFIC_NAMES.get(name.lower())
            or _SCIENTIFIC_NAMES.get(name)
            or _PDF_SCIENTIFIC.get(name.lower())
            or _PDF_SCIENTIFIC.get(name, "")
        )
        # Dedup by scientific name (case-insensitive). First occurrence wins.
        sci_key = scientific.strip().lower()
        if sci_key and sci_key in seen_sci:
            continue
        swsa = _parse_swsa(f.get("swsa_hab"))
        record = {
            "id": str(len(result) + 1),
            "name": name,
            "scientific_name": scientific,
            "diet": (f.get("diet") or "").strip(),
            "longevity": (f.get("longevity") or "").strip(),
            "conservation_status": (f.get("conservation_status") or "").strip(),
            "poison_toxin": (f.get("poison_toxin") or "").strip(),
            "habitats": _parse_habitats(f.get("natural_hab", "")),
            "swsa_habitats": swsa,
            "swsa_fruit": swsa[0] if swsa else "",
            "natural_hab_raw": (f.get("natural_hab") or "").strip(),
            "swsa_hab_raw": ", ".join(swsa),
            "nifty_facts": (f.get("nifty_facts") or "").strip(),
            "can_eat": (f.get("can_eat") or "").strip(),
            "colors": _parse_colors(f.get("description", "")),
            "description": (f.get("description") or "").strip(),
            "image_url": image_url,
        }
        if sci_key:
            seen_sci[sci_key] = len(result)
        result.append(record)
    return result


FISHES: List[Dict[str, Any]] = build_fishes()


def all_filter_options() -> Dict[str, List[str]]:
    colors, diets, habitats, conservation, can_eat, poison = (
        set(), set(), set(), set(), set(), set()
    )
    # Case-insensitive de-dup for swsa using lowercase key -> first-seen display value.
    swsa_seen: Dict[str, str] = {}
    for f in FISHES:
        for c in f["colors"]:
            colors.add(c)
        if f["diet"]:
            diets.add(f["diet"])
        for h in f["habitats"]:
            if h:
                habitats.add(h)
        for h in f["swsa_habitats"]:
            key = h.strip().lower()
            if not key:
                continue
            if key not in swsa_seen:
                # Prefer the first lowercase canonical form
                swsa_seen[key] = h.strip().lower()
        if f["conservation_status"]:
            conservation.add(f["conservation_status"])
        if f["can_eat"]:
            can_eat.add(f["can_eat"])
        if f["poison_toxin"]:
            poison.add(f["poison_toxin"])
    return {
        "colors": sorted(colors),
        "diets": sorted(diets),
        "habitats": sorted(habitats),
        "swsa_habitats": sorted(swsa_seen.values()),
        "conservation": sorted(conservation),
        "can_eat": sorted(can_eat),
        "poison": sorted(poison),
    }
