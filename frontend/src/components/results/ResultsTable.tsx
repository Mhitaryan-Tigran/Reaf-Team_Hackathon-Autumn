import { FC } from 'react';
import { CheckResult, CHECK_TYPES } from '../../types';
import { formatDuration } from '../../utils/format';
import { CheckCircle2, XCircle } from 'lucide-react';

interface ResultsTableProps {
  results: CheckResult[];
}

export const ResultsTable: FC<ResultsTableProps> = ({ results }) => {
  if (results.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        Результаты пока отсутствуют
      </div>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Статус
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Агент
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Проверка
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Время
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Детали
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {results.map((result) => (
            <tr key={result.id} className="hover:bg-gray-50">
              <td className="px-6 py-4 whitespace-nowrap">
                {result.success ? (
                  <CheckCircle2 className="w-5 h-5 text-green-600" />
                ) : (
                  <XCircle className="w-5 h-5 text-red-600" />
                )}
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <div className="text-sm font-medium text-gray-900">
                  {result.agent_name}
                </div>
                <div className="text-sm text-gray-500">
                  {result.agent_location}
                </div>
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {CHECK_TYPES[result.check_type as keyof typeof CHECK_TYPES] || result.check_type}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {formatDuration(result.duration_ms)}
              </td>
              <td className="px-6 py-4 text-sm text-gray-500">
                {result.success ? (
                  <span className="text-green-600">Успешно</span>
                ) : (
                  <span className="text-red-600">{result.error || 'Ошибка'}</span>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

