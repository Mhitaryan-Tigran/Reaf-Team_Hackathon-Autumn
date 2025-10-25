import { FC, useEffect, useState } from 'react';
import { CheckForm } from '../components/check/CheckForm';
import { Card } from '../components/common/Card';
import { StatusBadge } from '../components/common/StatusBadge';
import { formatDate } from '../utils/format';
import { Link } from 'react-router-dom';
import { ExternalLink } from 'lucide-react';
import { listChecks } from '../api/checks';
import { Check } from '../types';

export const Dashboard: FC = () => {
  const [checks, setChecks] = useState<Check[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchChecks = async () => {
      try {
        const data = await listChecks();
        setChecks(data);
      } catch (error) {
        console.error('Failed to fetch checks:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchChecks();
  }, []);

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Host Checker Dashboard
        </h1>
        <p className="text-gray-600">
          Проверьте доступность и производительность ваших хостов с разных точек мира
        </p>
      </div>

      <CheckForm />

      <Card title="Недавние проверки">
        {isLoading ? (
          <p className="text-gray-500 text-center py-8">
            Загрузка...
          </p>
        ) : checks.length === 0 ? (
          <p className="text-gray-500 text-center py-8">
            Проверки еще не выполнялись
          </p>
        ) : (
          <div className="space-y-4">
            {checks.map((check) => (
              <Link
                key={check.id}
                to={`/results/${check.id}`}
                className="block p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <div>
                      <h3 className="font-medium text-gray-900 flex items-center space-x-2">
                        <span>{check.target}</span>
                        <ExternalLink className="w-4 h-4 text-gray-400" />
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

