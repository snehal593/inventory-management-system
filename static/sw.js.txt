// A simple Service Worker to satisfy PWA installation requirements
self.addEventListener('install', (event) => {
    console.log('Service Worker: Installed');
});

self.addEventListener('fetch', (event) => {
    // This allows the app to fetch data from the internet normally
    event.respondWith(fetch(event.request));
});