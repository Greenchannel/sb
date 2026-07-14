const CACHE_NAME = 'site-nav-v1';
const CACHE_URLS = [
  'index.html',
  'manifest.json',
  'css/tone.css',
  'css/style.css',
  'css/glass.css',
  'proxys/edgetunnel.html'
];

// 安装：预缓存核心资源
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(CACHE_URLS);
    })
  );
  self.skipWaiting();
});

// 激活：清理旧缓存
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(name => {
          if (name !== CACHE_NAME) {
            return caches.delete(name);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// 拦截请求：缓存优先 + 网络回退
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(cached => {
      if (cached) return cached;
      return fetch(event.request).then(response => {
        // 只缓存同源资源
        if (response && response.status === 200 && 
            event.request.url.startsWith(self.location.origin) &&
            !event.request.url.includes('chrome-extension')) {
          const cloned = response.clone();
          caches.open(CACHE_NAME).then(cache => {
            cache.put(event.request, cloned);
          });
        }
        return response;
      }).catch(() => {
        // 离线时返回缓存中的 fallback
        return caches.match('index.html');
      });
    })
  );
});