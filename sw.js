// Service worker: la app abre sin conexión; el banco de preguntas se actualiza cuando hay red.
const CACHE = "plaza-docente-v12";
const ESTATICOS = ["./", "index.html", "css/app.css?v=11", "js/config.js?v=11", "js/extra.js?v=11", "js/app.js?v=11", "manifest.webmanifest",
  "icons/icon-192.png", "icons/apple-touch-icon.png", "simulacro.ics"];
self.addEventListener("install", e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(ESTATICOS)).then(() => self.skipWaiting())); });
self.addEventListener("activate", e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener("fetch", e => {
  const url = new URL(e.request.url);
  if (e.request.method !== "GET" || url.origin !== location.origin) return; // Supabase va directo a la red
  const red = url.pathname.includes("/data/") || e.request.mode === "navigate";
  if (red) {
    e.respondWith(fetch(e.request).then(r => { const cp = r.clone(); caches.open(CACHE).then(c => c.put(e.request, cp)); return r; })
      .catch(() => caches.match(e.request).then(r => r || caches.match("index.html"))));
  } else {
    e.respondWith(caches.match(e.request).then(r => r || fetch(e.request).then(res => { const cp = res.clone(); caches.open(CACHE).then(c => c.put(e.request, cp)); return res; })));
  }
});

// Recordatorios (notificaciones push)
self.addEventListener("push", e => {
  let d = {}; try { d = e.data.json(); } catch { d = { title: "Plaza Docente", body: e.data ? e.data.text() : "Tu reto de hoy te espera" }; }
  e.waitUntil(self.registration.showNotification(d.title || "Plaza Docente", {
    body: d.body || "", icon: "icons/icon-192.png", badge: "icons/icon-192.png", tag: d.tag || "plaza", renotify: true, data: { url: d.url || "./" } }));
});
self.addEventListener("notificationclick", e => {
  e.notification.close();
  const url = (e.notification.data && e.notification.data.url) || "./";
  e.waitUntil(clients.matchAll({ type: "window", includeUncontrolled: true }).then(cs => {
    for (const c of cs) if ("focus" in c) return c.focus();
    return clients.openWindow(url);
  }));
});
