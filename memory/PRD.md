# Reef Search — Product Requirements Document

## Overview
A React Native (Expo) mobile app that lets the user search and browse a catalog of
~89 reef / marine fish species extracted from the supplied *Reef Search – Fish Log* PDF.

## User requirements (captured)
- Search filters: name + color + diet + habitat + conservation + edibility + poison/toxin
- Placeholder images for all fish (user will add real images later)
- "Sea World" colour palette (bright aquatic blues, coral, sunny yellow)
- No extra features beyond search and detail view

## Architecture
- **Backend** (FastAPI, `/app/backend/server.py`)
  - Static dataset lives in `fish_data.py` (89 fish, normalized diet keywords,
    canonical habitat tags, colour list parsed from description).
  - Endpoints (all under `/api` per ingress rules):
    - `GET /api/` – health + count
    - `GET /api/filters` – available filter option lists
    - `GET /api/fishes` – supports `q`, multi-value `colors`, `diets`, `habitats`,
      `conservation`, `can_eat`, `poison`
    - `GET /api/fishes/{id}` – single fish detail (404 if missing)
- **Frontend** (Expo Router)
  - `app/_layout.tsx` – stack + loads Fredoka / Nunito via `@expo-google-fonts`
  - `app/index.tsx` – home: hero copy, search bar, filter pill sheet, 2-col fish grid
  - `app/fish/[id].tsx` – hero image, bento grid (diet / longevity / conservation /
    edibility), toxicity banner, habitat pills, nifty fact card
  - `src/api.ts` – typed fetch helpers
  - `src/theme.ts` – colour / font / spacing tokens driven by `design_guidelines.json`

## Design
- Palette: Deep ocean `#03045E` text, brand `#0077B6`, cyan `#00B4D8`, coral `#EF476F`,
  sunny `#FFD166`, seafoam `#F6FBFC` background
- Typography: Fredoka for display, Nunito for body (non-generic, not Inter/Roboto)
- Mobile first, 44px+ touch targets, keyboard avoidance, safe-area insets

## Smart business enhancement (future-ready)
Because the dataset already includes edibility and toxicity flags, a natural
extension is a "Safety filter" you could gate behind a premium *Dive Guide Pro*
tier — divemasters and aquarists would pay a small monthly fee for curated
"do not touch" safety lists, automatic trip filters, and printable field cards.
The API and data model already support it; only a Stripe gate would need to be
added later.

## Testing
- 8/8 pytest backend tests pass (`/app/backend/tests/test_reef_api.py`)
- Frontend Playwright flow passes: search debounce, filter sheet, color filter,
  detail navigation, back navigation, empty state
- No mocked APIs. No authentication. No external integrations.
