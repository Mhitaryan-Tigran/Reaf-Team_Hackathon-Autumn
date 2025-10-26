import apiClient from './client';
import { Check, CreateCheckRequest } from '../types';

export const createCheck = async (data: CreateCheckRequest): Promise<Check> => {
  const response = await apiClient.post<Check>('/checks', data);
  return response.data;
};

export const getCheck = async (checkId: string): Promise<Check> => {
  const response = await apiClient.get<Check>(`/checks/${checkId}`);
  return response.data;
};

export const listChecks = async (): Promise<Check[]> => {
  const response = await apiClient.get<Check[]>('/checks');
  return response.data;
};

export const deleteCheck = async (checkId: string): Promise<void> => {
  await apiClient.delete(`/checks/${checkId}`);
};
