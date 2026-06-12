"""Verbatim PDF parser using document order + x-reset detection.

Strategy:
1. For each page, group chars into rows by y-coordinate.
2. Within each row, walk chars in document order; an x-reset (current x < previous x by > 0.5pt) signals a new "cell".
3. Map cells to known columns by snapping the cell's first-char x to the nearest column-start.
"""
import json
import re
from pathlib import Path
import pdfplumber

PDF_PATH = Path("/tmp/reef.pdf")
OUT_PATH = Path("/app/backend/fish_dataset.json")

# Column start x-positions (calibrated for the latest PDF, June 2025).
COLUMN_STARTS = [
    ("name",         50),
    ("diet",        205),
    ("longevity",   233),
    ("conservation", 282),
    ("poison",      302),
    ("swsa",        320),
    ("natural",     369),
    ("nifty",       386),
    ("can_eat",     415),
    ("description", 497),
    ("scientific", 600),
]


def snap_column(x: float) -> str:
    """Return column whose [start, next_start) range contains x. Always returns one."""
    cols = COLUMN_STARTS
    for i, (name, start) in enumerate(cols):
        right = cols[i + 1][1] if i + 1 < len(cols) else 10000
        if start <= x < right:
            return name
    return cols[0][0]


def chars_to_rows(page):
    """Group chars into rows based on y-coordinate (each unique y == one row)."""
    chars = page.chars
    rows = {}
    for c in chars:
        ykey = round(c["top"], 1)
        rows.setdefault(ykey, []).append(c)
    # Sort by y ascending; each row keeps document order internally (chars were appended in stream order).
    ordered_rows = []
    for y in sorted(rows.keys()):
        ordered_rows.append((y, rows[y]))
    return ordered_rows


def split_row_into_cells(row_chars):
    """Walk chars in document order; split at x-resets or large forward jumps."""
    cells = []
    cur = []
    prev_x = None
    for c in row_chars:
        x = c["x0"]
        if prev_x is not None:
            delta = x - prev_x
            # New cell on (a) any backward jump or (b) forward jump > 8 pts.
            if delta < 0 or delta > 8:
                cells.append(cur)
                cur = []
        cur.append(c)
        prev_x = x
    if cur:
        cells.append(cur)
    return cells


def cell_text(cell_chars) -> str:
    return "".join(c["text"] for c in cell_chars).strip()


def cell_xstart(cell_chars) -> float:
    if not cell_chars:
        return 0.0
    return min(c["x0"] for c in cell_chars)


def parse_pdf():
    all_rows = []
    with pdfplumber.open(str(PDF_PATH)) as pdf:
        for page_idx, page in enumerate(pdf.pages):
            y_rows = chars_to_rows(page)
            for y, row_chars in y_rows:
                cells = split_row_into_cells(row_chars)
                # Build a dict by snapping each cell's start x to nearest column
                rec = {col: "" for col, _ in COLUMN_STARTS}
                for cell in cells:
                    text = cell_text(cell)
                    if not text:
                        continue
                    col = snap_column(cell_xstart(cell))
                    if not col:
                        continue
                    # If multiple text runs map to same column, concatenate with space
                    if rec[col]:
                        rec[col] = (rec[col] + " " + text).strip()
                    else:
                        rec[col] = text
                # Filter out header rows and empty rows
                if not rec["name"]:
                    continue
                # Skip header lines containing meta keywords
                if rec["name"].lower() in {"name", "namepic", "fish"}:
                    continue
                if "pic" in rec["name"].lower() and "diet" in rec.get("diet", "").lower():
                    continue
                all_rows.append({"_page": page_idx, "_y": y, **rec})
    return all_rows


