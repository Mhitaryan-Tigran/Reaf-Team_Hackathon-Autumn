import axios from 'axios';

// Получаем URL API из переменных окружения
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Создаем экземпляр axios с базовой конфигурацией
export const apiClient = axios.create({
  baseURL: `${API_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

// Интерсептор для обработки ошибок
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export default apiClient;

