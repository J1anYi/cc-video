export function registerServiceWorker(): Promise<ServiceWorkerRegistration | null> {
  if ('serviceWorker' in navigator) {
    return navigator.serviceWorker.register('/sw.js').then((reg) => { console.log('SW registered'); return reg; }).catch((e) => { console.error('SW failed', e); return null; });
  }
  return Promise.resolve(null);
}

export function isPWA(): boolean {
  return window.matchMedia('(display-mode: standalone)').matches;
}

export function isOnline(): boolean {
  return navigator.onLine;
}

const DB_NAME = 'cc-video-offline';
const DB_VERSION = 1;

export function openOfflineDB(): Promise<IDBDatabase> {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(DB_NAME, DB_VERSION);
    request.onerror = () => reject(request.error);
    request.onsuccess = () => resolve(request.result);
    request.onupgradeneeded = (event) => {
      const db = (event.target as IDBOpenDBRequest).result;
      if (!db.objectStoreNames.contains('movies')) db.createObjectStore('movies', { keyPath: 'id' });
      if (!db.objectStoreNames.contains('pending')) db.createObjectStore('pending', { keyPath: 'id', autoIncrement: true });
    };
  });
}

export async function cacheMovieData(movie: { id: number; title: string; description?: string }): Promise<void> {
  const db = await openOfflineDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction('movies', 'readwrite');
    const store = tx.objectStore('movies');
    const req = store.put({ ...movie, cachedAt: Date.now() });
    req.onsuccess = () => resolve();
    req.onerror = () => reject(req.error);
  });
}

export async function getCachedMovies(): Promise<unknown[]> {
  const db = await openOfflineDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction('movies', 'readonly');
    const req = tx.objectStore('movies').getAll();
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}
