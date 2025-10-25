import { FC, memo } from 'react';
import { CheckCircle2, XCircle, Clock, Globe, Wifi, Server, Network, Route, Activity } from 'lucide-react';
import { CheckResult, CHECK_TYPES } from '../../types';
import { formatDuration } from '../../utils/format';

interface ResultCardProps {
  result: CheckResult;
}

const getCheckIcon = (checkType: string, success: boolean) => {
  const color = success ? 'text-green-600' : 'text-red-600';
  const bgColor = success ? 'bg-green-100' : 'bg-red-100';
  
  let Icon = Activity;
  if (checkType === 'http') Icon = Globe;
  else if (checkType === 'ping') Icon = Wifi;
  else if (checkType === 'dns') Icon = Server;
  else if (checkType === 'tcp') Icon = Network;
  else if (checkType === 'traceroute') Icon = Route;

  return (
    <div className={`p-2 rounded-lg ${bgColor}`}>
      <Icon className={`w-5 h-5 ${color}`} />
    </div>
  );
};

const ResultCardComponent: FC<ResultCardProps> = ({ result }) => {
  const checkTypeName = CHECK_TYPES[result.check_type as keyof typeof CHECK_TYPES] || result.check_type;

  const renderDetails = () => {
    if (!result.success) {
      return (
        <div className="bg-red-50 border border-red-200 rounded p-3">
          <div className="flex items-start gap-2">
            <XCircle className="w-4 h-4 text-red-600 flex-shrink-0 mt-0.5" />
            <p className="text-sm text-red-700">{result.error || 'Неизвестная ошибка'}</p>
          </div>
        </div>
      );
    }

    const data = result.data;

    // HTTP проверка
    if (result.check_type === 'http') {
      return (
        <div className="space-y-2">
          {data.status_code && (
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">HTTP статус:</span>
              <span className={`font-medium px-2 py-1 rounded text-sm ${
                data.status_code >= 200 && data.status_code < 300 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-yellow-100 text-yellow-800'
              }`}>
                {data.status_code}
              </span>
            </div>
          )}
          {data.response_time_ms && (
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Время ответа:</span>
              <span className="text-sm font-medium">{data.response_time_ms} мс</span>
            </div>
          )}
          {data.content_length && (
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Размер:</span>
              <span className="text-sm font-medium">{(data.content_length / 1024).toFixed(2)} КБ</span>
            </div>
          )}
        </div>
      );
    }

    // Ping проверка
    if (result.check_type === 'ping') {
      return (
        <div className="space-y-2">
          {data.latency_ms !== undefined && (
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Задержка:</span>
              <span className="text-sm font-medium text-blue-600">{data.latency_ms.toFixed(1)} мс</span>
            </div>
          )}
          {data.packet_loss !== undefined && (
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Потеря пакетов:</span>
              <span className="text-sm font-medium">{data.packet_loss}%</span>
            </div>
          )}
          {data.packets_transmitted !== undefined && (
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Пакетов:</span>
              <span className="text-sm font-medium">{data.packets_transmitted}</span>
            </div>
          )}
        </div>
      );
    }

    // DNS проверка
    if (result.check_type === 'dns') {
      return (
        <div className="space-y-2">
          {data.ip_addresses && data.ip_addresses.length > 0 && (
            <div>
              <span className="text-sm text-gray-600 block mb-1">IP адреса:</span>
              <div className="space-y-1">
                {data.ip_addresses.map((ip: string, idx: number) => (
                  <span key={idx} className="text-sm font-mono bg-gray-100 px-2 py-1 rounded block">
                    {ip}
                  </span>
                ))}
              </div>
            </div>
          )}
          {data.mx_records && data.mx_records.length > 0 && (
            <div>
              <span className="text-sm text-gray-600 block mb-1">MX записи:</span>
              <div className="space-y-1">
                {data.mx_records.map((mx: string, idx: number) => (
                  <span key={idx} className="text-xs font-mono bg-gray-100 px-2 py-1 rounded block">
                    {mx}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      );
    }

    // TCP проверка
    if (result.check_type === 'tcp') {
      return (
        <div className="space-y-2">
          {data.port && (
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Порт:</span>
              <span className="text-sm font-medium">{data.port}</span>
            </div>
          )}
          {data.connection_time_ms !== undefined && (
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Время подключения:</span>
              <span className="text-sm font-medium">{data.connection_time_ms} мс</span>
            </div>
          )}
          <div className="flex items-center gap-2 text-sm text-green-600">
            <CheckCircle2 className="w-4 h-4" />
            <span>Порт доступен</span>
          </div>
        </div>
      );
    }

    // Traceroute проверка
    if (result.check_type === 'traceroute') {
      return (
        <div className="space-y-2">
          {data.hops && (
            <div>
              <span className="text-sm text-gray-600 block mb-1">Хопов: {data.hops.length}</span>
              <div className="max-h-32 overflow-y-auto space-y-1">
                {data.hops.slice(0, 5).map((hop: any, idx: number) => (
                  <div key={idx} className="text-xs font-mono bg-gray-50 px-2 py-1 rounded">
                    {hop.ip || hop}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      );
    }

    // Общий случай - показываем raw data
    return (
      <div className="bg-gray-50 rounded p-3">
        <pre className="text-xs text-gray-700 overflow-auto max-h-32">
          {JSON.stringify(data, null, 2)}
        </pre>
      </div>
    );
  };

  return (
    <div className={`border-2 rounded-lg p-4 transition-all hover:shadow-md ${
      result.success ? 'border-green-200 bg-green-50' : 'border-red-200 bg-red-50'
    }`}>
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          {getCheckIcon(result.check_type, result.success)}
          <div>
            <h4 className="font-semibold text-gray-900">{checkTypeName}</h4>
            <div className="flex items-center gap-2 mt-1">
              <Server className="w-3 h-3 text-gray-400" />
              <p className="text-sm text-gray-600">{result.agent_name}</p>
            </div>
            <p className="text-xs text-gray-500">{result.agent_location}</p>
          </div>
        </div>
        <div className="flex items-center gap-1 text-sm text-gray-500 bg-white px-2 py-1 rounded">
          <Clock className="w-4 h-4" />
          <span>{formatDuration(result.duration_ms)}</span>
        </div>
      </div>

      {/* Details */}
      {renderDetails()}
    </div>
  );
};

export const ResultCard = memo(ResultCardComponent);

