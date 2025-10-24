// API URLs
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
export const WS_BASE_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000';

// Polling intervals (ms)
export const POLLING_INTERVALS = {
  CHECK_RESULTS: 2000,
  AGENTS_STATUS: 5000,
  HEARTBEAT: 10000,
} as const;

// Pagination
export const ITEMS_PER_PAGE = {
  CHECKS: 10,
  AGENTS: 20,
  RESULTS: 50,
} as const;

// Timeouts (ms)
export const TIMEOUTS = {
  API_REQUEST: 10000,
  WEBSOCKET_RECONNECT: 5000,
} as const;

// Routes
export const ROUTES = {
  HOME: '/',
  RESULTS: '/results',
  AGENTS: '/agents',
} as const;

// Local Storage Keys
export const STORAGE_KEYS = {
  THEME: 'host-checker-theme',
  RECENT_CHECKS: 'host-checker-recent-checks',
} as const;

