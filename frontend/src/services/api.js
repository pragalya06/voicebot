/**
 * Centralized API base URL configuration.
 *
 * In local dev (localhost/127.0.0.1): uses '' so requests go to '/api/...' via Vite proxy.
 * In production / on Render: connects to 'https://sevamitra-the-voicebot.onrender.com'
 * or can be overridden via VITE_API_BASE_URL / VITE_API_URL environment variables.
 */
export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  import.meta.env.VITE_API_URL ||
  (typeof window !== 'undefined' &&
   window.location.hostname !== 'localhost' &&
   window.location.hostname !== '127.0.0.1'
    ? 'https://sevamitra-the-voicebot.onrender.com'
    : '');

/**
 * Helper to construct an absolute API URL when deployed, or relative path locally.
 * @param {string} path - e.g. '/api/health'
 * @returns {string}
 */
export function apiUrl(path) {
  const cleanPath = path.startsWith('/') ? path : `/${path}`;
  return `${API_BASE_URL}${cleanPath}`;
}
