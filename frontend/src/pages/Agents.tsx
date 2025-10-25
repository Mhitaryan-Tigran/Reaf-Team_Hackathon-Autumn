import { FC, useEffect, useState } from 'react';
import { Card } from '../components/common/Card';
import { AgentsList } from '../components/agents/AgentsList';
import { listAgents } from '../api/agents';
import { Agent } from '../types';
import { Activity } from 'lucide-react';

export const Agents: FC = () => {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchAgents = async () => {
      try {
        const data = await listAgents();
        setAgents(data);
      } catch (error) {
        console.error('Failed to fetch agents:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchAgents();
    
    // Refresh every 10 seconds
    const interval = setInterval(fetchAgents, 10000);
    return () => clearInterval(interval);
  }, []);

  const onlineCount = agents.filter((a) => a.status === 'online').length;
  const totalCount = agents.length;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Агенты проверки</h1>
        <p className="text-gray-600">
          Управление распределенными агентами для выполнения проверок
        </p>
      </div>

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
          <p className="text-gray-500 text-center py-8">Загрузка агентов...</p>
        ) : agents.length === 0 ? (
          <p className="text-gray-500 text-center py-8">
            Агенты еще не зарегистрированы. <br/>
            Запустите агента на VPS Aeza!
          </p>
        ) : (
          <AgentsList agents={agents} />
        )}
      </Card>
    </div>
  );
};

