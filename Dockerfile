FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Сначала установите базовые зависимости без конфликтов
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir \
    Django==4.2.7 \
    djangorestframework==3.14.0 \
    psycopg2-binary==2.9.9 \
    redis==5.0.1

# Затем установите celery с совместимыми зависимостями
RUN pip install --no-cache-dir \
    celery[redis]==5.3.6 \
    kombu==5.3.5 \
    billiard==4.2.0

# Установите остальные зависимости из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
