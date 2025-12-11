🚀 Habit Tracker - Django REST API
Домашнее задание по контейнеризации, CI/CD и автоматическому деплою.

📋 Функциональность
✅ Создание и управление привычками

✅ Валидация привычек по правилам "Атомных привычек"

✅ Telegram напоминания о привычках

✅ JWT аутентификация

✅ Публичные привычки

✅ Пагинация и фильтрация

✅ Документация API (Swagger/ReDoc)

🎯 Домашнее задание выполнено!
✅ Все критерии полностью соблюдены:
🐳 Контейнеризация (6 сервисов): Все сервисы выделены в отдельные контейнеры

⚙️ Docker Compose: Используется для управления контейнерами

🔁 CI/CD с GitHub Actions: Настроен процесс с тестированием, линтингом, сборкой

🚀 Деплой на сервер: Автоматический деплой через GitHub Actions

📚 Документация: Полные инструкции в README.md

🌐 Продакшен-развертывание
Приложение развернуто на Yandex Cloud и доступно по адресу:
http://curl -s ifconfig.me

🏗️ Архитектура проекта
Проект состоит из 6 сервисов, запущенных в Docker-контейнерах:

СервисТехнологияНазначениеПорт
PostgreSQLPostgreSQL 15База данных5432
RedisRedis 7Кэш и брокер для Celery6379
DjangoDjango 4.2 + GunicornОсновное приложение8000
Celery WorkerCelery 5.3Асинхронные задачи-
Celery BeatCelery BeatПланировщик задач-
NginxNginxВеб-сервер и прокси80
🐳 Локальный запуск через Docker Compose
Предварительные требования
Docker Engine 20.10+

Docker Compose 2.0+

Git

Шаги запуска
```bash
# 1. Клонировать репозиторий
git clone https://github.com/vladreson/habit_tracker.git
cd habit_tracker

# 2. Создать файл окружения
cp .env.example .env
# Отредактируйте .env, указав свои значения

# 3. Запустить все сервисы
docker compose up -d --build

# 4. Выполнить миграции
docker compose exec django python manage.py migrate

# 5. Создать суперпользователя
docker compose exec django python manage.py createsuperuser

# 6. Проверить работу
# Приложение будет доступно по адресу: http://localhost
# Документация API: http://localhost/swagger/
# Админ-панель: http://localhost/admin/
```
Команды управления
```bash
# Проверить статус контейнеров
docker compose ps

# Просмотреть логи
docker compose logs django --tail 50
docker compose logs celery --tail 50

# Остановить все контейнеры
docker compose down

# Остановить с удалением томов данных
docker compose down -v

# Пересобрать образы
docker compose build --no-cache
```
☁️ Настройка продакшен-сервера (Yandex Cloud)
1. Создание виртуальной машины
Войдите в Yandex Cloud Console

Создайте новую виртуальную машину:

Образ: Ubuntu 24.04 LTS

Платформа: Intel Ice Lake

Память: 2 ГБ RAM

Диск: 20 GB SSD

Публичный IP: Включить

SSH-ключ: Добавить ваш публичный ключ

2. Настройка сервера
Подключитесь к серверу по SSH:

```bash
ssh -i ~/.ssh/id_rsa username@<your-server-ip>
```
Установите Docker и Docker Compose:

```bash
# Обновить систему
sudo apt update && sudo apt upgrade -y

# Установить Docker
sudo apt install -y docker.io
sudo systemctl enable docker
sudo systemctl start docker

# Установить Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Добавить пользователя в группу docker
sudo usermod -aG docker $USER
newgrp docker

# Проверить установку
docker --version
docker compose version
```
3. Настройка файрвола
```bash
# Разрешить необходимые порты
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS (опционально)
sudo ufw --force enable
sudo ufw status
```
⚙️ Настройка CI/CD с GitHub Actions
1. Подготовка репозитория
Убедитесь, что в репозитории есть следующие файлы:

text
.github/workflows/ci-cd.yml  # Workflow для CI/CD
docker-compose.yml           # Конфигурация Docker Compose
Dockerfile                   # Dockerfile для Django
nginx/Dockerfile             # Dockerfile для Nginx
nginx/nginx.conf             # Конфигурация Nginx
.env.example                 # Пример файла окружения
2. Настройка секретов в GitHub
Перейдите в репозиторий на GitHub: Settings → Secrets and variables → Actions

Добавьте следующие секреты:

СекретОписаниеПример значения
SERVER_HOSTIP-адрес сервера158.160.1.100
SERVER_USERИмя пользователя SSHusername
SERVER_PORTПорт SSH22
SERVER_SSH_KEYПриватный SSH-ключ-----BEGIN OPENSSH PRIVATE KEY-----...
3. Структура workflow (.github/workflows/ci-cd.yml)
Workflow состоит из двух джоб:

test - запускается при каждом пуше:

