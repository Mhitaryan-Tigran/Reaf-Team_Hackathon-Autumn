import axios, { AxiosError } from 'axios';

// Получаем URL API из переменных окружения
// Важно: на Vercel установите переменную окружения VITE_API_URL
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

console.log('🔗 API URL:', API_URL);

// Создаем экземпляр axios с базовой конфигурацией
export const apiClient = axios.create({
  baseURL: `${API_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // Увеличили таймаут для медленных проверок
  withCredentials: false, // Не отправляем куки для CORS
});

// Интерсептор для логирования запросов (в dev режиме)
apiClient.interceptors.request.use(
  (config) => {
    if (import.meta.env.DEV) {
      console.log(`🔵 API Request: ${config.method?.toUpperCase()} ${config.url}`);
    }
    return config;
  },
  (error) => {
    console.error('❌ Request Error:', error);
    return Promise.reject(error);
  }
);

// Интерсептор для обработки ошибок
apiClient.interceptors.response.use(
  (response) => {
    if (import.meta.env.DEV) {
      console.log(`🟢 API Response: ${response.config.url}`, response.data);
    }
    return response;
  },
  (error: AxiosError) => {
    console.error('❌ API Error:', error.message);
    
    // Более детальная обработка ошибок
    if (error.response) {
      // Сервер ответил с кодом ошибки
      console.error('Response Error:', error.response.status, error.response.data);
    } else if (error.request) {
      // Запрос был отправлен, но ответа не было
      console.error('No Response:', error.request);
    } else {
      // Что-то пошло не так при настройке запроса
      console.error('Request Setup Error:', error.message);
    }
    
    return Promise.reject(error);
  }
);

export default apiClient;

