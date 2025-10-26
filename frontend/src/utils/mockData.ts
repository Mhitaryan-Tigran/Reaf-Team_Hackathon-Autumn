import { Agent, Check, CheckResult } from '../types';

export const mockAgents: Agent[] = [
  {
    id: '1',
    name: 'Moscow-1',
    location: 'Moscow, Russia',
    status: 'online',
    last_heartbeat: new Date(Date.now() - 5000).toISOString(),
    registered_at: new Date(Date.now() - 86400000).toISOString(),
    metadata: { ip: '185.123.45.67' },
  },
  {
    id: '2',
    name: 'London-1',
    location: 'London, UK',
    status: 'online',
    last_heartbeat: new Date(Date.now() - 3000).toISOString(),
    registered_at: new Date(Date.now() - 172800000).toISOString(),
    metadata: { ip: '51.124.78.90' },
  },
  {
    id: '3',
    name: 'Tokyo-1',
    location: 'Tokyo, Japan',
    status: 'offline',
    last_heartbeat: new Date(Date.now() - 120000).toISOString(),
    registered_at: new Date(Date.now() - 259200000).toISOString(),
    metadata: { ip: '133.45.67.89' },
  },
];

export const mockCheckResults: CheckResult[] = [
  {
    id: '1',
    check_id: '1',
    agent_id: '1',
    agent_name: 'Moscow-1',
    agent_location: 'Moscow, Russia',
    check_type: 'http',
    success: true,
    data: {
      status_code: 200,
      headers: { 'content-type': 'text/html' },
      body_size: 15234,
    },
    duration_ms: 45,
    created_at: new Date().toISOString(),
  },
  {
    id: '2',
    check_id: '1',
    agent_id: '2',
    agent_name: 'London-1',
    agent_location: 'London, UK',
    check_type: 'http',
    success: true,
    data: {
      status_code: 200,
      headers: { 'content-type': 'text/html' },
      body_size: 15234,
    },
    duration_ms: 120,
    created_at: new Date().toISOString(),
  },
  {
    id: '3',
    check_id: '1',
    agent_id: '1',
    agent_name: 'Moscow-1',
    agent_location: 'Moscow, Russia',
    check_type: 'ping',
    success: true,
    data: {
      latency_ms: 23.5,
      packets_sent: 4,
      packets_received: 4,
      packet_loss: 0,
    },
    duration_ms: 3000,
    created_at: new Date().toISOString(),
  },
  {
    id: '4',
    check_id: '1',
    agent_id: '2',
    agent_name: 'London-1',
    agent_location: 'London, UK',
    check_type: 'ping',
    success: true,
    data: {
      latency_ms: 89.2,
      packets_sent: 4,
      packets_received: 4,
      packet_loss: 0,
    },
    duration_ms: 3000,
    created_at: new Date().toISOString(),
  },
  {
    id: '5',
    check_id: '1',
    agent_id: '1',
    agent_name: 'Moscow-1',
    agent_location: 'Moscow, Russia',
    check_type: 'dns',
    success: true,
    data: {
      ip_addresses: ['142.250.185.46', '2a00:1450:4010:c08::8a'],
      dns_servers: ['8.8.8.8'],
    },
    duration_ms: 15,
    created_at: new Date().toISOString(),
  },
];

export const mockCheck: Check = {
  id: '1',
  target: 'google.com',
  check_types: ['http', 'ping', 'dns'],
  status: 'completed',
  created_at: new Date(Date.now() - 60000).toISOString(),
  completed_at: new Date(Date.now() - 30000).toISOString(),
  results: mockCheckResults,
};

export const mockChecks: Check[] = [
  mockCheck,
  {
    id: '2',
    target: 'github.com',
    check_types: ['http', 'ping'],
    status: 'in_progress',
    created_at: new Date(Date.now() - 30000).toISOString(),
  },
  {
    id: '3',
    target: 'example.com',
    check_types: ['http', 'dns'],
    status: 'failed',
    created_at: new Date(Date.now() - 120000).toISOString(),
    completed_at: new Date(Date.now() - 90000).toISOString(),
  },
];
