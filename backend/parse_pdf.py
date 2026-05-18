"""Parse the reef-search PDF text-layout output into a structured JSON file.

The PDF table is messy (column wrapping), but each fish row starts with a
line containing the fish name in the leftmost column, followed by an 'Omnivore'
/ 'Carnivore' / 'Herbivore' / 'Planktiv' / 'Zooxan' / 'Filter fe' / etc. token
somewhere on the same line or the next. We use that diet token as the anchor
to chunk rows. Then we extract the easy fields with regex from the row text.
"""
import json
import re
from pathlib import Path

SRC = Path("/tmp/reef.txt")
OUT = Path("/app/backend/fish_dataset.json")

DIET_TOKENS = ["Omnivore", "Carnivore", "Herbivore", "Planktivore", "Plankivore",
               "Plankiv", "Zooxan", "Zoopla", "Filter fe", "omnivo", "carnivo",
               "carnive", "zooplar", "zoopl"]
DIET_RE = re.compile(r"\b(" + "|".join(re.escape(t) for t in DIET_TOKENS) + r")\w*", re.I)

CONS_TOKENS = ["LC", "NT", "VU", "EN", "DD", "CR", "Varies", "no status", "?"]
LONG_RE = re.compile(r"\b(\d+\+?\s*[-–]?\s*\d*\+?\s*(?:year|years|yr))", re.I)
LONG_ALT_RE = re.compile(r"\b(Unknown|unknown)\b")
POISON_RE = re.compile(r"\b(yes|no)\b", re.I)
EAT_RE = re.compile(r"(Technically|NO!|N/A)", re.I)
COLOR_TOKENS = {"orange", "yellow", "red", "pink", "purple", "blue", "green",
                "black", "white", "brown", "silver", "tan", "gold"}


def parse_text(text: str):
    # Drop the header/title preamble before first real fish row
    lines = text.splitlines()
    # Stitch wrapped table rows: a "row" starts when a line begins at column 0
    # with a lowercase letter or capital (fish name) — and subsequent lines are
    # continuations if they're indented or shorter than ~20 chars.
    blocks = []
    current: list[str] = []
    for line in lines:
        if not line.strip():
            if current:
                blocks.append(" ".join(current))
                current = []
            continue
        # New block if line starts at column 0 with alpha char and we already
        # have content
        starts_fresh = bool(line) and not line[0].isspace() and line[0].isalpha()
        if starts_fresh and current:
            blocks.append(" ".join(current))
            current = [line.rstrip()]
        else:
            current.append(line.rstrip())
    if current:
        blocks.append(" ".join(current))

    fishes = []
    for blk in blocks:
        m = DIET_RE.search(blk)
        if not m:
            continue
        # Fish name = everything before the diet token (cleaned)
        name = blk[: m.start()].strip().lower()
        if not name or len(name) > 50 or any(c.isdigit() for c in name):
            continue
        # Skip obvious header/garbage rows
        if name in {"name", "fish", "scientific name"} or "pic" in name.split():
            continue

        rest = blk[m.start():]
        diet_raw = m.group(0).lower()
        diet = normalize_diet(diet_raw)

        # Longevity
        long_m = LONG_RE.search(rest) or LONG_ALT_RE.search(rest)
        longevity = long_m.group(0).strip() if long_m else "Unknown"

        # Conservation status (look for known tokens AFTER diet token)
        cons = "Unknown"
        for tok in CONS_TOKENS:
            # Whole word check
            if re.search(r"(?<!\w)" + re.escape(tok) + r"(?!\w)", rest):
                cons = tok
                break

        # poison/toxin (first yes/no after cons)
        poison = "no"
        pm = POISON_RE.search(rest)
        if pm:
            poison = pm.group(1).lower()

        # can_eat
        eat = "Unknown"
        em = EAT_RE.search(rest)
        if em:
            eat = em.group(1)

        # Colors from description (look in the whole block)
        desc_colors = []
        for ct in re.findall(r"[a-z]+", blk.lower()):
            if ct in COLOR_TOKENS and ct not in desc_colors:
                desc_colors.append(ct)

        # SWSA hab — look for known tank/gallery/reef tokens
        swsa_tags = extract_swsa(rest)
        # Natural habitat — pick a recognizable region
        natural = extract_region(rest)

        # Nifty fact — heuristic: first sentence-ish text after "Technically" or "NO!"
        nifty = extract_nifty(rest, eat)

        fishes.append({
            "name": name,
            "diet": diet,
            "longevity": longevity,
            "conservation_status": cons,
            "poison_toxin": poison,
            "natural_hab": natural,
            "swsa_hab": ", ".join(swsa_tags),
            "nifty_facts": nifty,
            "can_eat": eat,
            "description": ", ".join(desc_colors),
        })

    # Deduplicate by name (keep first occurrence)
    seen = set()
    unique = []
    for f in fishes:
        if f["name"] in seen:
            continue
        seen.add(f["name"])
        unique.append(f)
    return unique


