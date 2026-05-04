const BASE_URL = process.env.EXPO_PUBLIC_BACKEND_URL;

export type Fish = {
  id: string;
  name: string;
  diet: string;
  longevity: string;
  conservation_status: string;
  poison_toxin: string;
  habitats: string[];
  swsa_habitats: string[];
  natural_hab_raw: string;
  swsa_hab_raw: string;
  nifty_facts: string;
  can_eat: string;
  colors: string[];
  description: string;
  image_url?: string;
};

export type FilterOptions = {
  colors: string[];
  diets: string[];
  habitats: string[];
  swsa_habitats: string[];
  conservation: string[];
  can_eat: string[];
  poison: string[];
};

export type SearchFilters = {
  q?: string;
  colors?: string[];
  diets?: string[];
  habitats?: string[];
  swsa_habitats?: string[];
  conservation?: string[];
  can_eat?: string[];
  poison?: string[];
};

function buildQuery(filters: SearchFilters): string {
  const params = new URLSearchParams();
  if (filters.q) params.append("q", filters.q);
  const multi: (keyof SearchFilters)[] = ["colors", "diets", "habitats", "swsa_habitats", "conservation", "can_eat", "poison"];
  for (const key of multi) {
    const values = filters[key] as string[] | undefined;
    if (values && values.length) {
      for (const v of values) params.append(key, v);
    }
  }
  const s = params.toString();
  return s ? `?${s}` : "";
}

export async function fetchFishes(filters: SearchFilters): Promise<{ count: number; fishes: Fish[] }> {
  const res = await fetch(`${BASE_URL}/api/fishes${buildQuery(filters)}`);
  if (!res.ok) throw new Error(`Failed to fetch fishes: ${res.status}`);
  return res.json();
}

export async function fetchFilters(): Promise<FilterOptions> {
  const res = await fetch(`${BASE_URL}/api/filters`);
  if (!res.ok) throw new Error(`Failed to fetch filters: ${res.status}`);
  return res.json();
}

export async function fetchFish(id: string): Promise<Fish> {
  const res = await fetch(`${BASE_URL}/api/fishes/${id}`);
  if (!res.ok) throw new Error(`Failed to fetch fish: ${res.status}`);
  return res.json();
}
