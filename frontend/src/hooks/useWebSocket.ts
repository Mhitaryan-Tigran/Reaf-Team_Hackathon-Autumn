import { useEffect, useRef, useState } from 'react';

/**
 * Хук для работы с WebSocket
 * Используется для real-time обновлений результатов проверки
 */
export const useWebSocket = <T>(url: string, enabled: boolean = true) => {
  const [data, setData] = useState<T | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    if (!enabled || !url) {
      return;
    }

    try {
      const ws = new WebSocket(url);
      wsRef.current = ws;

      ws.onopen = () => {
        console.log('WebSocket connected');
        setIsConnected(true);
        setError(null);
      };

      ws.onmessage = (event) => {
        try {
          const parsedData = JSON.parse(event.data);
          setData(parsedData);
        } catch (err) {
          console.error('Failed to parse WebSocket message:', err);
        }
      };

      ws.onerror = (event) => {
        console.error('WebSocket error:', event);
        setError(new Error('WebSocket connection error'));
      };

      ws.onclose = () => {
        console.log('WebSocket disconnected');
        setIsConnected(false);
      };
    } catch (err) {
      setError(err as Error);
    }

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [url, enabled]);

  return { data, isConnected, error };
};

// Пример использования:
// const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000';
// const { data: liveUpdate, isConnected } = useWebSocket(
//   `${WS_URL}/api/ws/checks/${checkId}`,
//   check?.status === 'in_progress'
// );

