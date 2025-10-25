import { FC, useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Card } from '../components/common/Card';
import { StatusBadge } from '../components/common/StatusBadge';
import { ResultsTable } from '../components/results/ResultsTable';
import { ResultCard } from '../components/results/ResultCard';
import { getCheck } from '../api/checks';
import { Check, CheckResult } from '../types';
import { formatDate } from '../utils/format';
import { ArrowLeft, RefreshCw, Globe, CheckCircle, XCircle, Clock, AlertCircle } from 'lucide-react';
import { Button } from '../components/common/Button';

export const Results: FC = () => {
  const { checkId } = useParams<{ checkId: string }>();
  const [check, setCheck] = useState<Check | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string>('');

  const fetchCheck = async () => {
    if (!checkId) return;
    
    try {
      const data = await getCheck(checkId);
      setCheck(data);
      setError('');
    } catch (err: any) {
      console.error('Failed to fetch check:', err);
      setError(err.message || 'Не удалось загрузить результаты проверки');
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
  }, [checkId, check?.status]);

  if (isLoading && !check) {
    return (
      <div className="flex justify-center items-center min-h-[400px]">
        <div className="text-center">
          <RefreshCw className="w-12 h-12 text-blue-600 animate-spin mx-auto mb-4" />
          <p className="text-gray-500">Загрузка результатов...</p>
        </div>
      </div>
    );
  }

  if (error || !check) {
    return (
      <Card className="border-red-200 bg-red-50">
        <div className="text-center py-12">
          <AlertCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
          <p className="text-red-600 text-lg font-medium mb-2">
            {error || 'Проверка не найдена'}
          </p>
          <Link to="/" className="text-blue-600 hover:underline mt-4 inline-block">
            Вернуться на главную
          </Link>
        </div>
      </Card>
    );
  }

  const successCount = check.results?.filter(r => r.success).length || 0;
  const failCount = (check.results?.length || 0) - successCount;
  const avgDuration = check.results?.length 
    ? Math.round(check.results.reduce((sum, r) => sum + r.duration_ms, 0) / check.results.length)
    : 0;

  // Группировка результатов по типам проверок
  const resultsByType = check.results?.reduce((acc, result) => {
    if (!acc[result.check_type]) {
      acc[result.check_type] = [];
    }
    acc[result.check_type].push(result);
    return acc;
  }, {} as Record<string, CheckResult[]>) || {};

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between flex-wrap gap-4">
        <div className="flex items-center space-x-4">
          <Link
            to="/"
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
          </Link>
          <div>
            <div className="flex items-center gap-3">
              <Globe className="w-8 h-8 text-blue-600" />
              <h1 className="text-3xl font-bold text-gray-900">{check.target}</h1>
            </div>
            <p className="text-gray-600 mt-1">Создано: {formatDate(check.created_at)}</p>
          </div>
        </div>
        <div className="flex items-center space-x-3">
          <StatusBadge status={check.status} />
          <Button variant="secondary" size="sm" onClick={fetchCheck}>
            <RefreshCw className="w-4 h-4 mr-2" />
            Обновить
          </Button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="bg-gradient-to-br from-blue-50 to-blue-100 border-blue-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-blue-600 mb-1">Типов проверок</p>
              <p className="text-2xl font-bold text-blue-900">{check.check_types.length}</p>
            </div>
            <Globe className="w-8 h-8 text-blue-600" />
          </div>
        </Card>

        <Card className="bg-gradient-to-br from-green-50 to-green-100 border-green-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-green-600 mb-1">Успешно</p>
              <p className="text-2xl font-bold text-green-900">{successCount}</p>
            </div>
            <CheckCircle className="w-8 h-8 text-green-600" />
          </div>
        </Card>

        <Card className="bg-gradient-to-br from-red-50 to-red-100 border-red-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-red-600 mb-1">Ошибок</p>
              <p className="text-2xl font-bold text-red-900">{failCount}</p>
            </div>
            <XCircle className="w-8 h-8 text-red-600" />
          </div>
        </Card>

        <Card className="bg-gradient-to-br from-purple-50 to-purple-100 border-purple-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-purple-600 mb-1">Ср. время</p>
              <p className="text-2xl font-bold text-purple-900">{avgDuration}ms</p>
            </div>
            <Clock className="w-8 h-8 text-purple-600" />
          </div>
        </Card>
      </div>

      {/* Results by Type */}
      {check.results && check.results.length > 0 ? (
        <>
          {Object.entries(resultsByType).map(([type, results]) => (
            <Card key={type}>
              <h2 className="text-xl font-bold text-gray-900 mb-4 capitalize">
                {type} проверки
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {results.map((result) => (
                  <ResultCard key={result.id} result={result} />
                ))}
              </div>
            </Card>
          ))}

          <Card>
            <h2 className="text-xl font-bold text-gray-900 mb-4">Детальная таблица</h2>
            <ResultsTable results={check.results} />
          </Card>
        </>
      ) : (
        <Card>
          <div className="text-center py-12">
            <RefreshCw className="w-16 h-16 text-blue-600 mx-auto mb-4 animate-spin" />
            <p className="text-gray-700 text-lg font-medium mb-2">Выполняется проверка...</p>
            <p className="text-gray-500 text-sm">
              Результаты появятся через несколько секунд
            </p>
            <div className="mt-6">
              <p className="text-xs text-gray-400">
                Проверяем: {check.check_types.join(', ')}
              </p>
            </div>
          </div>
        </Card>
      )}
    </div>
  );
};

