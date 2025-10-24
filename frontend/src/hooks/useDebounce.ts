import { useState, useEffect } from 'react';

/**
 * Хук для debounce значения
 * Полезен для оптимизации поиска и валидации
 */
export const useDebounce = <T>(value: T, delay: number = 500): T => {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
};

// Пример использования:
// const searchTerm = useDebounce(inputValue, 500);
// useEffect(() => {
//   // Выполнить поиск только после того, как пользователь перестал печатать
//   searchAPI(searchTerm);
// }, [searchTerm]);

