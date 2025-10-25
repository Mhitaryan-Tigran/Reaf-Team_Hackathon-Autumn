import { FC, memo } from 'react';
import { CheckCircle2, XCircle, Clock } from 'lucide-react';
import { CheckResult, CHECK_TYPES } from '../../types';
import { formatDuration } from '../../utils/format';

interface ResultCardProps {
  result: CheckResult;
}

const ResultCardComponent: FC<ResultCardProps> = ({ result }) => {
  const checkTypeName = CHECK_TYPES[result.check_type as keyof typeof CHECK_TYPES] || result.check_type;

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4">
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center space-x-2">
          {result.success ? (
            <CheckCircle2 className="w-5 h-5 text-green-600" />
          ) : (
            <XCircle className="w-5 h-5 text-red-600" />
          )}
          <div>
            <h4 className="font-medium text-gray-900">{checkTypeName}</h4>
            <p className="text-sm text-gray-500">{result.agent_location}</p>
          </div>
        </div>
        <div className="flex items-center space-x-1 text-sm text-gray-500">
          <Clock className="w-4 h-4" />
          <span>{formatDuration(result.duration_ms)}</span>
        </div>
      </div>

      {result.success ? (
        <div className="space-y-1">
          {result.check_type === 'http' && result.data.status_code && (
            <p className="text-sm text-gray-600">
              Статус: <span className="font-medium">{result.data.status_code}</span>
            </p>
          )}
          {result.check_type === 'ping' && result.data.latency_ms && (
            <p className="text-sm text-gray-600">
              Задержка: <span className="font-medium">{result.data.latency_ms.toFixed(1)} мс</span>
            </p>
          )}
          {result.check_type === 'dns' && result.data.ip_addresses && (
            <p className="text-sm text-gray-600">
              IP: <span className="font-medium">{result.data.ip_addresses.join(', ')}</span>
            </p>
          )}
        </div>
      ) : (
        <p className="text-sm text-red-600">{result.error || 'Неизвестная ошибка'}</p>
      )}
    </div>
  );
};

export const ResultCard = memo(ResultCardComponent);

