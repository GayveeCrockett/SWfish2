"""Static fish data sourced from the Reef Search fish log PDF.
Each entry is normalized with consistent diet keywords and color tags.
"""
from typing import List, Dict, Any
import json
from pathlib import Path

_IMAGES_PATH = Path(__file__).parent / "fish_images.json"
try:
    _WIKI_IMAGES: Dict[str, str] = json.loads(_IMAGES_PATH.read_text())
except FileNotFoundError:
    _WIKI_IMAGES = {}

VALID_DIETS = {
    "zoopl": "zooplankton",
    "zooplar": "zooplankton",
    "omnivo": "omnivore",
    "omnivore": "omnivore",
    "carnivo": "carnivore",
    "plankiv": "planktivore",
}

RAW_FISH: List[Dict[str, Any]] = [
    {"name": "clown fish", "diet": "zoopl", "longevity": "6-10 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "sequential hermaphrodite", "can_eat": "Technically", "description": "orange, black, white", "image_url": "https://customer-assets.emergentagent.com/job_fish-search-app/artifacts/9vuy2m5y_clown.jpg"},
    {"name": "koi", "diet": "omnivore", "longevity": "25-35 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Fresh Water; east asia", "nifty_facts": "", "can_eat": "Technically", "description": "orange, black, yellow"},
    {"name": "flame angelfish", "diet": "omnivo", "longevity": "5-10 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Pacific; coral", "nifty_facts": "", "can_eat": "Technically", "description": "orange, black, blue"},
    {"name": "freckletail lyretail", "diet": "omnivo", "longevity": "8-15 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "blue, white, black"},
    {"name": "black spot angelfish", "diet": "omnivo", "longevity": "8-15 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "white, brown"},
    {"name": "king angelfish", "diet": "omnivo", "longevity": "8-15 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "east pacific", "nifty_facts": "", "can_eat": "Technically", "description": "yellow, white, blue"},
    {"name": "asfur angelfish", "diet": "omnivo", "longevity": "8-15 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Red sea, indian ocean", "nifty_facts": "", "can_eat": "Technically", "description": "yellow, black, white, blue"},
    {"name": "six banded angelfish", "diet": "omnivo", "longevity": "8-10 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "yellow, black, white, blue"},
    {"name": "blue ringed angelfish", "diet": "omnivo", "longevity": "10-15 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "yellow, blue"},
    {"name": "yellow stripe angelfish", "diet": "omnivo", "longevity": "15-20 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "yellow, blue"},
    {"name": "polka dot boxfish", "diet": "omnivore", "longevity": "8-15 years", "conservation_status": "LC", "poison_toxin": "yes", "natural_hab": "Indo-Pacific", "nifty_facts": "releases toxin when stressed", "can_eat": "NO!", "description": "yellow, black"},
    {"name": "bicolor angelfish", "diet": "omnivo", "longevity": "5-10 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "yellow, blue"},
    {"name": "lemon peel angelfish", "diet": "omnivo", "longevity": "10-15 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "yellow, blue"},
    {"name": "coral beauty angelfish", "diet": "omnivo", "longevity": "5-10 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "blue, orange"},
    {"name": "scribbled angelfish", "diet": "omnivo", "longevity": "10-15 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "south pacific", "nifty_facts": "", "can_eat": "Technically", "description": "blue, yellow"},
    {"name": "false personifier angelfish", "diet": "zooplar", "longevity": "10-15 years", "conservation_status": "no status", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "blue, yellow, white"},
    {"name": "singapore angelfish", "diet": "omnivo", "longevity": "7-10 years", "conservation_status": "no status", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "hermaphroditic", "can_eat": "Technically", "description": "black, white, yellow"},
    {"name": "goldtail angelfish", "diet": "omnivo", "longevity": "8-10 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "western indian ocean", "nifty_facts": "", "can_eat": "Technically", "description": "black, white, yellow"},
    {"name": "exquisite wrasse", "diet": "zooplar", "longevity": "5 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "males will lose color when stressed", "can_eat": "Technically", "description": "blue, yellow, orange"},
    {"name": "ruby head wrasse", "diet": "plankiv", "longevity": "5-6 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "western pacific", "nifty_facts": "", "can_eat": "Technically", "description": "red"},
    {"name": "formosa wrasse", "diet": "carnivo", "longevity": "5-10 years", "conservation_status": "no status", "poison_toxin": "no", "natural_hab": "indian ocean", "nifty_facts": "", "can_eat": "Technically", "description": "yellow, black, white"},
    {"name": "clown wrasse", "diet": "carnivo", "longevity": "5-10 years", "conservation_status": "no status", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "orange, blue, white"},
    {"name": "lubbock's wrasse", "diet": "carnivo", "longevity": "4-7 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Philippines", "nifty_facts": "", "can_eat": "Technically", "description": "orange, blue, yellow, white"},
    {"name": "clown red wrasse", "diet": "carnivo", "longevity": "5-8 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "green, blue"},
    {"name": "lunar wrasse", "diet": "carnivo", "longevity": "10 years", "conservation_status": "no status", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "protogynous hermaphrodite", "can_eat": "Technically", "description": "green, blue"},
    {"name": "cleaner wrasse", "diet": "carnivo", "longevity": "4 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "cleans parasites off other fish", "can_eat": "NO!", "description": "black, blue, yellow"},
    {"name": "bird wrasse", "diet": "carnivo", "longevity": "5-15 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "long beak-like snout", "can_eat": "NO!", "description": "blue, green"},
    {"name": "vagabond butterflyfish", "diet": "omnivo", "longevity": "5-10 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "white, yellow, black"},
    {"name": "double saddle butterflyfish", "diet": "omnivore", "longevity": "5-10 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "white, black, yellow"},
    {"name": "copper band butterflyfish", "diet": "carnivo", "longevity": "5-10 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "white, black, yellow"},
    {"name": "pearl scale butterflyfish", "diet": "omnivo", "longevity": "5-10 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "white, yellow, black"},
    {"name": "longfin bannerfish", "diet": "omnivo", "longevity": "5-10 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "white, orange, black"},
    {"name": "longnosed butterflyfish", "diet": "omnivo", "longevity": "5-10 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "yellow, black, white"},
    {"name": "singular bannerfish", "diet": "omnivo", "longevity": "5-10 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "white, black, yellow"},
    {"name": "masked bannerfish", "diet": "omnivo", "longevity": "5-10 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "white, black, yellow"},
    {"name": "majestic angelfish", "diet": "omnivo", "longevity": "10-15 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "yellow, blue"},
    {"name": "blue face angelfish", "diet": "omnivo", "longevity": "10-15 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "blue, yellow, green"},
    {"name": "koran angelfish", "diet": "omnivo", "longevity": "15-20 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "green, yellow, blue"},
    {"name": "semicircle angelfish", "diet": "omnivo", "longevity": "10-15 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "black, white, blue"},
    {"name": "emperor angelfish", "diet": "omnivo", "longevity": "15-20 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "juvenile looks very different from adult", "can_eat": "Technically", "description": "yellow, blue, black"},
    {"name": "tomato anemonefish", "diet": "omnivo", "longevity": "5-10 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "orange, white"},
    {"name": "striped anemonefish", "diet": "omnivo", "longevity": "5-10 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "orange, white"},
    {"name": "two banded angelfish", "diet": "omnivo", "longevity": "5-10 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Red sea, indian ocean", "nifty_facts": "", "can_eat": "Technically", "description": "yellow, white"},
    {"name": "anemonefish", "diet": "omnivore", "longevity": "5-10 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "black, white"},
    {"name": "maroon anemonefish", "diet": "omnivo", "longevity": "5-10 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "purple, yellow"},
    {"name": "black anemonefish", "diet": "omnivo", "longevity": "5-10 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "black, orange, yellow"},
    {"name": "saddleback clownfish", "diet": "omnivo", "longevity": "5-10 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "black, white, orange"},
    {"name": "black and gold angelfish", "diet": "omnivo", "longevity": "5-10 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "yellow, black"},
    {"name": "blue green chromis", "diet": "zoopl", "longevity": "5-10 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "green, blue"},
    {"name": "purple tang", "diet": "omnivo", "longevity": "10-15 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Red sea, indian ocean", "nifty_facts": "", "can_eat": "Technically", "description": "purple, yellow"},
    {"name": "chevron tang", "diet": "omnivo", "longevity": "10-15 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "orange, black"},
    {"name": "flamefin tang", "diet": "omnivo", "longevity": "10-15 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "brown, yellow"},
    {"name": "red sea sailfin tang", "diet": "omnivo", "longevity": "10-15 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Red sea, indian ocean", "nifty_facts": "", "can_eat": "Technically", "description": "white, yellow, blue"},
    {"name": "orange back fairyfish", "diet": "carnivo", "longevity": "5-7 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "purple, orange"},
    {"name": "sixline wrasse", "diet": "carnivo", "longevity": "4-6 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "purple, yellow"},
    {"name": "black leopard wrasse", "diet": "carnivo", "longevity": "5-10 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "black, yellow, white"},
    {"name": "onespot foxface rabbitfish", "diet": "omnivo", "longevity": "5-10 years", "conservation_status": "LC", "poison_toxin": "yes", "natural_hab": "Indo-Pacific", "nifty_facts": "venomous dorsal spines", "can_eat": "NO!", "description": "yellow, white, black"},
    {"name": "black sailfin blenny", "diet": "omnivo", "longevity": "2-4 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "black"},
    {"name": "neon dottyback", "diet": "carnivo", "longevity": "5-7 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "orange, blue"},
    {"name": "spotted prawn goby", "diet": "carnivo", "longevity": "5-8 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "symbiotic with pistol shrimp", "can_eat": "Technically", "description": "white, orange"},
    {"name": "spotted mandarin fish", "diet": "carnivo", "longevity": "4-6 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "produces a toxic slime coat", "can_eat": "NO!", "description": "orange, blue, green"},
    {"name": "dogface pufferfish", "diet": "carnivo", "longevity": "10-15 years", "conservation_status": "LC", "poison_toxin": "yes", "natural_hab": "Indo-Pacific", "nifty_facts": "contains tetrodotoxin", "can_eat": "NO!", "description": "white, black"},
    {"name": "orange body filefish", "diet": "omnivo", "longevity": "3-5 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "orange, black"},
    {"name": "spotted scat", "diet": "omnivo", "longevity": "10-20 years", "conservation_status": "LC", "poison_toxin": "yes", "natural_hab": "Indo-Pacific", "nifty_facts": "venomous fin spines", "can_eat": "Technically", "description": "yellow, black"},
    {"name": "diamond fish", "diet": "omnivo", "longevity": "5-10 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "white"},
    {"name": "freckled hawkfish", "diet": "carnivo", "longevity": "5-8 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "orange, yellow"},
    {"name": "flame hawkfish", "diet": "carnivo", "longevity": "5-10 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "red, black"},
    {"name": "indo-pacific squirrelfish", "diet": "carnivo", "longevity": "5-10 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "orange, white"},
    {"name": "striped squirrelfish", "diet": "carnivo", "longevity": "5-10 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "red, white"},
    {"name": "forktail rabbitfish", "diet": "omnivo", "longevity": "10-12 years", "conservation_status": "LC", "poison_toxin": "yes", "natural_hab": "Indo-Pacific", "nifty_facts": "venomous fin spines", "can_eat": "Technically", "description": "blue, yellow"},
    {"name": "two bar spinefoot rabbitfish", "diet": "omnivo", "longevity": "10-12 years", "conservation_status": "LC", "poison_toxin": "yes", "natural_hab": "Indo-Pacific", "nifty_facts": "venomous fin spines", "can_eat": "Technically", "description": "white, blue, yellow, black"},
    {"name": "orange spotted rabbitfish", "diet": "omnivo", "longevity": "10-12 years", "conservation_status": "LC", "poison_toxin": "yes", "natural_hab": "Indo-Pacific", "nifty_facts": "venomous fin spines", "can_eat": "Technically", "description": "purple, yellow, orange"},
    {"name": "masked rabbitfish", "diet": "omnivo", "longevity": "10-12 years", "conservation_status": "LC", "poison_toxin": "yes", "natural_hab": "Indo-Pacific", "nifty_facts": "venomous fin spines", "can_eat": "Technically", "description": "yellow, black, white"},
    {"name": "double barred rabbitfish", "diet": "omnivo", "longevity": "10-12 years", "conservation_status": "LC", "poison_toxin": "yes", "natural_hab": "Indo-Pacific", "nifty_facts": "venomous fin spines", "can_eat": "Technically", "description": "black, yellow, white"},
    {"name": "bicolor foxface rabbitfish", "diet": "omnivo", "longevity": "10-12 years", "conservation_status": "LC", "poison_toxin": "yes", "natural_hab": "Indo-Pacific", "nifty_facts": "venomous fin spines", "can_eat": "NO!", "description": "blue, yellow"},
    {"name": "stars and stripes pufferfish", "diet": "carnivo", "longevity": "10-15 years", "conservation_status": "LC", "poison_toxin": "yes", "natural_hab": "Indo-Pacific", "nifty_facts": "contains tetrodotoxin", "can_eat": "NO!", "description": "yellow, white, black"},
    {"name": "foxface rabbitfish", "diet": "omnivo", "longevity": "10-12 years", "conservation_status": "LC", "poison_toxin": "yes", "natural_hab": "Indo-Pacific", "nifty_facts": "venomous fin spines", "can_eat": "NO!", "description": "white, orange"},
    {"name": "silver squirrelfish", "diet": "carnivo", "longevity": "5-10 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "white, orange"},
    {"name": "black bar soldierfish", "diet": "carnivo", "longevity": "5-10 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "nocturnal", "can_eat": "Technically", "description": "orange, black, white"},
    {"name": "many barred goatfish", "diet": "carnivo", "longevity": "10-20 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "yellow, orange, black, white"},
    {"name": "bicolor goatfish", "diet": "carnivo", "longevity": "5-10 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "uses barbels to find prey", "can_eat": "Technically", "description": "yellow, orange, black, white"},
    {"name": "yellowback goatfish", "diet": "carnivo", "longevity": "5-10 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "white, yellow, black"},
    {"name": "red assorted colour", "diet": "carnivo", "longevity": "3-5 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "mouth brooder", "can_eat": "Technically", "description": "white, red, black"},
    {"name": "red diana hogfish", "diet": "carnivo", "longevity": "7-10 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "red, white"},
    {"name": "yellow candy basslet", "diet": "carnivo", "longevity": "5-7 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Caribbean", "nifty_facts": "", "can_eat": "Technically", "description": "yellow, red"},
    {"name": "coral hotfish", "diet": "carnivo", "longevity": "5-10 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "black, yellow"},
    {"name": "sailfin snapper", "diet": "carnivo", "longevity": "10-15 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "blue, yellow, orange, black"},
    {"name": "blue and yellow snapper", "diet": "omnivo", "longevity": "5-7 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "blue, yellow"},
    {"name": "banana fusilier", "diet": "plankiv", "longevity": "5-10 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "blue, yellow"},
    {"name": "bicolor parrotfish", "diet": "omnivo", "longevity": "5-10 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "grazes algae off coral", "can_eat": "Technically", "description": "green"},
    {"name": "stocky pink anthias", "diet": "zoopl", "longevity": "5-10 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "", "can_eat": "Technically", "description": "pink, orange"},
    {"name": "sea turtle", "diet": "omnivore", "longevity": "50-100 years", "conservation_status": "LC", "poison_toxin": "no", "natural_hab": "Indo-Pacific", "nifty_facts": "ancient mariner of the reef", "can_eat": "NO!", "description": "green, brown"},
]


def _normalize_diet(raw: str) -> str:
    if not raw:
        return ""
    return VALID_DIETS.get(raw.strip().lower(), "")


def _parse_colors(desc: str) -> List[str]:
    if not desc:
        return []
    return [c.strip().lower() for c in desc.split(",") if c.strip()]


def _normalize_habitat(raw: str) -> List[str]:
    """Split a natural_hab string into canonical region tags."""
    if not raw:
        return []
    r = raw.lower()
    regions = []
    if "indo-pacific" in r or "indo pacific" in r:
        regions.append("Indo-Pacific")
    if "east pacific" in r:
        regions.append("East Pacific")
    if "western pacific" in r:
        regions.append("Western Pacific")
    if "south pacific" in r:
        regions.append("South Pacific")
    if "pacific" in r and not regions:
        regions.append("Pacific")
    if "red sea" in r:
        regions.append("Red Sea")
    if "indian ocean" in r:
        regions.append("Indian Ocean")
    if "philippines" in r or "phillipines" in r:
        regions.append("Philippines")
    if "fresh water" in r or "east asia" in r:
        regions.append("Fresh Water")
    if "caribbean" in r:
        regions.append("Caribbean")
    if not regions:
        regions.append(raw)
    # de-duplicate preserving order
    seen = set()
    out = []
    for x in regions:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def _fruit_for_index(idx: int) -> str:
    """Map fish index to SWSA habitat tank (fruit) per the Reef Search fish log."""
    if idx <= 6:
        return "banana"
    if idx <= 19:
        return "mango"
    if idx <= 67:
        return "kiwi"
    return "strawberry"


def build_fishes() -> List[Dict[str, Any]]:
    result = []
    for idx, f in enumerate(RAW_FISH):
        # Priority: explicit image_url on the fish (e.g., user upload) > Wikipedia lookup
        image_url = f.get("image_url") or _WIKI_IMAGES.get(f["name"], "")
        fruit = _fruit_for_index(idx)
        result.append({
            "id": str(idx + 1),
            "name": f["name"],
            "diet": _normalize_diet(f.get("diet", "")),
            "longevity": f.get("longevity", "") or "Unknown",
            "conservation_status": f.get("conservation_status", "") or "Unknown",
            "poison_toxin": f.get("poison_toxin", "") or "unknown",
            "habitats": _normalize_habitat(f.get("natural_hab", "")),
            "swsa_habitats": [fruit],
            "swsa_fruit": fruit,
            "natural_hab_raw": f.get("natural_hab", ""),
            "swsa_hab_raw": fruit,
            "nifty_facts": f.get("nifty_facts", ""),
            "can_eat": f.get("can_eat", "") or "Unknown",
            "colors": _parse_colors(f.get("description", "")),
            "description": f.get("description", ""),
            "image_url": image_url,
        })
    return result


FISHES: List[Dict[str, Any]] = build_fishes()


def all_filter_options() -> Dict[str, List[str]]:
    colors = set()
    diets = set()
    habitats = set()
    swsa = set()
    conservation = set()
    can_eat = set()
    poison = set()
    for f in FISHES:
        for c in f["colors"]:
            colors.add(c)
        if f["diet"]:
            diets.add(f["diet"])
        for h in f["habitats"]:
            habitats.add(h)
        for h in f["swsa_habitats"]:
            swsa.add(h)
        conservation.add(f["conservation_status"])
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
