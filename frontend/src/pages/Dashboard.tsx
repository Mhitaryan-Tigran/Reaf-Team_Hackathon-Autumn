import { FC, useEffect, useState } from 'react';
import { CheckForm } from '../components/check/CheckForm';
import { Card } from '../components/common/Card';
import { StatusBadge } from '../components/common/StatusBadge';
import { formatDate } from '../utils/format';
import { Link } from 'react-router-dom';
import { ExternalLink, Activity, Globe, RefreshCw, AlertCircle, CheckCircle2 } from 'lucide-react';
import { listChecks } from '../api/checks';
import { listAgents } from '../api/agents';
import { Check, Agent } from '../types';
import { Button } from '../components/common/Button';

export const Dashboard: FC = () => {
  const [checks, setChecks] = useState<Check[]>([]);
  const [agents, setAgents] = useState<Agent[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    try {
      setError(null);
      const [checksData, agentsData] = await Promise.all([
        listChecks().catch(() => []),
        listAgents().catch(() => [])
      ]);
      setChecks(checksData || []);
      setAgents(agentsData || []);
    } catch (err: any) {
      console.error('Failed to fetch data:', err);
      setError(err.message || 'Не удалось загрузить данные');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    
    // Auto-refresh every 15 seconds
    const interval = setInterval(fetchData, 15000);
    return () => clearInterval(interval);
  }, []);

  const onlineAgents = agents.filter(a => a.status === 'online').length;
  const totalChecks = checks.length;
  const completedChecks = checks.filter(c => c.status === 'completed').length;

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center">
        <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl mb-4">
          <Globe className="w-10 h-10 text-white" />
        </div>
        <h1 className="text-4xl font-bold text-gray-900 mb-3">
          Host Checker
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Проверьте доступность и производительность ваших хостов с разных точек мира
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="bg-gradient-to-br from-green-50 to-green-100 border-green-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-green-600 mb-1">Онлайн агентов</p>
              <p className="text-3xl font-bold text-green-900">{onlineAgents}</p>
            </div>
            <div className="p-4 bg-green-200 rounded-full">
              <Activity className="w-8 h-8 text-green-700" />
            </div>
          </div>
        </Card>

        <Card className="bg-gradient-to-br from-blue-50 to-blue-100 border-blue-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-blue-600 mb-1">Всего проверок</p>
              <p className="text-3xl font-bold text-blue-900">{totalChecks}</p>
            </div>
            <div className="p-4 bg-blue-200 rounded-full">
              <CheckCircle2 className="w-8 h-8 text-blue-700" />
            </div>
          </div>
        </Card>

        <Card className="bg-gradient-to-br from-purple-50 to-purple-100 border-purple-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-purple-600 mb-1">Завершено</p>
              <p className="text-3xl font-bold text-purple-900">{completedChecks}</p>
            </div>
            <div className="p-4 bg-purple-200 rounded-full">
              <Globe className="w-8 h-8 text-purple-700" />
            </div>
          </div>
        </Card>
      </div>

      {/* Error Alert */}
      {error && (
        <Card className="border-red-200 bg-red-50">
          <div className="flex items-center gap-3 text-red-800">
            <AlertCircle className="w-5 h-5" />
            <div>
              <p className="font-medium">Ошибка загрузки данных</p>
              <p className="text-sm text-red-600">{error}</p>
            </div>
          </div>
        </Card>
      )}

      {/* Check Form */}
      <CheckForm onCheckCreated={fetchData} />

      {/* Recent Checks */}
      <Card>
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-gray-900">Недавние проверки</h2>
          <Button
            onClick={fetchData}
            variant="secondary"
            size="sm"
            disabled={isLoading}
          >
            <RefreshCw className={`w-4 h-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
            Обновить
          </Button>
        </div>

        {isLoading ? (
          <div className="text-center py-12">
            <RefreshCw className="w-8 h-8 text-blue-600 animate-spin mx-auto mb-4" />
            <p className="text-gray-500">Загрузка проверок...</p>
          </div>
        ) : checks.length === 0 ? (
          <div className="text-center py-12">
            <Globe className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-600 font-medium mb-2">
              Проверки еще не выполнялись
            </p>
            <p className="text-gray-500 text-sm">
              Создайте первую проверку используя форму выше
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            {checks.slice(0, 10).map((check) => (
              <Link
                key={check.id}
                to={`/results/${check.id}`}
                className="block p-4 border border-gray-200 rounded-lg hover:border-blue-300 hover:bg-blue-50 transition-all duration-200 group"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4 flex-1">
                    <div className="flex-shrink-0">
                      <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center group-hover:bg-blue-200 transition-colors">
                        <Globe className="w-5 h-5 text-blue-600" />
                      </div>
                    </div>
                    <div className="flex-1 min-w-0">
                      <h3 className="font-medium text-gray-900 flex items-center space-x-2 group-hover:text-blue-600 transition-colors">
                        <span className="truncate">{check.target}</span>
                        <ExternalLink className="w-4 h-4 text-gray-400 flex-shrink-0" />
                      </h3>
                      <p className="text-sm text-gray-500">
                        {check.check_types.join(', ')} • {formatDate(check.created_at)}
                      </p>
                    </div>
                  </div>
                  <StatusBadge status={check.status} />
                </div>
              </Link>
            ))}
          </div>
        )}
      </Card>
    </div>
  );
};

