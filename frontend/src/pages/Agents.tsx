import { FC, useEffect, useState } from 'react';
import { Card } from '../components/common/Card';
import { AgentsList } from '../components/agents/AgentsList';
import { listAgents } from '../api/agents';
import { Agent } from '../types';
import { Activity, AlertCircle, RefreshCw, Server } from 'lucide-react';
import { Button } from '../components/common/Button';

export const Agents: FC = () => {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());

  const fetchAgents = async () => {
    try {
      setError(null);
      const data = await listAgents();
      setAgents(data || []);
      setLastUpdate(new Date());
    } catch (err: any) {
      console.error('Failed to fetch agents:', err);
      setError(err.message || 'Не удалось загрузить список агентов');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchAgents();
    
    // Refresh every 10 seconds
    const interval = setInterval(fetchAgents, 10000);
    return () => clearInterval(interval);
  }, []);

  const onlineCount = agents.filter((a) => a.status === 'online').length;
  const totalCount = agents.length;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2 flex items-center gap-3">
            <Server className="w-8 h-8 text-blue-600" />
            Агенты проверки
          </h1>
          <p className="text-gray-600">
            Управление распределенными агентами для выполнения проверок
          </p>
        </div>
        <div className="text-right">
          <Button
            onClick={fetchAgents}
            variant="secondary"
            disabled={isLoading}
          >
            <RefreshCw className={`w-4 h-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
            Обновить
          </Button>
          <p className="text-xs text-gray-500 mt-2">
            Обновлено: {lastUpdate.toLocaleTimeString('ru-RU')}
          </p>
        </div>
      </div>

      {error && (
        <Card className="border-red-200 bg-red-50">
          <div className="flex items-center gap-3 text-red-800">
            <AlertCircle className="w-5 h-5" />
            <div>
              <p className="font-medium">Ошибка загрузки</p>
              <p className="text-sm text-red-600">{error}</p>
            </div>
          </div>
        </Card>
      )}

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-green-100 rounded-full">
              <Activity className="w-6 h-6 text-green-600" />
            </div>
            <div>
              <p className="text-sm text-gray-500">Онлайн агентов</p>
              <p className="text-2xl font-bold text-gray-900">{onlineCount}</p>
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-gray-100 rounded-full">
              <Activity className="w-6 h-6 text-gray-600" />
            </div>
            <div>
              <p className="text-sm text-gray-500">Всего агентов</p>
              <p className="text-2xl font-bold text-gray-900">{totalCount}</p>
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center space-x-3">
            <div className="p-3 bg-blue-100 rounded-full">
              <Activity className="w-6 h-6 text-blue-600" />
            </div>
            <div>
              <p className="text-sm text-gray-500">Работоспособность</p>
              <p className="text-2xl font-bold text-gray-900">
                {totalCount > 0 ? Math.round((onlineCount / totalCount) * 100) : 0}%
              </p>
            </div>
          </div>
        </Card>
      </div>

      <Card>
        {isLoading ? (
          <div className="text-center py-12">
            <RefreshCw className="w-8 h-8 text-blue-600 animate-spin mx-auto mb-4" />
            <p className="text-gray-500">Загрузка агентов...</p>
          </div>
        ) : agents.length === 0 ? (
          <div className="text-center py-12">
            <Server className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-600 font-medium mb-2">
              Агенты еще не зарегистрированы
            </p>
            <p className="text-gray-500 text-sm">
              Запустите агента на VPS Aeza для выполнения проверок
            </p>
          </div>
        ) : (
          <AgentsList agents={agents} />
        )}
      </Card>
    </div>
  );
};

