import { FC, memo } from 'react';
import { MapPin, Activity } from 'lucide-react';
import { Agent } from '../../types';
import { StatusBadge } from '../common/StatusBadge';
import { formatDate } from '../../utils/format';

interface AgentCardProps {
  agent: Agent;
}

const AgentCardComponent: FC<AgentCardProps> = ({ agent }) => {
  return (
    <div className="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-lg transition-shadow">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center space-x-3">
          <div className={`p-2 rounded-full ${agent.status === 'online' ? 'bg-green-100' : 'bg-gray-100'}`}>
            <Activity className={`w-5 h-5 ${agent.status === 'online' ? 'text-green-600' : 'text-gray-400'}`} />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-900">{agent.name}</h3>
            <div className="flex items-center text-sm text-gray-500 mt-1">
              <MapPin className="w-4 h-4 mr-1" />
              {agent.location}
            </div>
          </div>
        </div>
        <StatusBadge status={agent.status} type="agent" />
      </div>

      <div className="space-y-2 text-sm">
        <div className="flex justify-between">
          <span className="text-gray-500">Последний heartbeat:</span>
          <span className="text-gray-900 font-medium">{formatDate(agent.last_heartbeat)}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-500">Зарегистрирован:</span>
          <span className="text-gray-900 font-medium">{formatDate(agent.registered_at)}</span>
        </div>
        {agent.metadata?.ip && (
          <div className="flex justify-between">
            <span className="text-gray-500">IP:</span>
            <span className="text-gray-900 font-medium">{agent.metadata.ip}</span>
          </div>
        )}
      </div>
    </div>
  );
};

export const AgentCard = memo(AgentCardComponent);

