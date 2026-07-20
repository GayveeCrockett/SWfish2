/* Sea World Explorer's Reef — Service Worker
 * Strategy:
 *   - App shell (HTML/JS/CSS): network-first with cache fallback
 *   - Fish images (/api/images/*): cache-first
 *   - API JSON (/api/fishes|/api/filters): stale-while-revalidate
 */
const CACHE_VERSION = "reef-v1";
const APP_SHELL_CACHE = `${CACHE_VERSION}-shell`;
const IMAGE_CACHE = `${CACHE_VERSION}-images`;
const API_CACHE = `${CACHE_VERSION}-api`;

const PRECACHE = [
  "/",
  "/manifest.json",
  "/icons/icon-192.png",
  "/icons/icon-512.png",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(APP_SHELL_CACHE).then((cache) => cache.addAll(PRECACHE)).catch(() => {})
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((names) =>
      Promise.all(
        names
          .filter((n) => !n.startsWith(CACHE_VERSION))
          .map((n) => caches.delete(n))
      )
    )
  );
  self.clients.claim();
});

async function cacheFirst(request, cacheName) {
  const cache = await caches.open(cacheName);
  const hit = await cache.match(request);
  if (hit) return hit;
  try {
    const resp = await fetch(request);
    if (resp && resp.ok) cache.put(request, resp.clone());
    return resp;
  } catch (err) {
    return hit || Response.error();
  }
}

async function staleWhileRevalidate(request, cacheName) {
  const cache = await caches.open(cacheName);
  const hit = await cache.match(request);
  const fetchPromise = fetch(request)
    .then((resp) => {
      if (resp && resp.ok) cache.put(request, resp.clone());
      return resp;
    })
    .catch(() => hit);
  return hit || fetchPromise;
}

async function networkFirst(request, cacheName) {
  const cache = await caches.open(cacheName);
  try {
    const resp = await fetch(request);
    if (resp && resp.ok) cache.put(request, resp.clone());
    return resp;
  } catch (err) {
    const hit = await cache.match(request);
    return hit || Response.error();
  }
}

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);

  // Only handle same-origin plus our known API/image origins.
  const isImage = url.pathname.startsWith("/api/images/");
  const isApi = url.pathname.startsWith("/api/fishes") || url.pathname.startsWith("/api/filters") || url.pathname === "/api/";
  const isShell = url.origin === self.location.origin && !url.pathname.startsWith("/api/");

  if (isImage) {
    event.respondWith(cacheFirst(req, IMAGE_CACHE));
  } else if (isApi) {
    event.respondWith(staleWhileRevalidate(req, API_CACHE));
  } else if (isShell) {
    event.respondWith(networkFirst(req, APP_SHELL_CACHE));
  }
});
