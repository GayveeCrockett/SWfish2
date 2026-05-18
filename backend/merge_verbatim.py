"""Merge verbatim-extracted columns from the PDF into fish_dataset.json.

This script takes the verbatim extraction (diet/longevity/conservation) and
overwrites those fields in the existing dataset with the PDF's literal values.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
DATASET = ROOT / "fish_dataset.json"
OUT = ROOT / "fish_dataset.json"

# Verbatim extract from the PDF for diet/longevity/conservation.
# Diet column was concatenated with longevity in PDF cells, so we split it.
VERBATIM_FIELDS_PATH = ROOT / "verbatim_diet_longevity.json"


def split_diet_longevity(merged: str) -> tuple[str, str]:
    """Split 'Omnivc 5-10 years' into ('Omnivc', '5-10 years')."""
    if not merged:
        return "", ""
    m = re.match(r"^(\S+?)\s+(.+)$", merged.strip())
    if not m:
        return merged.strip(), ""
    return m.group(1), m.group(2)


def main():
    dataset = json.loads(DATASET.read_text())
    verbatim = json.loads(VERBATIM_FIELDS_PATH.read_text())
    by_name = {v["name"].strip().lower(): v for v in verbatim}

    updated = 0
    for fish in dataset:
        name = fish["name"].strip().lower()
        v = by_name.get(name)
        if not v:
            continue
        diet, longevity = split_diet_longevity(v.get("diet", ""))
        if diet:
            fish["diet"] = diet
        if longevity:
            fish["longevity"] = longevity
        cons = v.get("longevity", "")  # AI put conservation in "longevity" field
        if cons:
            fish["conservation_status"] = cons
        updated += 1

    OUT.write_text(json.dumps(dataset, indent=2))
    print(f"Merged verbatim diet/longevity/conservation for {updated}/{len(dataset)} fish")


if __name__ == "__main__":
    main()
