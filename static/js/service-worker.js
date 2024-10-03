const CACHE_NAME = 'seguranca-cache-v1';
const urlsToCache = [
  '/',
  '/static/css/style.css',
  '/static/js/service-worker.js',
  '/static/icons/icon-192x192.png',
  '/static/icons/icon-512x512.png'
];

// Instala o service worker e adiciona os arquivos ao cache
self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        return cache.addAll(urlsToCache);
      })
  );
});

// Responde às solicitações com recursos do cache
self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        return response || fetch(event.request);
      })
  );
});

// Remove caches antigos durante a ativação do service worker
self.addEventListener('activate', function(event) {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then(function(cacheNames) {
      return Promise.all(
        cacheNames.map(function(cacheName) {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});
