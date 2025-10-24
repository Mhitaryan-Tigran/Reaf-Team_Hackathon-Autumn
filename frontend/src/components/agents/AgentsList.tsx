import { FC } from 'react';
import { Agent } from '../../types';
import { AgentCard } from './AgentCard';

interface AgentsListProps {
  agents: Agent[];
}

export const AgentsList: FC<AgentsListProps> = ({ agents }) => {
  if (agents.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500 text-lg">Агенты не найдены</p>
        <p className="text-gray-400 text-sm mt-2">
          Зарегистрируйте агенты для выполнения проверок
        </p>
      </div>
    );
  }

  const onlineAgents = agents.filter((a) => a.status === 'online');
  const offlineAgents = agents.filter((a) => a.status === 'offline');

  return (
    <div className="space-y-8">
      {onlineAgents.length > 0 && (
        <div>
          <h2 className="text-xl font-semibold mb-4 text-gray-900">
            Онлайн агенты ({onlineAgents.length})
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {onlineAgents.map((agent) => (
              <AgentCard key={agent.id} agent={agent} />
            ))}
          </div>
        </div>
      )}

      {offlineAgents.length > 0 && (
        <div>
          <h2 className="text-xl font-semibold mb-4 text-gray-900">
            Оффлайн агенты ({offlineAgents.length})
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {offlineAgents.map((agent) => (
              <AgentCard key={agent.id} agent={agent} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