def normalize_diet(raw: str) -> str:
    r = raw.lower()
    if r.startswith("omn"):
        return "omnivore"
    if r.startswith("car"):
        return "carnivore"
    if r.startswith("her"):
        return "herbivore"
    if r.startswith("plan"):
        return "planktivore"
    if r.startswith("zoox"):
        return "zooxanthellae"
    if r.startswith("zoo"):
        return "zooplankton"
    if r.startswith("fil"):
        return "filter feeder"
    return ""


SWSA_TAGS = [
    ("turtle reef", "Turtle Reef"),
    ("coral reef", "Coral Reef"),
    ("tank a", "Tank A"),
    ("tank b", "Tank B"),
    ("gallery 6", "Gallery 6"),
    ("gallery 7", "Gallery 7"),
    ("shark", "Shark Tank"),
]


def extract_swsa(text: str) -> list[str]:
    out = []
    lower = text.lower()
    # tokens like "1,2,4,5" or single numbers
    for n in re.findall(r"\b([1-5])\b", lower):
        tag = f"Tank {n}"
        if tag not in out:
            out.append(tag)
    for needle, tag in SWSA_TAGS:
        if needle in lower and tag not in out:
            out.append(tag)
    return out


REGIONS = [
    ("indo-pacific", "Indo-Pacific"),
    ("indo pacific", "Indo-Pacific"),
    ("indo-west", "Indo-West Pacific"),
    ("eastern pacific", "Eastern Pacific"),
    ("western pacific", "Western Pacific"),
    ("south pacific", "South Pacific"),
    ("pacific ocean", "Pacific"),
    ("red sea", "Red Sea"),
    ("indian ocean", "Indian Ocean"),
    ("western indian", "Western Indian Ocean"),
    ("caribbean", "Caribbean"),
    ("western atlantic", "Western Atlantic"),
    ("atlantic ocean", "Atlantic"),
    ("amazon", "Amazon Basin"),
    ("south america", "South America"),
    ("southeast asia", "Southeast Asia"),
    ("east asia", "East Asia"),
    ("hawaii", "Hawaii"),
    ("fiji", "Fiji"),
    ("philippines", "Philippines"),
    ("banggai", "Banggai Islands"),
    ("circumtropical", "Circumtropical"),
    ("oceans world", "Worldwide"),
    ("freshwater", "Freshwater"),
    ("fresh water", "Freshwater"),
]


def extract_region(text: str) -> str:
    lower = text.lower()
    for needle, label in REGIONS:
        if needle in lower:
            return label
    return ""


def extract_nifty(text: str, eat: str) -> str:
    if eat and eat in text:
        idx = text.index(eat) + len(eat)
        snippet = text[idx:].strip()
        # Trim long descriptions/colors
        # Stop at first comma-separated color list
        cut = re.search(r"\s+(orange|yellow|red|pink|purple|blue|green|black|white|brown|silver)(?:,|\s+)", snippet)
        if cut:
            snippet = snippet[: cut.start()].strip()
        return snippet[:140].strip().rstrip("co ")
    return ""


if __name__ == "__main__":
    txt = SRC.read_text()
    data = parse_text(txt)
    OUT.write_text(json.dumps(data, indent=2))
    print(f"Wrote {len(data)} fish entries to {OUT}")
