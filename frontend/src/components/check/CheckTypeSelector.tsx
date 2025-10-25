import { FC, useCallback, useMemo } from 'react';
import { CHECK_TYPES } from '../../types';

interface CheckTypeSelectorProps {
  selectedTypes: string[];
  onChange: (types: string[]) => void;
}

export const CheckTypeSelector: FC<CheckTypeSelectorProps> = ({ selectedTypes, onChange }) => {
  const checkTypeEntries = useMemo(() => Object.entries(CHECK_TYPES), []);

  const handleToggle = useCallback((type: string) => {
    if (selectedTypes.includes(type)) {
      onChange(selectedTypes.filter((t) => t !== type));
    } else {
      onChange([...selectedTypes, type]);
    }
  }, [selectedTypes, onChange]);

  return (
    <div className="space-y-2">
      <label className="block text-sm font-medium text-gray-700">
        Типы проверок
      </label>
      <div className="grid grid-cols-2 gap-2">
        {checkTypeEntries.map(([key, label]) => (
          <label
            key={key}
            className="flex items-center p-3 border border-gray-300 rounded-lg cursor-pointer hover:bg-gray-50 transition-colors"
          >
            <input
              type="checkbox"
              checked={selectedTypes.includes(key)}
              onChange={() => handleToggle(key)}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <span className="ml-2 text-sm text-gray-700">{label}</span>
          </label>
        ))}
      </div>
    </div>
  );
};

