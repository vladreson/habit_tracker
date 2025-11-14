# Habit Tracker 🚀

Django REST API для трекера полезных привычек по методологии Джеймса Клира "Атомные привычки".

## 📋 Функциональность

- ✅ Создание и управление привычками
- ✅ Валидация привычек по правилам из книги
- ✅ Telegram напоминания о привычках
- ✅ JWT аутентификация
- ✅ Публичные привычки
- ✅ Пагинация и фильтрация
- ✅ Документация API (Swagger/ReDoc)

## 🛠 Технологии

- **Backend**: Django 4.2, Django REST Framework
- **Database**: SQLite3 (разработка), PostgreSQL (продакшен)
- **Task Queue**: Celery + Redis
- **Notifications**: Telegram Bot API
- **Documentation**: Swagger/ReDoc
- **Testing**: Django Test Framework, Coverage 90%+

## 🚀 Быстрый старт

### 1. Клонирование репозитория
```bash
git clone https://github.com/yourusername/habit_tracker.git
cd habit_tracker
```

2. Настройка окружения
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```
3. Настройка переменных окружения
Создайте файл .env:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
REDIS_URL=redis://localhost:6379/0
```
4. Миграции и суперпользователь
```bash
python manage.py migrate
python manage.py createsuperuser
```
5. Запуск
```bash
# Сервер разработки
python manage.py runserver

# Celery worker (в отдельном терминале)
celery -A config worker --loglevel=info

# Celery beat (в отдельном терминале)
celery -A config beat --loglevel=info
```
📚 API Endpoints
Аутентификация
POST /api/auth/register/ - Регистрация

POST /api/auth/token/ - Получение JWT токена

GET /api/auth/profile/ - Профиль пользователя

Привычки
GET/POST /api/habits/ - Список и создание привычек

GET/PUT/DELETE /api/habits/{id}/ - Управление привычкой

GET /api/habits/public/ - Публичные привычки

Telegram
POST /api/telegram/connect/ - Подключение Telegram

GET/DELETE /api/telegram/me/ - Управление подключением

Документация
GET /swagger/ - Swagger UI

GET /redoc/ - ReDoc

🧪 Тестирование
```bash
# Запуск тестов
python manage.py test

# С покрытием кода
coverage run --source='.' manage.py test
coverage report

# Проверка стиля кода
flake8 .
```
📋 Правила привычек
⏱ Время выполнения ≤ 120 секунд

🎯 Нельзя одновременно связанную привычку и вознаграждение

😊 Приятные привычки не могут иметь вознаграждения

🔗 Связанные привычки должны быть приятными

🌐 Публичные привычки видны всем пользователям