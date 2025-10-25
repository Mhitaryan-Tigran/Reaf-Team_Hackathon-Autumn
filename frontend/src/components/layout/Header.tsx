import { FC } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Globe, Home, Server } from 'lucide-react';
import clsx from 'clsx';

export const Header: FC = () => {
  const location = useLocation();

  const navItems = [
    { path: '/', label: 'Главная', icon: Home },
    { path: '/agents', label: 'Агенты', icon: Server },
  ];

  return (
    <header className="bg-gradient-to-r from-blue-600 to-purple-600 shadow-lg sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="flex items-center space-x-3 hover:opacity-90 transition-opacity">
            <div className="p-2 bg-white rounded-lg">
              <Globe className="h-6 w-6 text-blue-600" />
            </div>
            <span className="text-xl font-bold text-white">Host Checker</span>
          </Link>
          
          <nav className="flex space-x-2">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;
              
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={clsx(
                    'flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all',
                    isActive
                      ? 'bg-white text-blue-600 shadow-lg'
                      : 'text-white hover:bg-white/20'
                  )}
                >
                  <Icon className="w-4 h-4" />
                  {item.label}
                </Link>
              );
            })}
          </nav>
        </div>
      </div>
    </header>
  );
};

