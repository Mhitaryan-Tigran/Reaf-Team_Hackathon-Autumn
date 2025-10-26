import apiClient from './client';
import { Agent } from '../types';

export const listAgents = async (): Promise<Agent[]> => {
  const response = await apiClient.get<Agent[]>('/agents');
  return response.data;
};

export const getAgent = async (agentId: string): Promise<Agent> => {
  const response = await apiClient.get<Agent>(`/agents/${agentId}`);
  return response.data;
};

export const registerAgent = async (data: {
  name: string;
  location: string;
}): Promise<{ agent_id: string; api_token: string }> => {
  const response = await apiClient.post('/agents/register', data, {
    headers: {
      'X-Registration-Token': 'master-registration-token',
    },
  });
  return response.data;
};

export const getAgentStats = async (agentId: string): Promise<any> => {
  const response = await apiClient.get(`/agents/${agentId}/stats`);
  return response.data;
};
