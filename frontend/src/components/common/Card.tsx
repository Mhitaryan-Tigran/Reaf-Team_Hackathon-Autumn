import { FC, ReactNode, memo } from 'react';
import clsx from 'clsx';

interface CardProps {
  children: ReactNode;
  className?: string;
  title?: string;
}

const CardComponent: FC<CardProps> = ({ children, className, title }) => {
  return (
    <div className={clsx('bg-white rounded-lg shadow-md p-6', className)}>
      {title && <h3 className="text-lg font-semibold mb-4">{title}</h3>}
      {children}
    </div>
  );
};

export const Card = memo(CardComponent);

