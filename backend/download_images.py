"""Download every Wikipedia image referenced in fish_images.json to local disk
and rewrite the mapping so the app serves them from /api/images/<hash>.<ext>.

Customer-uploaded images (customer-assets.emergentagent.com) are left alone —
we don't want to lose the mapping to the original artifact host.
"""
import hashlib
import json
import mimetypes
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
CACHE = ROOT / "fish_images.json"
IMAGES_DIR = ROOT / "static" / "images"
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

# Prefix that the FastAPI server exposes for the images mount.
LOCAL_PREFIX = "/api/images/"

HEADERS = {"User-Agent": "ExplorersReefApp/1.0 (contact: dev@seaworld.com)"}


def _hash_url(url: str) -> str:
    return hashlib.md5(url.encode("utf-8")).hexdigest()


def _extension_for(url: str, content_type: str = "") -> str:
    # Prefer extension from the URL if it looks like a real image file.
    path = urllib.parse.urlparse(url).path
    if "." in path.rsplit("/", 1)[-1]:
        ext = "." + path.rsplit(".", 1)[-1].split("?")[0].lower()
        # Strip any funky query junk
        ext = ext.split("%")[0]
        if len(ext) <= 6 and ext[1:].isalnum():
            return ext
    guessed = mimetypes.guess_extension(content_type.split(";")[0].strip()) or ""
    return guessed or ".jpg"


def _download(url: str, dest: Path) -> bool:
    req = urllib.request.Request(url, headers=HEADERS)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read()
                dest.write_bytes(data)
                return True
        except Exception as e:
            print(f"    attempt {attempt+1} failed: {e}")
            time.sleep(1.5 + attempt)
    return False


def main():
    cache = json.loads(CACHE.read_text())
    updated = {}
    downloaded = 0
    kept_remote = 0
    already_local = 0
    failed = []

    # Group by URL so we don't re-download duplicates.
    url_to_local = {}

    total = len(cache)
    for i, (name, url) in enumerate(cache.items(), 1):
        # Preserve user-uploaded customer-assets URLs
        if not url:
            updated[name] = ""
            continue
        if url.startswith(LOCAL_PREFIX) or url.startswith("http://") is False and url.startswith("https://") is False and url.startswith("/"):
            updated[name] = url
            already_local += 1
            continue
        if "customer-assets.emergentagent.com" in url:
            updated[name] = url
            kept_remote += 1
            continue
        if url in url_to_local:
            updated[name] = url_to_local[url]
            continue

        h = _hash_url(url)
        # Try to determine extension without doing a HEAD first (just use URL suffix).
        ext = _extension_for(url)
        filename = f"{h}{ext}"
        dest = IMAGES_DIR / filename
        local_url = LOCAL_PREFIX + filename
        if dest.exists() and dest.stat().st_size > 0:
            url_to_local[url] = local_url
            updated[name] = local_url
            already_local += 1
            continue

        print(f"  [{i:3d}/{total}] downloading {name!r} <- {url[:80]}")
        ok = _download(url, dest)
        if ok:
            url_to_local[url] = local_url
            updated[name] = local_url
            downloaded += 1
        else:
            # Fall back to the remote URL — better than nothing
            updated[name] = url
            failed.append((name, url))

        # Persist every 20 fetches
        if downloaded and downloaded % 20 == 0:
            CACHE.write_text(json.dumps(updated, indent=2, sort_keys=True))
        time.sleep(0.1)

    CACHE.write_text(json.dumps(updated, indent=2, sort_keys=True))
    print("\n=== SUMMARY ===")
    print(f"  Downloaded: {downloaded}")
    print(f"  Already local: {already_local}")
    print(f"  Kept remote (customer-assets): {kept_remote}")
    print(f"  Failed: {len(failed)}")
    for name, url in failed[:20]:
        print(f"    - {name}: {url}")


if __name__ == "__main__":
    main()
