"""Fetch Wikipedia thumbnail URLs for each fish name in fish_data.RAW_FISH
and write a JSON cache so fish_data.py can reference them statically.
"""
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from fish_data import RAW_FISH  # type: ignore

HEADERS = {"User-Agent": "ReefSearchApp/1.0 (contact: dev@example.com)"}
API = "https://en.wikipedia.org/api/rest_v1/page/summary/"

# Hand-curated mapping to disambiguate / steer wiki lookups.
OVERRIDES = {
    "clown fish": "Ocellaris_clownfish",
    "koi": "Koi",
    "flame angelfish": "Flame_angelfish",
    "freckletail lyretail": "Anthias_squamipinnis",
    "black spot angelfish": "Genicanthus_melanospilos",
    "king angelfish": "Holacanthus_passer",
    "asfur angelfish": "Pomacanthus_asfur",
    "six banded angelfish": "Pomacanthus_sexstriatus",
    "blue ringed angelfish": "Pomacanthus_annularis",
    "yellow stripe angelfish": "Apolemichthys_xanthurus",
    "polka dot boxfish": "Ostracion_cubicus",
    "bicolor angelfish": "Centropyge_bicolor",
    "lemon peel angelfish": "Lemonpeel_angelfish",
    "coral beauty angelfish": "Centropyge_bispinosa",
    "scribbled angelfish": "Chaetodontoplus_duboulayi",
    "false personifier angelfish": "Paracentropyge_venusta",
    "singapore angelfish": "Chaetodontoplus_mesoleucus",
    "goldtail angelfish": "Pomacanthus_chrysurus",
    "exquisite wrasse": "Cirrhilabrus_exquisitus",
    "ruby head wrasse": "Cirrhilabrus_cyanopleura",
    "formosa wrasse": "Coris_formosa",
    "clown wrasse": "Coris_aygula",
    "lubbock's wrasse": "Cirrhilabrus_lubbocki",
    "clown red wrasse": "Halichoeres_chloropterus",
    "lunar wrasse": "Thalassoma_lunare",
    "cleaner wrasse": "Bluestreak_cleaner_wrasse",
    "bird wrasse": "Gomphosus",
    "vegabond butterflyfish": "Chaetodon_vagabundus",
    "double saddle butterflyfish": "Chaetodon_ulietensis",
    "copper band butterflyfish": "Copperband_butterflyfish",
    "pearl scale butterflyfish": "Chaetodon_xanthurus",
    "longfin bannerfish": "Heniochus_acuminatus",
    "longnosed butterflyfish": "Forcipiger_flavissimus",
    "singular bannerfish": "Heniochus_singularius",
    "masked bannerfish": "Heniochus_monoceros",
    "majestic angelfish": "Pomacanthus_navarchus",
    "blue face angelfish": "Pomacanthus_xanthometopon",
    "koran angelfish": "Pomacanthus_semicirculatus",
    "semicircle angelfish": "Pomacanthus_semicirculatus",
    "emperor angelfish": "Emperor_angelfish",
    "tomato anemonefish": "Tomato_clownfish",
    "striped anemonefish": "Orange-fin_anemonefish",
    "maroon anemonefish": "Maroon_clownfish",
    "two banded angelfish": "Amphiprion_bicinctus",
    "anemonefish": "Amphiprion",
    "black anemonefish": "Amphiprion_melanopus",
    "saddleback clownfish": "Saddleback_clownfish",
    "black and gold angelfish": "Centropyge_bicolor",
    "blue green chromis": "Blue_green_chromis",
    "purple tang": "Zebrasoma_xanthurum",
    "chevron tang": "Ctenochaetus_hawaiiensis",
    "flamefin tang": "Acanthurus_pyroferus",
    "red sea sailfin tang": "Zebrasoma_desjardinii",
    "orange back fairyfish": "Cirrhilabrus_aurantidorsalis",
    "sixline wrasse": "Sixline_wrasse",
    "black leopard wrasse": "Macropharyngodon_negrosensis",
    "onespot foxface rabbitfish": "Siganus_unimaculatus",
    "black sailfin blenny": "Atrosalarias_fuscus",
    "neon dottyback": "Pseudochromis_aldabraensis",
    "spotted prawn goby": "Amblyeleotris_guttata",
    "spotted mandarin fish": "Synchiropus_picturatus",
    "dogface pufferfish": "Arothron_nigropunctatus",
    "orange body filefish": "Oxymonacanthus_longirostris",
    "spotted scat": "Scatophagus_argus",
    "diamond fish": "Monodactylus_argenteus",
    "freckled hawkfish": "Paracirrhites_forsteri",
    "flame hawkfish": "Neocirrhites_armatus",
    "indo-pacific squirrelfish": "Sargocentron_diadema",
    "striped squirrelfish": "Sargocentron_xantherythrum",
    "forktail rabbitfish": "Siganus_argenteus",
    "two bar spinefoot rabbitfish": "Siganus_virgatus",
    "orange spotted rabbitfish": "Siganus_guttatus",
    "masked rabbitfish": "Siganus_puellus",
    "double barred rabbitfish": "Siganus_doliatus",
    "bicolor foxface rabbitfish": "Siganus_uspi",
    "stars and stripes pufferfish": "Arothron_hispidus",
    "foxface rabbitfish": "Siganus_vulpinus",
    "silver squirrelfish": "Sargocentron_caudimaculatum",
    "black bar soldierfish": "Myripristis_jacobus",
    "many barred goatfish": "Parupeneus_multifasciatus",
    "bicolor goatfish": "Parupeneus_barberinoides",
    "yellowback goatfish": "Mulloidichthys_vanicolensis",
    "red assorted colour": "Apogon_maculatus",
    "red diana hogfish": "Bodianus_diana",
    "yellow candy basslet": "Liopropoma_carmabi",
    "coral hotfish": "Bodianus_mesothorax",
    "sailfin snapper": "Symphorichthys_spilurus",
    "blue and yellow snapper": "Lutjanus_kasmira",
    "banana fusilier": "Pterocaesio_pisang",
    "bicolor parrotfish": "Cetoscarus_bicolor",
    "stocky pink anthias": "Pseudanthias_hypselosoma",
    "sea turtle": "Green_sea_turtle",
}


def lookup(title: str):
    url = API + urllib.parse.quote(title)
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            thumb = data.get("thumbnail") or data.get("originalimage")
            if thumb and thumb.get("source"):
                return thumb["source"]
    except Exception as e:
        print(f"  !! {title}: {e}")
    return None


def main():
    out = {}
    for f in RAW_FISH:
        name = f["name"]
        title = OVERRIDES.get(name) or name.replace(" ", "_")
        img = lookup(title)
        if not img and name not in OVERRIDES:
            # fall-back: try stripping qualifiers
            base = name.split(" ")[-1].capitalize()
            img = lookup(base)
        out[name] = img or ""
        print(f"{name}: {'OK' if img else 'MISS'}")
    Path(__file__).parent.joinpath("fish_images.json").write_text(json.dumps(out, indent=2))
    print(f"\nWrote {len(out)} entries.")


if __name__ == "__main__":
    main()
