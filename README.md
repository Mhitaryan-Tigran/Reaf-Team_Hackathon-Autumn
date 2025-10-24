# Host Checker - Сервис проверки хостов и DNS

> Распределенный сервис для проверки доступности хостов с поддержкой агентов в разных локациях

[![React](https://img.shields.io/badge/React-18.2-blue.svg)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.2-blue.svg)](https://www.typescriptlang.org/)
[![Vite](https://img.shields.io/badge/Vite-5.0-purple.svg)](https://vitejs.dev)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.3-cyan.svg)](https://tailwindcss.com)

---

## 📋 Содержание

- [Быстрый старт](#-быстрый-старт)
- [О проекте](#-о-проекте)
- [Структура фронтенда](#-структура-фронтенда)
- [Компоненты](#-компоненты)
- [API и интеграция](#-api-и-интеграция)
- [Как подключить бекенд](#-как-подключить-бекенд)
- [Оптимизации](#-оптимизации)
- [Развертывание](#-развертывание)

---

## 🚀 Быстрый старт

### Запуск фронтенда (3 минуты)

```bash
# 1. Перейти в папку фронтенда
cd frontend

# 2. Установить зависимости
npm install

# 3. Запустить dev сервер
npm run dev
```

Откройте **http://localhost:3000** - фронтенд работает с моковыми данными!

### Основные команды

```bash
npm run dev      # Разработка (hot reload)
npm run build    # Сборка для продакшена
npm run preview  # Предпросмотр продакшен сборки
npm run lint     # Проверка кода
```

---

## 📖 О проекте

### Что это?

**Host Checker** - веб-приложение для проверки доступности и производительности хостов с использованием распределенных агентов в разных географических локациях.

### Основные возможности

#### ✅ Создание проверок
- Ввод домена или IP адреса
- Выбор типов проверок: HTTP/HTTPS, Ping, DNS, TCP Port, Traceroute
- Выбор агентов для выполнения проверок

#### ✅ Просмотр результатов
- Детальные результаты от каждого агента
- Визуализация успешности проверок
- Время выполнения и статистика
- Карточки и таблицы с данными

#### ✅ Мониторинг агентов
- Список всех агентов
- Статусы (онлайн/оффлайн)
- Информация о последнем heartbeat
- Статистика по локациям

### Технологический стек

**Frontend:**
- ⚛️ **React 18.2** - UI библиотека
- 📘 **TypeScript 5.2** - строгая типизация
- ⚡ **Vite 5.0** - быстрый dev сервер и сборка
- 🎨 **Tailwind CSS 3.3** - утилитарный CSS
- 🧭 **React Router 6.20** - маршрутизация
- 🔄 **Axios 1.6** - HTTP клиент
- 🎯 **Lucide React** - иконки

**Backend (TODO):**
- 🐍 FastAPI - API сервер
- 🗄️ PostgreSQL - база данных
- 🔴 Redis - очереди и кеширование
- 🐳 Docker - контейнеризация

---

## 📁 Структура фронтенда

### Общая структура

```
frontend/
├── src/
│   ├── components/       # React компоненты
│   │   ├── agents/      # Компоненты агентов
│   │   ├── check/       # Компоненты создания проверок
│   │   ├── common/      # Переиспользуемые компоненты
│   │   ├── layout/      # Компоненты макета
│   │   └── results/     # Компоненты результатов
│   │
│   ├── pages/           # Страницы приложения
│   │   ├── Dashboard.tsx    # Главная страница
│   │   ├── Results.tsx      # Страница результатов
│   │   └── Agents.tsx       # Страница агентов
│   │
│   ├── api/             # API клиенты
│   │   ├── client.ts        # Базовый Axios клиент
│   │   ├── checks.ts        # API для проверок
│   │   └── agents.ts        # API для агентов
│   │
│   ├── hooks/           # Custom React hooks
│   │   ├── usePolling.ts    # Автообновление данных
│   │   ├── useWebSocket.ts  # WebSocket соединения
│   │   └── useDebounce.ts   # Отложенное выполнение
│   │
│   ├── types/           # TypeScript типы
│   │   └── index.ts         # Интерфейсы и типы
│   │
│   ├── utils/           # Утилиты
│   │   ├── format.ts        # Форматирование данных
│   │   ├── constants.ts     # Константы
│   │   └── mockData.ts      # Моковые данные (временно)
│   │
│   ├── styles/          # Стили
│   │   └── globals.css      # Глобальные стили
│   │
│   ├── App.tsx          # Главный компонент
│   └── main.tsx         # Точка входа
│
├── public/              # Статические файлы
├── package.json         # Зависимости
├── vite.config.ts       # Конфигурация Vite
├── tsconfig.json        # Конфигурация TypeScript
└── tailwind.config.js   # Конфигурация Tailwind
```

### Детальная структура компонентов

#### 📦 components/common/ - Базовые компоненты

**Button.tsx** - Универсальная кнопка
```typescript
<Button variant="primary" size="md">Создать</Button>
<Button variant="secondary">Отмена</Button>
<Button variant="danger">Удалить</Button>
```

**Card.tsx** - Карточка контента
```typescript
<Card title="Заголовок">
  <p>Содержимое карточки</p>
</Card>
```

**Input.tsx** - Поле ввода с лейблом
```typescript
<Input 
  label="Хост" 
  value={value} 
  onChange={onChange}
  error={error}
/>
```

**StatusBadge.tsx** - Бейдж статуса
```typescript
<StatusBadge status="completed" type="check" />
<StatusBadge status="online" type="agent" />
```

**LoadingSpinner.tsx** - Индикатор загрузки
```typescript
<LoadingSpinner size="md" />
```

**ErrorBoundary.tsx** - Обработка ошибок React
```typescript
<ErrorBoundary>
  <App />
</ErrorBoundary>
```

#### 🏗️ components/layout/ - Макет

**Header.tsx** - Шапка с навигацией
- Логотип "Host Checker"
- Навигационное меню (Dashboard, Агенты)
- Активная страница подсвечивается

**Layout.tsx** - Общий макет страницы
- Оборачивает Header + контент
- Адаптивные отступы

#### ✅ components/check/ - Создание проверок

**CheckForm.tsx** - Форма создания проверки
- Поле ввода для хоста/домена
- Выбор типов проверок (CheckTypeSelector)
- Валидация
- Обработка отправки

**CheckTypeSelector.tsx** - Выбор типов проверок
- Чекбоксы для каждого типа (HTTP, Ping, DNS, TCP, Traceroute)
- Grid layout (2 колонки)
- Hover эффекты

#### 📊 components/results/ - Результаты

**ResultCard.tsx** - Карточка результата
- Иконка успеха/неудачи
- Тип проверки и локация агента
- Время выполнения
- Детали результата (статус код, latency, IP и т.д.)

**ResultsTable.tsx** - Таблица результатов
- Все результаты в виде таблицы
- Столбцы: Статус, Агент, Проверка, Время, Детали
- Адаптивная (горизонтальный скролл на мобильных)

#### 👥 components/agents/ - Агенты

**AgentCard.tsx** - Карточка агента
- Название и локация
- Статус (онлайн/оффлайн)
- Последний heartbeat
- Дата регистрации
- IP адрес (если доступен)

**AgentsList.tsx** - Список агентов
- Группировка на онлайн/оффлайн
- Grid layout (3 колонки на desktop)
- Адаптивный

---

## 🧩 Компоненты

### Страницы

#### Dashboard (/)
**Функции:**
- Форма создания новой проверки
- Список недавних проверок
- Клик на проверку → переход к результатам

**Используемые компоненты:**
- `CheckForm` - форма создания
- `Card` - обертка для списка
- `StatusBadge` - статусы проверок
- `Link` - навигация

#### Results (/results/:checkId)
**Функции:**
- Детальная информация о проверке
- Карточки результатов по агентам
- Таблица всех результатов
- Кнопка обновления

**Используемые компоненты:**
- `Card` - информационные блоки
- `StatusBadge` - статус проверки
- `ResultCard` - карточки результатов
- `ResultsTable` - таблица

**Особенность:** Использует URL параметр `checkId` для загрузки данных

#### Agents (/agents)
**Функции:**
- Статистика агентов (онлайн/всего/работоспособность)
- Список всех агентов
- Группировка по статусу

**Используемые компоненты:**
- `Card` - статистика
- `AgentsList` - список агентов
- `AgentCard` - карточка агента

### Типы данных (TypeScript)

```typescript
// Проверка
interface Check {
  id: string;
  target: string;
  check_types: string[];
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
  created_at: string;
  completed_at?: string;
  results?: CheckResult[];
}

// Результат проверки
interface CheckResult {
  id: string;
  check_id: string;
  agent_id: string;
  agent_name: string;
  agent_location: string;
  check_type: string;
  success: boolean;
  data: Record<string, any>;
  error?: string;
  duration_ms: number;
  created_at: string;
}

// Агент
interface Agent {
  id: string;
  name: string;
  location: string;
  status: 'online' | 'offline';
  last_heartbeat: string;
  registered_at: string;
  metadata?: Record<string, any>;
}

// Запрос на создание проверки
interface CreateCheckRequest {
  target: string;
  checks: string[];
  agents?: string[];
}
```

---

## 🔌 API и интеграция

### API клиенты (готовы к использованию!)

#### client.ts - Базовый клиент

```typescript
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: `${API_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});
```

#### checks.ts - API для проверок

```typescript
// Создать проверку
export const createCheck = async (data: CreateCheckRequest): Promise<Check> => {
  const response = await apiClient.post<Check>('/checks', data);
  return response.data;
};

// Получить проверку
export const getCheck = async (checkId: string): Promise<Check> => {
  const response = await apiClient.get<Check>(`/checks/${checkId}`);
  return response.data;
};

// Список проверок
export const listChecks = async (): Promise<Check[]> => {
  const response = await apiClient.get<Check[]>('/checks');
  return response.data;
};

// Удалить проверку
export const deleteCheck = async (checkId: string): Promise<void> => {
  await apiClient.delete(`/checks/${checkId}`);
};
```

#### agents.ts - API для агентов

```typescript
// Список агентов
export const listAgents = async (): Promise<Agent[]> => {
  const response = await apiClient.get<Agent[]>('/agents');
  return response.data;
};

// Получить агента
export const getAgent = async (agentId: string): Promise<Agent> => {
  const response = await apiClient.get<Agent>(`/agents/${agentId}`);
  return response.data;
};

// Регистрация агента
export const registerAgent = async (data: {
  name: string;
  location: string;
}): Promise<{ agent_id: string; api_token: string }> => {
  const response = await apiClient.post('/agents/register', data);
  return response.data;
};
```

### Custom Hooks

#### usePolling - Автообновление данных

```typescript
// Автоматически опрашивает API каждые N секунд
const { data, error, isLoading } = usePolling(
  () => getCheck(checkId),
  2000,  // интервал 2 секунды
  check?.status !== 'completed'  // только пока не завершено
);
```

**Использование:**
- Автообновление результатов проверки
- Мониторинг статуса агентов
- Любые данные, которые часто меняются

#### useWebSocket - Real-time обновления

```typescript
const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000';

const { data, isConnected, error } = useWebSocket(
  `${WS_URL}/api/ws/checks/${checkId}`,
  check?.status === 'in_progress'
);
```

**Использование:**
- Real-time обновления результатов
- Уведомления о завершении проверок
- Live статусы агентов

#### useDebounce - Отложенное выполнение

```typescript
const debouncedSearchTerm = useDebounce(searchTerm, 500);

useEffect(() => {
  // Выполнится только после того, как пользователь перестанет печатать
  searchAPI(debouncedSearchTerm);
}, [debouncedSearchTerm]);
```

**Использование:**
- Поиск с задержкой
- Валидация при вводе
- Оптимизация API запросов

---

## 🔗 Как подключить бекенд

### Шаг 1: Создайте .env файл

```bash
cd frontend
cat > .env << EOF
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
EOF
```

### Шаг 2: Запустите бекенд

```bash
# В отдельном терминале
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Шаг 3: Замените моки на реальные API

Нужно изменить только **3 файла**:

#### 1. src/pages/Dashboard.tsx

**Было:**
```typescript
import { mockChecks } from '../utils/mockData';

export const Dashboard = () => {
  const checks = mockChecks;
  
  return (
    <div>
      {checks.map(check => ...)}
    </div>
  );
};
```

**Стало:**
```typescript
import { useEffect, useState } from 'react';
import { listChecks } from '../api/checks';

export const Dashboard = () => {
  const [checks, setChecks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    listChecks()
      .then(setChecks)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <LoadingSpinner />;

  return (
    <div>
      {checks.map(check => ...)}
    </div>
  );
};
```

#### 2. src/pages/Results.tsx

**Было:**
```typescript
import { mockCheck } from '../utils/mockData';

export const Results = () => {
  const { checkId } = useParams();
  const check = mockCheck;
  
  return <div>...</div>;
};
```

**Стало (с автообновлением):**
```typescript
import { useParams } from 'react-router-dom';
import { usePolling } from '../hooks/usePolling';
import { getCheck } from '../api/checks';

export const Results = () => {
  const { checkId } = useParams<{ checkId: string }>();
  
  // Автоматически обновляется каждые 2 секунды
  const { data: check, isLoading, error } = usePolling(
    () => getCheck(checkId!),
    2000,
    true  // можно сделать проверку: check?.status !== 'completed'
  );

  if (isLoading) return <LoadingSpinner />;
  if (error) return <div>Ошибка загрузки</div>;
  if (!check) return <div>Проверка не найдена</div>;

  return <div>...</div>;
};
```

#### 3. src/pages/Agents.tsx

**Было:**
```typescript
import { mockAgents } from '../utils/mockData';

export const Agents = () => {
  const onlineCount = mockAgents.filter(a => a.status === 'online').length;
  const totalCount = mockAgents.length;

  return (
    <div>
      <AgentsList agents={mockAgents} />
    </div>
  );
};
```

**Стало:**
```typescript
import { useEffect, useState } from 'react';
import { listAgents } from '../api/agents';

export const Agents = () => {
  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAgents = async () => {
      try {
        const data = await listAgents();
        setAgents(data);
      } catch (error) {
        console.error('Failed to fetch agents:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchAgents();
    // Опционально: обновлять каждые 5 секунд
    const interval = setInterval(fetchAgents, 5000);
    return () => clearInterval(interval);
  }, []);

  if (loading) return <LoadingSpinner />;

  const onlineCount = agents.filter(a => a.status === 'online').length;
  const totalCount = agents.length;

  return (
    <div>
      <AgentsList agents={agents} />
    </div>
  );
};
```

### Шаг 4: Обновите CheckForm для создания проверок

**Было:**
```typescript
const handleSubmit = async (e: FormEvent) => {
  e.preventDefault();
  // Имитация
  setTimeout(() => {
    const mockCheckId = Math.random().toString(36).substring(7);
    navigate(`/results/${mockCheckId}`);
  }, 500);
};
```

**Стало:**
```typescript
import { createCheck } from '../api/checks';

const handleSubmit = async (e: FormEvent) => {
  e.preventDefault();
  setError('');
  setIsSubmitting(true);

  try {
    const check = await createCheck({
      target: target.trim(),
      checks: selectedTypes,
      agents: ['all'], // или конкретные ID агентов
    });
    
    navigate(`/results/${check.id}`);
  } catch (err) {
    setError('Не удалось создать проверку. Попробуйте снова.');
    console.error('Failed to create check:', err);
  } finally {
    setIsSubmitting(false);
  }
};
```

### Шаг 5: Настройте CORS на бекенде

```python
# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # фронтенд
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Шаг 6: Протестируйте

1. Запустите бекенд: `uvicorn app.main:app --reload`
2. Запустите фронтенд: `npm run dev`
3. Откройте http://localhost:3000
4. Создайте проверку
5. Убедитесь, что данные приходят с бекенда

### Опционально: WebSocket для real-time

```typescript
// В Results.tsx добавьте WebSocket
import { useWebSocket } from '../hooks/useWebSocket';

const { data: liveUpdate, isConnected } = useWebSocket(
  `ws://localhost:8000/api/ws/checks/${checkId}`,
  check?.status === 'in_progress'
);

// При получении обновления
useEffect(() => {
  if (liveUpdate) {
    // Обновить локальное состояние
    setCheck(prevCheck => ({
      ...prevCheck,
      ...liveUpdate
    }));
  }
}, [liveUpdate]);
```

---

## ⚡ Оптимизации

### React оптимизации

**React.memo** - Предотвращает лишние рендеры
```typescript
export const Button = memo(ButtonComponent);
export const Card = memo(CardComponent);
export const ResultCard = memo(ResultCardComponent);
```

**useCallback** - Кеширование функций
```typescript
const handleSubmit = useCallback(async (e) => {
  // ...
}, [dependencies]);
```

**useMemo** - Кеширование вычислений
```typescript
const checkTypeEntries = useMemo(() => 
  Object.entries(CHECK_TYPES), 
[]); 
```

### Производительность

**Ленивая загрузка компонентов:**
```typescript
const Results = lazy(() => import('./pages/Results'));
const Agents = lazy(() => import('./pages/Agents'));
```

**Виртуализация списков (для больших данных):**
```bash
npm install react-window
```

### Bundle size

**Текущий размер:** ~240KB (gzipped: ~80KB)

**Оптимизации:**
- Tree-shaking работает автоматически
- Code splitting готов к использованию
- Tailwind CSS purge включен

---

## 🚀 Развертывание

### Локальная сборка

```bash
npm run build
npm run preview  # проверить сборку
```

### Vercel (рекомендуется)

```bash
# Установить Vercel CLI
npm i -g vercel

# Деплой
cd frontend
vercel
```

**Автоматический деплой:**
1. Push в GitHub
2. Подключите репозиторий к Vercel
3. Vercel автоматически деплоит при каждом push

**Настройка переменных окружения в Vercel:**
```
VITE_API_URL=https://your-api.com
VITE_WS_URL=wss://your-api.com
```

### Netlify

```bash
# Создайте netlify.toml
cat > netlify.toml << EOF
[build]
  command = "npm run build"
  publish = "dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
EOF

# Деплой
npm install -g netlify-cli
netlify deploy --prod
```

### Docker

```dockerfile
# Dockerfile для фронтенда
FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

```nginx
# nginx.conf
server {
    listen 80;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# Собрать и запустить
docker build -t host-checker-frontend .
docker run -p 3000:80 host-checker-frontend
```

### Docker Compose (полный стек)

```yaml
version: '3.8'

services:
  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    environment:
      - VITE_API_URL=http://localhost:8000
    depends_on:
      - backend

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/hostchecker
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=hostchecker
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

  agent:
    build: ./agent
    environment:
      - API_URL=http://backend:8000
      - AGENT_NAME=Local-Agent-1
      - AGENT_LOCATION=Local
    depends_on:
      - backend

volumes:
  postgres_data:
  redis_data:
```

---

## 📚 Дополнительная документация

### Полная документация в папке docs/

- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Архитектура всей системы
- **[docs/IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md)** - План реализации бекенда
- **[docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)** - Структура и шаблоны кода
- **[docs/STACK_SUMMARY.md](docs/STACK_SUMMARY.md)** - Обоснование выбора технологий

### API Endpoints (для бекенда)

**Checks:**
- `POST /api/checks` - создать проверку
- `GET /api/checks` - список проверок
- `GET /api/checks/{id}` - получить проверку
- `DELETE /api/checks/{id}` - удалить проверку

**Agents:**
- `GET /api/agents` - список агентов
- `POST /api/agents/register` - зарегистрировать агента
- `POST /api/agents/heartbeat` - heartbeat агента
- `GET /api/agents/{id}` - получить агента

**WebSocket:**
- `WS /api/ws/checks/{id}` - real-time обновления

---

## 🤝 Команда

- Никита
- Артем
- Андрей
- Тигран
- Алексей

---

## 📄 Лицензия

MIT License - можно использовать как угодно

---

## 🎯 Roadmap

### ✅ Фаза 1: MVP (готово)
- [x] Фронтенд на React + TypeScript
- [x] Все компоненты и страницы
- [x] API клиенты готовы
- [x] Моковые данные для демонстрации

### 🔄 Фаза 2: Бекенд (в процессе)
- [ ] FastAPI сервер
- [ ] PostgreSQL + модели
- [ ] Redis + очереди
- [ ] API endpoints
- [ ] WebSocket

### ⏳ Фаза 3: Агенты
- [ ] Python агент
- [ ] Проверки (HTTP, Ping, DNS, TCP)
- [ ] Heartbeat система
- [ ] Обработка задач из очереди

### 🚀 Фаза 4: Интеграция и деплой
- [ ] Интеграция фронт + бэк
- [ ] Docker Compose
- [ ] CI/CD
- [ ] Продакшен деплой

---

**Фронтенд готов! Осталось только подключить бекенд! 🚀**

Вопросы? Проблемы? Создайте issue или напишите команде!
