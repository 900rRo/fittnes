# Используем официальный Python образ
FROM python:3.9-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл с зависимостями
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в контейнер
COPY . .

# Используем Gunicorn для запуска приложения с 4 рабочими процессами
CMD ["gunicorn", "-w", "4", "app:app"]
