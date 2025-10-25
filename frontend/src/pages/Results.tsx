import { FC, useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Card } from '../components/common/Card';
import { StatusBadge } from '../components/common/StatusBadge';
import { ResultsTable } from '../components/results/ResultsTable';
import { ResultCard } from '../components/results/ResultCard';
import { getCheck } from '../api/checks';
import { Check } from '../types';
import { formatDate } from '../utils/format';
import { ArrowLeft, RefreshCw } from 'lucide-react';
import { Button } from '../components/common/Button';

export const Results: FC = () => {
  const { checkId } = useParams<{ checkId: string }>();
  const [check, setCheck] = useState<Check | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string>('');

  const fetchCheck = async () => {
    if (!checkId) return;
    
    setIsLoading(true);
    try {
      const data = await getCheck(checkId);
      setCheck(data);
      setError('');
    } catch (err) {
      console.error('Failed to fetch check:', err);
      setError('Не удалось загрузить результаты проверки');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchCheck();
    
    // Polling для обновления результатов
    const interval = setInterval(() => {
      if (check?.status !== 'completed' && check?.status !== 'failed') {
        fetchCheck();
      }
    }, 3000);

    return () => clearInterval(interval);
  }, [checkId]);

  if (isLoading && !check) {
    return (
      <div className="flex justify-center items-center min-h-[400px]">
        <RefreshCw className="w-8 h-8 text-gray-400 animate-spin" />
      </div>
    );
  }

  if (error || !check) {
    return (
      <Card>
        <div className="text-center py-12">
          <p className="text-red-500 text-lg">{error || 'Проверка не найдена'}</p>
          <Link to="/" className="text-blue-600 hover:underline mt-4 inline-block">
            Вернуться на главную
          </Link>
        </div>
      </Card>
    );
  }

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

