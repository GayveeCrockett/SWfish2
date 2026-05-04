from fastapi import FastAPI, APIRouter, HTTPException, Query
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import os
import logging
from pathlib import Path
from typing import List, Optional

from fish_data import FISHES, all_filter_options

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")

app = FastAPI(title="Reef Search API")
api_router = APIRouter(prefix="/api")


@api_router.get("/")
async def root():
    return {"message": "Reef Search API", "fish_count": len(FISHES)}


@api_router.get("/filters")
async def get_filters():
    """Return all available filter options derived from the dataset."""
    return all_filter_options()


def _match_any(values: List[str], wanted: List[str]) -> bool:
    if not wanted:
        return True
    lowered = [v.lower() for v in values]
    return any(w.lower() in lowered for w in wanted)


def _match_single(value: str, wanted: List[str]) -> bool:
    if not wanted:
        return True
    return value.lower() in [w.lower() for w in wanted]


@api_router.get("/fishes")
async def list_fishes(
    q: Optional[str] = None,
    colors: Optional[List[str]] = Query(default=None),
    diets: Optional[List[str]] = Query(default=None),
    habitats: Optional[List[str]] = Query(default=None),
    swsa_habitats: Optional[List[str]] = Query(default=None),
    conservation: Optional[List[str]] = Query(default=None),
    can_eat: Optional[List[str]] = Query(default=None),
    poison: Optional[List[str]] = Query(default=None),
):
    results = []
    query = (q or "").strip().lower()
    for fish in FISHES:
        if query and query not in fish["name"].lower():
            continue
        if not _match_any(fish["colors"], colors or []):
            continue
        if diets and not _match_single(fish["diet"], diets):
            continue
        if not _match_any(fish["habitats"], habitats or []):
            continue
        if not _match_any(fish["swsa_habitats"], swsa_habitats or []):
            continue
        if conservation and not _match_single(fish["conservation_status"], conservation):
            continue
        if can_eat and not _match_single(fish["can_eat"], can_eat):
            continue
        if poison and not _match_single(fish["poison_toxin"], poison):
            continue
        results.append(fish)
    return {"count": len(results), "fishes": results}


@api_router.get("/fishes/{fish_id}")
async def get_fish(fish_id: str):
    for fish in FISHES:
        if fish["id"] == fish_id:
            return fish
    raise HTTPException(status_code=404, detail="Fish not found")


app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)
