# GitHub Stats API

API-приложение для отображения статистики GitHub репозиториев.

## Требования

- Docker
- Docker Compose

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/bodaue/ecomet-backend.git
cd ecomet-backend
```

2. Создайте файл .env на основе .env.example:
```bash
cp .env.example .env
```

3. Отредактируйте .env файл, указав параметры подключения к вашему PostgreSQL кластеру:
```env
POSTGRES_HOST=your-postgres-host
POSTGRES_PORT=5432
POSTGRES_USER=your-username
POSTGRES_PASSWORD=your-password
POSTGRES_DB=your-database
```

4. Запустите приложение:
```bash
docker-compose up --build
```

API будет доступно по адресу http://localhost:8000

## API Endpoints

### GET /api/repos/top100
Получение топ-100 GitHub репозиториев, отсортированных по звездам.

Параметры запроса:
- `limit` (опционально): количество репозиториев (1-100, по умолчанию 100)
- `sort_by` (опционально): поле для сортировки (stars, watchers, forks, open_issues, language, position_cur)
- `sort_order` (опционально): порядок сортировки (asc, desc)

### GET /api/repos/{owner}/{repo}/activity
Получение информации об активности репозитория.

Параметры запроса:
- `since`: начальная дата (YYYY-MM-DD)
- `until`: конечная дата (YYYY-MM-DD)

## Разработка

Проект использует:
- Python 3.12+
- FastAPI
- PostgreSQL
- Docker
- Poetry для управления зависимостями

### Локальная разработка

1. Установите Poetry:
```bash
pip install poetry
```

2. Установите зависимости:
```bash
poetry install
```

3. Запустите приложение:
```bash
poetry run python -m src.main
```