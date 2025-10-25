import { FC, FormEvent, useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Input } from '../common/Input';
import { Button } from '../common/Button';
import { Card } from '../common/Card';
import { CheckTypeSelector } from './CheckTypeSelector';
import { createCheck } from '../../api/checks';

export const CheckForm: FC = () => {
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
      navigate(`/results/${check.id}`);
    } catch (err) {
      console.error('Failed to create check:', err);
      setError('Не удалось создать проверку. Попробуйте снова.');
      setIsSubmitting(false);
    }
  }, [target, selectedTypes, navigate]);

  const handleClear = useCallback(() => {
    setTarget('');
    setSelectedTypes(['http', 'ping']);
    setError('');
  }, []);

  return (
    <Card className="max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold mb-6">Создать новую проверку</h2>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        <Input
          label="Хост или IP-адрес"
          placeholder="example.com или 192.168.1.1"
          value={target}
          onChange={(e) => setTarget(e.target.value)}
          error={error && !target.trim() ? error : undefined}
        />

        <CheckTypeSelector
          selectedTypes={selectedTypes}
          onChange={setSelectedTypes}
        />

        {error && selectedTypes.length === 0 && (
          <p className="text-sm text-red-600">{error}</p>
        )}

        <div className="flex justify-end space-x-3">
          <Button
            type="button"
            variant="secondary"
            onClick={handleClear}
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

