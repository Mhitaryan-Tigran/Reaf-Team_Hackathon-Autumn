import { FC, FormEvent, useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Input } from '../common/Input';
import { Button } from '../common/Button';
import { Card } from '../common/Card';
import { CheckTypeSelector } from './CheckTypeSelector';
import { createCheck } from '../../api/checks';
import { Search } from 'lucide-react';

interface CheckFormProps {
  onCheckCreated?: () => void;
}

export const CheckForm: FC<CheckFormProps> = ({ onCheckCreated }) => {
  const navigate = useNavigate();
  const [target, setTarget] = useState('');
  const [selectedTypes, setSelectedTypes] = useState<string[]>(['http', 'ping']);
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = useCallback(async (e: FormEvent) => {
    e.preventDefault();
    setError('');

    if (!target.trim()) {
      setError('Введите хост для проверки');
      return;
    }

    if (selectedTypes.length === 0) {
      setError('Выберите хотя бы один тип проверки');
      return;
    }

    setIsSubmitting(true);

    try {
      // Реальный API вызов
      const check = await createCheck({
        target: target.trim(),
        checks: selectedTypes,
      });
      
      // Callback для обновления списка проверок
      if (onCheckCreated) {
        onCheckCreated();
      }
      
      // Переход на страницу результатов
      navigate(`/results/${check.id}`);
    } catch (err: any) {
      console.error('Failed to create check:', err);
      setError(err.response?.data?.detail || 'Не удалось создать проверку. Проверьте, что есть онлайн агенты.');
      setIsSubmitting(false);
    }
  }, [target, selectedTypes, navigate, onCheckCreated]);

  const handleClear = useCallback(() => {
    setTarget('');
    setSelectedTypes(['http', 'ping']);
    setError('');
  }, []);

  return (
    <Card className="max-w-3xl mx-auto shadow-lg">
      <div className="flex items-center gap-3 mb-6">
        <div className="p-3 bg-blue-100 rounded-lg">
          <Search className="w-6 h-6 text-blue-600" />
        </div>
        <h2 className="text-2xl font-bold text-gray-900">Создать новую проверку</h2>
      </div>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        <Input
          label="Хост или IP-адрес"
          placeholder="example.com, 192.168.1.1 или example.com:8080"
          value={target}
          onChange={(e) => setTarget(e.target.value)}
          error={error && !target.trim() ? error : undefined}
        />

        <CheckTypeSelector
          selectedTypes={selectedTypes}
          onChange={setSelectedTypes}
        />

        {error && (
          <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-sm text-red-600">{error}</p>
          </div>
        )}

        <div className="flex justify-end space-x-3">
          <Button
            type="button"
            variant="secondary"
            onClick={handleClear}
            disabled={isSubmitting}
          >
            Очистить
          </Button>
          <Button type="submit" disabled={isSubmitting}>
            {isSubmitting ? 'Создание...' : 'Создать проверку'}
          </Button>
        </div>
      </form>
    </Card>
  );
};

