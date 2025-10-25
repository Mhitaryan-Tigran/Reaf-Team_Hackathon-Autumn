import { useEffect, useRef, useState } from 'react';

/**
 * Хук для периодического опроса данных
 * Используется для обновления результатов проверки
 */
export const usePolling = <T>(
  fetchFn: () => Promise<T>,
  interval: number = 2000,
  enabled: boolean = true
) => {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<Error | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const intervalRef = useRef<number | null>(null);

  useEffect(() => {
    if (!enabled) {
      setIsLoading(false);
      return;
    }

    const poll = async () => {
      try {
        const result = await fetchFn();
        setData(result);
        setError(null);
      } catch (err) {
        setError(err as Error);
      } finally {
        setIsLoading(false);
      }
    };

    // Первый запрос сразу
    poll();

    // Запускаем интервал
    intervalRef.current = setInterval(poll, interval);

    // Очистка при размонтировании
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [fetchFn, interval, enabled]);

  return { data, error, isLoading };
};

// Пример использования:
// const { data: check, isLoading } = usePolling(
//   () => getCheck(checkId),
//   2000,
//   check?.status !== 'completed'
// );

