# Используем официальный образ Python как базовый
FROM python:3.9-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл с зависимостями в контейнер
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . /app/

# Устанавливаем переменную окружения для Flask (определяем порт для слушания)
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=80

# Открываем порт, на котором будет работать Flask
EXPOSE 80

# Запускаем сервер с помощью Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:app"]
