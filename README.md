# ML Sentiment Analysis with Database Integration

Интеграция ML модели анализа тональности с MS SQL Server и повторное использование CI/CD пайплайнов.

## 🎯 Цель проекта

Демонстрация навыков интеграции ML сервиса с базой данных, обеспечения безопасности и автоматизации развертывания.

## 🏗️ Архитектура

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Flask API     │    │   MS SQL Server │    │   CI/CD         │
│                 │    │                 │    │                 │
│ • Predictions   │◄──►│ • Predictions   │    │ • GitHub Actions│
│ • Authentication│    │ • Training Data │    │ • Docker Build  │
│ • Health Checks │    │ • Model Metrics │    │ • Auto Deploy   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Быстрый старт

### Предварительные требования

- Docker и Docker Compose
- Python 3.11+ (для локальной разработки)
- Git

### Запуск с Docker Compose

```bash
# Клонирование репозитория
git clone https://github.com/osadcijm84/ml-sentiment-db-integration.git
cd ml-sentiment-db-integration

# Создание файла окружения
cp .env.example .env

# Запуск сервисов
docker-compose up -d

# Проверка состояния
curl http://localhost:5000/api/health
```

### Локальная разработка

```bash
# Установка зависимостей
pip install -r requirements.txt

# Настройка переменных окружения
export DB_HOST=localhost
export DB_PORT=1433
export DB_NAME=SentimentDB
export DB_USER=sa
export DB_PASSWORD=StrongPassword123!

# Запуск приложения
python ml_sentiment_api/app_with_db.py
```

## 📊 База данных

### Структура таблиц

**SentimentPredictions** - хранение результатов предсказаний
```sql
CREATE TABLE SentimentPredictions (
    id INT IDENTITY(1,1) PRIMARY KEY,
    text NVARCHAR(MAX) NOT NULL,
    sentiment NVARCHAR(50) NOT NULL,
    confidence FLOAT NOT NULL,
    prediction_date DATETIME2 DEFAULT GETDATE(),
    model_version NVARCHAR(50) DEFAULT '1.0',
    created_at DATETIME2 DEFAULT GETDATE()
);
```

**TrainingData** - данные для обучения и валидации
```sql
CREATE TABLE TrainingData (
    id INT IDENTITY(1,1) PRIMARY KEY,
    text NVARCHAR(MAX) NOT NULL,
    actual_sentiment NVARCHAR(50) NOT NULL,
    rating FLOAT,
    product_category NVARCHAR(100),
    data_source NVARCHAR(100) DEFAULT 'Amazon Reviews',
    created_at DATETIME2 DEFAULT GETDATE(),
    is_training BIT DEFAULT 1,
    is_validation BIT DEFAULT 0
);
```

**ModelMetrics** - метрики производительности модели
```sql
CREATE TABLE ModelMetrics (
    id INT IDENTITY(1,1) PRIMARY KEY,
    model_version NVARCHAR(50) NOT NULL,
    accuracy FLOAT,
    precision_score FLOAT,
    recall_score FLOAT,
    f1_score FLOAT,
    training_date DATETIME2 DEFAULT GETDATE(),
    notes NVARCHAR(MAX)
);
```

## 🔐 Аутентификация

### API ключи

Для доступа к защищенным эндпоинтам используйте заголовок:
```
X-API-Key: YOUR_API_KEY
```

### JWT токены

Получение токена:
```bash
curl -X POST http://localhost:5000/api/auth/token \
  -H "Content-Type: application/json" \
  -d '{"api_key": "YOUR_API_KEY"}'
```

Использование токена:
```
Authorization: Bearer YOUR_JWT_TOKEN
```

## 📡 API Endpoints

### Публичные эндпоинты

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/api/health` | Проверка состояния сервиса |
| POST | `/api/predict` | Предсказание тональности |
| POST | `/api/auth/token` | Получение JWT токена |

### Защищенные эндпоинты (требуют API ключ)

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/api/predictions` | История предсказаний |
| GET | `/api/stats` | Статистика и метрики |
| POST | `/api/training-data` | Добавление данных обучения |
| GET | `/api/training-data` | Получение данных обучения |

### Примеры использования

**Предсказание тональности:**
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "This product is amazing!"}'
```

**Получение статистики:**
```bash
curl http://localhost:5000/api/stats \
  -H "X-API-Key: YOUR_API_KEY"
