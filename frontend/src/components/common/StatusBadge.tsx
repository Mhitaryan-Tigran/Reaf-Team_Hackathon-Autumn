import { FC, memo } from 'react';
import clsx from 'clsx';
import { CHECK_STATUS_COLORS, AGENT_STATUS_COLORS } from '../../types';

interface StatusBadgeProps {
  status: keyof typeof CHECK_STATUS_COLORS | keyof typeof AGENT_STATUS_COLORS;
  type?: 'check' | 'agent';
}

const StatusBadgeComponent: FC<StatusBadgeProps> = ({ status, type = 'check' }) => {
  const colors = type === 'check' ? CHECK_STATUS_COLORS : AGENT_STATUS_COLORS;
  const colorClass = colors[status as keyof typeof colors];

  const labels: Record<string, string> = {
    pending: 'Ожидание',
    in_progress: 'Выполняется',
    completed: 'Завершено',
    failed: 'Ошибка',
    online: 'Онлайн',
    offline: 'Оффлайн',
  };

  return (
    <span
      className={clsx(
        'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
        colorClass
      )}
    >
      {labels[status]}
    </span>
  );
};

export const StatusBadge = memo(StatusBadgeComponent);

