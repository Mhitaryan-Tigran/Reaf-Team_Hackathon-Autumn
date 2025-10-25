export interface Check {
  id: string;
  target: string;
  check_types: string[];
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
  created_at: string;
  completed_at?: string;
  results?: CheckResult[];
}

export interface CheckResult {
  id: string;
  check_id: string;
  agent_id: string;
  agent_name: string;
  agent_location: string;
  check_type: string;
  success: boolean;
  data: Record<string, any>;
  error?: string;
  duration_ms: number;
  created_at: string;
}

export interface Agent {
  id: string;
  name: string;
  location: string;
  status: 'online' | 'offline';
  last_heartbeat: string;
  registered_at: string;
  metadata?: Record<string, any>;
}

export interface CreateCheckRequest {
  target: string;
  checks: string[];
  agents?: string[];
}

export const CHECK_TYPES = {
  http: 'HTTP/HTTPS',
  ping: 'Ping',
  dns: 'DNS Lookup',
  tcp: 'TCP Port',
  traceroute: 'Traceroute',
} as const;

export const CHECK_STATUS_COLORS = {
  pending: 'bg-yellow-100 text-yellow-800',
  in_progress: 'bg-blue-100 text-blue-800',
  completed: 'bg-green-100 text-green-800',
  failed: 'bg-red-100 text-red-800',
} as const;

export const AGENT_STATUS_COLORS = {
  online: 'bg-green-100 text-green-800',
  offline: 'bg-gray-100 text-gray-800',
} as const;

