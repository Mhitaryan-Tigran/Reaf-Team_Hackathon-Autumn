import apiClient from './client';
import { Check, CreateCheckRequest } from '../types';

// API методы для работы с проверками

/**
 * Создать новую проверку
 */
export const createCheck = async (data: CreateCheckRequest): Promise<Check> => {
  const response = await apiClient.post<Check>('/checks', data);
  return response.data;
};

/**
 * Получить информацию о проверке по ID
 */
export const getCheck = async (checkId: string): Promise<Check> => {
  const response = await apiClient.get<Check>(`/checks/${checkId}`);
  return response.data;
};

/**
 * Получить список всех проверок
 */
export const listChecks = async (): Promise<Check[]> => {
  const response = await apiClient.get<Check[]>('/checks');
  return response.data;
};

/**
 * Удалить проверку
 */
export const deleteCheck = async (checkId: string): Promise<void> => {
  await apiClient.delete(`/checks/${checkId}`);
};

// Пример использования в компоненте:
// import { createCheck } from '../api/checks';
//
// const handleSubmit = async (data: CreateCheckRequest) => {
//   try {
//     const check = await createCheck(data);
//     navigate(`/results/${check.id}`);
//   } catch (error) {
//     console.error('Failed to create check:', error);
//   }
// };

