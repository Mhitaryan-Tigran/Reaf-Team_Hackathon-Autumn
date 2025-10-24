import { FC } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Card } from '../components/common/Card';
import { StatusBadge } from '../components/common/StatusBadge';
import { ResultsTable } from '../components/results/ResultsTable';
import { ResultCard } from '../components/results/ResultCard';
import { mockCheck, mockChecks } from '../utils/mockData';
import { formatDate } from '../utils/format';
import { ArrowLeft, RefreshCw } from 'lucide-react';
import { Button } from '../components/common/Button';

export const Results: FC = () => {
  const { checkId } = useParams<{ checkId: string }>();

  // В будущем здесь будет реальный API вызов
  const check = checkId === '1' ? mockCheck : mockChecks.find((c) => c.id === checkId) || mockCheck;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Link
            to="/"
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
          </Link>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">{check.target}</h1>
            <p className="text-gray-600">Создано: {formatDate(check.created_at)}</p>
          </div>
        </div>
        <div className="flex items-center space-x-3">
          <StatusBadge status={check.status} />
          <Button variant="secondary" size="sm">
            <RefreshCw className="w-4 h-4 mr-2" />
            Обновить
          </Button>
        </div>
      </div>

      <Card title="Информация о проверке">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <p className="text-sm text-gray-500">Хост</p>
            <p className="text-lg font-medium text-gray-900">{check.target}</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Типы проверок</p>
            <p className="text-lg font-medium text-gray-900">
              {check.check_types.join(', ')}
            </p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Статус</p>
            <div className="mt-1">
              <StatusBadge status={check.status} />
            </div>
          </div>
        </div>
      </Card>

      {check.results && check.results.length > 0 ? (
        <>
          <Card title="Результаты по агентам">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {check.results.map((result) => (
                <ResultCard key={result.id} result={result} />
              ))}
            </div>
          </Card>

          <Card title="Детальная таблица">
            <ResultsTable results={check.results} />
          </Card>
        </>
      ) : (
        <Card>
          <div className="text-center py-12">
            <RefreshCw className="w-12 h-12 text-gray-400 mx-auto mb-4 animate-spin" />
            <p className="text-gray-500 text-lg">Выполняется проверка...</p>
            <p className="text-gray-400 text-sm mt-2">
              Результаты появятся через несколько секунд
            </p>
          </div>
        </Card>
      )}
    </div>
  );
};

