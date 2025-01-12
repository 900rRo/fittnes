import os
import psycopg2

# Получение URL базы данных из переменных окружения
DATABASE_URL = os.getenv('DATABASE_URL')

# Подключение к базе данных
try:
    conn = psycopg2.connect(DATABASE_URL)
    print("Успешное подключение к базе данных!")
except Exception as e:
    print(f"Ошибка подключения к базе данных: {e}")
