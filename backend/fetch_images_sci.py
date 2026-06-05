"""Fetch Wikipedia/Wikimedia images for each fish using its scientific name.

Lookup order:
  1. Wikipedia REST summary by exact scientific name (Genus_species).
  2. Wikipedia REST summary by genus only (first word of scientific name).
  3. Wikipedia search API (best match title) then summary on that title.
  4. Common-name lookup as a last resort.

The resulting URL is the Wikipedia "thumbnail" or "originalimage" source which is
already a Wikimedia Commons CDN URL — safe to embed.

Run:  python fetch_images_sci.py        (resumes existing cache, only fills missing)
      python fetch_images_sci.py --all  (refetch everything)
"""
import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
DATASET = ROOT / "fish_dataset.json"
SCI_NAMES = ROOT / "scientific_names.json"
IMAGE_CACHE = ROOT / "fish_images.json"

HEADERS = {"User-Agent": "ExplorersReefApp/1.0 (contact: dev@seaworld.com)"}
SUMMARY_API = "https://en.wikipedia.org/api/rest_v1/page/summary/"
SEARCH_API = "https://en.wikipedia.org/w/api.php?action=query&list=search&format=json&srlimit=3&srsearch="


def _fetch_json(url: str, timeout: int = 8):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8", errors="ignore"))
    except Exception as e:
        return None


def summary_image(title: str):
    """Return image URL for a Wikipedia page title, or None."""
    if not title:
        return None
    url = SUMMARY_API + urllib.parse.quote(title.replace(" ", "_"))
    data = _fetch_json(url)
    if not data:
        return None
    # Skip disambiguation pages
    if data.get("type") == "disambiguation":
        return None
    thumb = data.get("originalimage") or data.get("thumbnail")
    if thumb and thumb.get("source"):
        return thumb["source"]
    return None


def search_first_image(query: str):
    """Use Wikipedia search to find the most-relevant title and fetch its image."""
    if not query:
        return None
    url = SEARCH_API + urllib.parse.quote(query)
    data = _fetch_json(url)
    if not data:
        return None
    hits = (data.get("query") or {}).get("search") or []
    for hit in hits[:3]:
        title = hit.get("title")
        if not title:
            continue
        # Skip obvious junk
        low = title.lower()
        if "list of" in low or "wikipedia" in low:
            continue
        img = summary_image(title)
        if img:
            return img
    return None


def resolve_image(common_name: str, scientific: str) -> str:
    """Try multiple strategies to find a fitting image."""
    # 1) Exact scientific name
    if scientific:
        img = summary_image(scientific)
        if img:
            return img
        # 2) Genus only (first token)
        genus = scientific.split()[0] if " " in scientific else None
        if genus:
            img = summary_image(genus)
            if img:
                return img
        # 3) Search by scientific name
        img = search_first_image(scientific)
        if img:
            return img
    # 4) Search/lookup by common name
    img = summary_image(common_name)
    if img:
        return img
    img = search_first_image(common_name)
    return img or ""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true", help="Refetch all entries")
    parser.add_argument("--limit", type=int, default=0, help="Stop after N updates (0=no limit)")
    args = parser.parse_args()

    dataset = json.loads(DATASET.read_text())
    sci_map = json.loads(SCI_NAMES.read_text())
    cache = {}
    if IMAGE_CACHE.exists() and not args.all:
        try:
            cache = json.loads(IMAGE_CACHE.read_text())
        except Exception:
            cache = {}

    updated = 0
    for i, fish in enumerate(dataset):
        name = fish["name"]
        sci = sci_map.get(name.lower(), "").strip()
        cached = cache.get(name)
        if cached and not args.all:
            # Already have an image — skip unless --all
            continue
        img = resolve_image(name, sci)
        cache[name] = img
        updated += 1
        marker = "✓" if img else "·"
        print(f"  [{i+1:3d}/{len(dataset)}] {marker} {name!r:50s} sci={sci!r:40s} img={img[:60]!r}")
        # Persist every 25 fish so progress survives interruption
        if updated % 25 == 0:
            IMAGE_CACHE.write_text(json.dumps(cache, indent=2, sort_keys=True))
        if args.limit and updated >= args.limit:
            break
        # Be polite to Wikipedia
        time.sleep(0.15)

    IMAGE_CACHE.write_text(json.dumps(cache, indent=2, sort_keys=True))
    have = sum(1 for v in cache.values() if v)
    print(f"\nDone. Cache has {have}/{len(cache)} entries with images.")


if __name__ == "__main__":
    main()