```

**Добавление данных обучения:**
```bash
curl -X POST http://localhost:5000/api/training-data \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '[{
    "text": "Great product!",
    "actual_sentiment": "positive",
    "rating": 5.0,
    "product_category": "Beauty"
  }]'
```

## 🔄 CI/CD Pipeline

### Continuous Integration (CI)

Автоматически запускается при:
- Push в ветки `main` или `develop`
- Pull request в ветку `main`

Этапы:
1. ✅ Запуск тестов с MS SQL Server
2. ✅ Проверка покрытия кода
3. ✅ Сборка Docker образа
4. ✅ Публикация на DockerHub

### Continuous Deployment (CD)

Автоматически запускается:
- После успешного CI
- По требованию (manual trigger)
- По расписанию (ежедневно в 2:00 UTC)

Этапы:
1. ✅ Развертывание с Docker Compose
2. ✅ Функциональное тестирование
3. ✅ Нагрузочное тестирование
4. ✅ Сбор логов и метрик

## 🧪 Тестирование

### Запуск тестов локально

```bash
# Unit тесты
python -m pytest test_model.py -v

# API тесты
python -m pytest test_api.py -v

# Тесты с покрытием
python -m pytest --cov=. --cov-report=html
```

### Функциональные тесты

```bash
# Проверка здоровья сервиса
curl http://localhost:5000/api/health

# Тест предсказания
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Test message"}'
```

## 🐳 Docker

### Сборка образа

```bash
docker build -t ml-sentiment-db-integration .
```

### Запуск контейнера

```bash
docker run -p 5000:5000 \
  -e DB_HOST=host.docker.internal \
  -e DB_PASSWORD=StrongPassword123! \
  ml-sentiment-db-integration
```

## 📈 Мониторинг

### Health Checks

Сервис предоставляет детальную информацию о состоянии:
- Статус загрузки модели
- Подключение к базе данных
- Версия приложения
- Временные метки

### Логирование

Структурированные логи включают:
- Уровень логирования (INFO, WARNING, ERROR)
- Временные метки
- Информацию о клиентах
- Детали ошибок

### Метрики

Автоматический сбор метрик:
- Количество предсказаний
- Распределение тональности
- Средняя уверенность модели
- Производительность модели

## 🔧 Конфигурация

### Переменные окружения

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `DB_HOST` | Хост базы данных | `localhost` |
| `DB_PORT` | Порт базы данных | `1433` |
| `DB_NAME` | Имя базы данных | `SentimentDB` |
| `DB_USER` | Пользователь БД | `sa` |
| `DB_PASSWORD` | Пароль БД | - |
| `SECRET_KEY` | Секретный ключ Flask | auto-generated |
| `API_KEY_1` | Первый API ключ | auto-generated |
| `API_KEY_2` | Второй API ключ | auto-generated |

### Файлы конфигурации

- `.env` - переменные окружения (не в репозитории)
- `.env.example` - пример конфигурации
- `config.ini` - гиперпараметры модели
- `docker-compose.yml` - конфигурация сервисов

## 🚀 Развертывание

### Staging окружение

```bash
# Автоматическое развертывание через GitHub Actions
# или ручной запуск:
docker-compose -f docker-compose.yml up -d
```

### Production окружение

```bash
# Использование production конфигурации
docker-compose -f docker-compose.prod.yml up -d
```

## 📚 Документация

- [Отчет по лабораторной работе](ОТЧЕТ_ЛР2.md)
- [API документация](docs/api.md)
- [Руководство по развертыванию](docs/deployment.md)

## 🤝 Участие в разработке

1. Fork репозитория
2. Создайте feature ветку (`git checkout -b feature/amazing-feature`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в ветку (`git push origin feature/amazing-feature`)
5. Создайте Pull Request

## 📄 Лицензия

Этот проект создан в образовательных целях.

## 📞 Контакты

- **Автор:** Maxim
- **GitHub:** https://github.com/osadcijm84/ml-sentiment-db-integration
- **Docker Hub:** https://hub.docker.com/r/osadcijm84/ml-sentiment-db-integration

---

## 🏆 Достижения

- ✅ Интеграция с MS SQL Server
- ✅ Система аутентификации и авторизации
- ✅ CI/CD пайплайны с автоматическим тестированием
- ✅ Docker контейнеризация
- ✅ Функциональное и нагрузочное тестирование
- ✅ Мониторинг и логирование
- ✅ Безопасное управление конфигурацией

**Версия:** 2.0  
**Последнее обновление:** 11 августа 2025

