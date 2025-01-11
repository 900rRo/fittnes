from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"
import psycopg2
from psycopg2.extras import RealDictCursor

# Настройки подключения
DB_HOST = "your_host"
DB_NAME = "fitness_app_db"
DB_USER = "your_user"
DB_PASSWORD = "your_password"

# Подключение к базе
try:
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        cursor_factory=RealDictCursor
    )
    print("Успешное подключение к базе данных")
except Exception as e:
    print("Ошибка подключения к базе данных:", e)
