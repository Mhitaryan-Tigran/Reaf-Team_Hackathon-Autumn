import apiClient from './client';
import { Agent } from '../types';

// API методы для работы с агентами

/**
 * Получить список всех агентов
 */
export const listAgents = async (): Promise<Agent[]> => {
  const response = await apiClient.get<Agent[]>('/agents');
  return response.data;
};

/**
 * Получить информацию об агенте по ID
 */
export const getAgent = async (agentId: string): Promise<Agent> => {
  const response = await apiClient.get<Agent>(`/agents/${agentId}`);
  return response.data;
};

/**
 * Зарегистрировать нового агента
 */
export const registerAgent = async (data: {
  name: string;
  location: string;
}): Promise<{ agent_id: string; api_token: string }> => {
  const response = await apiClient.post('/agents/register', data, {
    headers: {
      'X-Registration-Token': 'master-registration-token', // В продакшене брать из env
    },
  });
  return response.data;
};

/**
 * Получить статистику агента
 */
export const getAgentStats = async (agentId: string): Promise<any> => {
  const response = await apiClient.get(`/agents/${agentId}/stats`);
  return response.data;
};

// Пример использования в компоненте:
// import { listAgents } from '../api/agents';
//
// const fetchAgents = async () => {
//   try {
//     const agents = await listAgents();
//     setAgents(agents);
//   } catch (error) {
//     console.error('Failed to fetch agents:', error);
//   }
// };