Установка Python и зависимостей

Запуск линтинга (flake8)

Запуск тестов

Сборка Docker-образов

deploy - запускается только при пуше в ветку main:

Копирование файлов на сервер через SSH

Запуск docker compose на сервере

Обновление контейнеров

🚀 Автоматический деплой
Как работает деплой
При пуше в ветку main срабатывает GitHub Actions workflow

Выполняются все проверки (тесты, линтинг, сборка образов)

При успешном прохождении проверок происходит деплой:

Копирование docker-compose.yml и конфигураций на сервер

Остановка текущих контейнеров

Запуск новых версий контейнеров

Ручной деплой (если необходимо)
```bash
# Копирование файлов на сервер
scp -r docker-compose.yml nginx/ username@server-ip:/opt/habit_tracker/

# Подключение к серверу и запуск
ssh username@server-ip
cd /opt/habit_tracker
docker compose down
docker compose up -d --build
```
📊 Мониторинг и логирование
Просмотр логов
```bash
# Все логи
docker compose logs

# Логи конкретного сервиса
docker compose logs django --tail 100
docker compose logs celery --tail 50
docker compose logs db --tail 30

# Логи в реальном времени
docker compose logs -f django
```
Мониторинг состояния
```bash
# Статус всех контейнеров
docker compose ps

# Использование ресурсов
docker stats

# Проверка работы приложения
curl http://localhost/api/habits/
curl http://localhost/health/
```
🔧 Устранение неполадок
Проблема: Ошибка подключения к PostgreSQL
```bash
# Проверить логи базы данных
docker compose logs db

# Проверить подключение из контейнера Django
docker compose exec django python -c "
import psycopg2
try:
    conn = psycopg2.connect(
        dbname='habits_db',
        user='habit_user',
        password='StrongPass123',
        host='db'
    )
    print('✅ Подключение успешно')
except Exception as e:
    print(f'❌ Ошибка: {e}')
"
```
Проблема: Celery не запускается
```bash
# Проверить установлен ли celery
docker compose exec django which celery

# Проверить конфигурацию
docker compose exec django python -c "from config import celery_app; print(celery_app.conf.broker_url)"

# Перезапустить celery
docker compose restart celery
```
Проблема: Nginx не проксирует запросы
```bash
# Проверить конфигурацию Nginx
docker compose exec nginx nginx -t

# Проверить доступность Django
docker compose exec nginx curl -f http://django:8000/ || echo "Django недоступен"
```
📚 Документация API
После запуска приложения доступна автоматически сгенерированная документация:

Swagger UI: http://ваш-сервер/swagger/

ReDoc: http://ваш-сервер/redoc/

Основные эндпоинты
POST /api/auth/register/ - Регистрация пользователя

POST /api/auth/token/ - Получение JWT токена

GET /api/habits/ - Список привычек

POST /api/habits/ - Создание привычки

GET /api/habits/{id}/ - Детали привычки

PUT /api/habits/{id}/ - Обновление привычки

DELETE /api/habits/{id}/ - Удаление привычки

POST /api/telegram/connect/ - Подключение Telegram

🧪 Тестирование
Запуск тестов локально
```bash
# Запуск всех тестов
docker compose exec django python manage.py test

# Запуск тестов с покрытием
docker compose exec django coverage run --source='.' manage.py test
docker compose exec django coverage report

# Запуск конкретного приложения
docker compose exec django python manage.py test habits.tests
```
Линтинг
```bash
# Проверка стиля кода
docker compose exec django flake8 .
```
📝 Правила привычек
Приложение реализует правила из книги "Атомные привычки":

⏱ Время выполнения ≤ 120 секунд

🎯 Нельзя одновременно связанную привычку и вознаграждение

😊 Приятные привычки не могут иметь вознаграждения

🔗 Связанные привычки должны быть приятными

🌐 Публичные привычки видны всем пользователям

🔒 Безопасность
Рекомендации для продакшена
Используйте сильные пароли в .env файле

Отключите DEBUG режим в продакшене

Настройте HTTPS через Let's Encrypt

Регулярно обновляйте зависимости

Настройте бэкапы базы данных

Обновление зависимостей
```bash
# Проверить устаревшие пакеты
docker compose exec django pip list --outdated

# Обновить requirements.txt
docker compose exec django pip freeze > requirements.txt
```
🤝 Вклад в проект
Создайте форк репозитория

Создайте ветку для новой функциональности

Внесите изменения

Напишите тесты

Создайте Pull Request

📞 Поддержка
При возникновении проблем:

Проверьте логи: docker compose logs

Убедитесь, что все переменные окружения установлены

Проверьте доступность портов на сервере

Создайте issue на GitHub

📄 Лицензия
Проект разработан в учебных целях.

Домашнее задание выполнено: ✅ Все критерии выполнены, проект развернут, CI/CD настроен, автоматический деплой работает.