if __name__ == "__main__":
    rows = parse_pdf()
    print(f"Parsed {len(rows)} rows")

    # Post-process: split natural/nifty when natural contains a sentence after a region word.
    REGION_ENDS = [
        "Ocean", "Pacific", "Atlantic", "reefs", "reef", "Sea", "Caribbean",
        "Asia", "America", "Islands", "Australia", "Africa", "Mexico",
        "Indonesia", "Philippines", "Hawaii", "Fiji", "Worldwide", "Tropics",
        "Archipelago", "ocean", "pacific", "atlantic", "Basin", "basin",
        "rainforest", "Coast", "coast", "Rocky", "Reefs", "waters",
        "Wide-ranging",
    ]
    # Color vocab used to detect description text that bled into another column.
    COLORS = {"black", "blue", "green", "orange", "red", "yellow", "purple",
              "pink", "brown", "silver", "tan", "gold", "white", "olive",
              "rainbow"}

    def _split_after_region(text: str):
        """If text contains a region word followed by an uppercase letter, split."""
        for word in REGION_ENDS:
            idx = text.find(word)
            if idx <= 0:
                continue
            end_idx = idx + len(word)
            if end_idx < len(text) and text[end_idx].isupper():
                return text[:end_idx].strip(), text[end_idx:].strip()
        return None

    def _strip_trailing_colors(text: str):
        """If text ends with color-list, return (clean_text, color_list)."""
        # Match a trailing sequence of comma-separated color words.
        tokens = re.split(r"[,\s]+", text)
        i = len(tokens)
        while i > 0 and tokens[i - 1].lower().rstrip(".") in COLORS:
            i -= 1
        if i == len(tokens):
            return text, ""
        prefix_tokens = tokens[:i]
        color_tokens = tokens[i:]
        prefix = " ".join(prefix_tokens).strip()
        # Best-effort: reconstruct color text exactly.
        # Find where colors begin in original text.
        for c in color_tokens:
            pos = text.find(c)
            if pos >= 0:
                return text[:pos].rstrip(", ").strip(), text[pos:].strip()
        return text, ""

    # Set of can_eat prefixes — anything that follows directly may be description.
    CAN_EAT_PREFIXES = ("Technically", "NO!", "N/A")

    def _peel_can_eat(text: str):
        """Return (clean_can_eat, leftover) by splitting after a known prefix."""
        for p in CAN_EAT_PREFIXES:
            if text.startswith(p) and len(text) > len(p):
                return p, text[len(p):].strip(", ").strip()
        return text, ""

    for r in rows:
        # Fix natural/nifty merge
        nat = r["natural"]
        if not r["nifty"] and len(nat) >= 25:
            split = _split_after_region(nat)
            if split:
                r["natural"], r["nifty"] = split

        # Fix can_eat -> description merge (e.g. "Technicallyblack, blue, orange")
        eat = r["can_eat"]
        if eat and not r["description"]:
            # If eat contains color-list trailing it, peel description out.
            cleaned, colors = _strip_trailing_colors(eat)
            if colors:
                r["can_eat"] = cleaned
                r["description"] = colors

        # Hard split when can_eat begins with a known prefix and has trailing junk
        eat = r["can_eat"]
        if eat and eat not in CAN_EAT_PREFIXES:
            cleaned, leftover = _peel_can_eat(eat)
            if cleaned != eat:
                r["can_eat"] = cleaned
                if leftover and not r["description"]:
                    r["description"] = leftover
                elif leftover and r["description"]:
                    r["description"] = leftover + ", " + r["description"]

        # Fix swsa -> natural bleed (when swsa ends with region word and natural is empty)
        sw = r["swsa"]
        if sw and not r["natural"]:
            split = _split_after_region(sw)
            if split:
                r["swsa"], r["natural"] = split
            else:
                # Look for an "Indo-Pacific", "Pacific", "Atlantic", "Caribbean" prefix in tail.
                # The leading char may be a stray uppercase letter due to overflow (e.g. "AIndo-").
                m = re.search(
                    r"(?:[A-Z](?=Indo-))?(Indo-Pacific|Pacific|Atlantic|Caribbean|Indian|Red Sea|Western|Eastern|Tropical|Hawaii|Fiji|Amazon|Mexico|South|North|Southeast|East|Banggai|African|Florida|Australia|Philippines|Indonesia|Worldwide|Mediterranean|Coastal|Open ocean|Subtropical|Asian|Oceans world|Caribbean coral|Wide-ranging)",
                    sw,
                )
                if m and m.start() > 0:
                    cut = m.start(1)
                    pre = sw[:cut].rstrip(", ").rstrip()
                    post = sw[cut:].strip()
                    # Strip any single leading capital letter that was part of e.g. "AIndo"
                    if pre.endswith(" A") or pre.endswith(",A"):
                        pre = pre[:-2].rstrip(", ").strip()
                    elif pre and pre[-1].isupper() and len(pre.split()) > 1:
                        pre = pre[:-1].rstrip(", ").strip()
                    r["swsa"] = pre
                    r["natural"] = post

    # Build the dataset matching existing fish_dataset.json schema.
    # Filter out any obvious header artifacts.
    dataset = []
    sci_names = {}
    for r in rows:
        name = r["name"].strip()
        if not name or "pic" == name.lower() or name.lower() in {"name", "fish"}:
            continue
        # Skip rows whose diet is empty (likely a header/garbage row)
        if not r["diet"].strip():
            continue
        dataset.append({
            "name": name,
            "diet": r["diet"].strip(),
            "longevity": r["longevity"].strip(),
            "conservation_status": r["conservation"].strip(),
            "poison_toxin": r["poison"].strip(),
            "natural_hab": r["natural"].strip(),
            "swsa_hab": r["swsa"].strip(),
            "nifty_facts": r["nifty"].strip(),
            "can_eat": r["can_eat"].strip(),
            "description": r["description"].strip(),
        })
        if r["scientific"].strip():
            sci_names[name.lower()] = r["scientific"].strip()

    print(f"Final dataset: {len(dataset)} fish")
    OUT_PATH.write_text(json.dumps(dataset, indent=2))
    print(f"Wrote {OUT_PATH}")

    sci_path = OUT_PATH.parent / "scientific_names.json"
    sci_path.write_text(json.dumps(sci_names, indent=2, sort_keys=True))
    print(f"Wrote {sci_path} ({len(sci_names)} entries)")
