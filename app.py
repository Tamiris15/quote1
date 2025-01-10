from flask import Flask, render_template, request, jsonify
import sqlite3
import requests
import os

app = Flask(__name__)

# Путь к базе данных в постоянной файловой системе
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_DIR = os.path.join(BASE_DIR, 'data')  # Директория для хранения базы данных
DATABASE = os.path.join(DATABASE_DIR, 'daba.db')  # Полный путь к базе данных

# Создание директории для базы данных, если она не существует
if not os.path.exists(DATABASE_DIR):
    os.makedirs(DATABASE_DIR)
    print(f"Created directory for database: {DATABASE_DIR}")

# Функция для инициализации базы данных
def init_db():
    if not os.path.exists(DATABASE):
        print(f"Creating database at {DATABASE}")
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE daba (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                author TEXT NOT NULL,
                category TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
        print("Database created successfully.")

# Функция для подключения к базе данных
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Инициализация базы данных при запуске приложения
init_db()

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# Получение случайной цитаты из базы данных
@app.route('/get_random_quote', methods=['GET'])
def get_random_quote():
    conn = get_db_connection()
    quote = conn.execute('SELECT * FROM daba ORDER BY RANDOM() LIMIT 1').fetchone()
    conn.close()
    return jsonify(dict(quote))

# Добавление новой цитаты
@app.route('/add_quote', methods=['POST'])
def add_quote():
    data = request.json
    conn = get_db_connection()
    conn.execute('INSERT INTO daba (text, author, category) VALUES (?, ?, ?)',
                 (data['text'], data['author'], data['category']))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

# Получение цитат по автору
@app.route('/get_quotes_by_author/<author>', methods=['GET'])
def get_quotes_by_author(author):
    conn = get_db_connection()
    quotes = conn.execute('SELECT * FROM daba WHERE author = ?', (author,)).fetchall()
    conn.close()
    return jsonify([dict(quote) for quote in quotes])

# Получение цитат по категории
@app.route('/get_quotes_by_category/<category>', methods=['GET'])
def get_quotes_by_category(category):
    conn = get_db_connection()
    quotes = conn.execute('SELECT * FROM daba WHERE category = ?', (category,)).fetchall()
    conn.close()
    return jsonify([dict(quote) for quote in quotes])

# Получение списка всех авторов
@app.route('/get_authors', methods=['GET'])
def get_authors():
    conn = get_db_connection()
    authors = conn.execute('SELECT DISTINCT author FROM daba').fetchall()
    conn.close()
    return jsonify([author['author'] for author in authors])

# Получение списка всех категорий
@app.route('/get_categories', methods=['GET'])
def get_categories():
    conn = get_db_connection()
    categories = conn.execute('SELECT DISTINCT category FROM daba').fetchall()
    conn.close()
    return jsonify([category['category'] for category in categories])

# Получение случайной цитаты из внешнего API
@app.route('/get_external_quote', methods=['GET'])
def get_external_quote():
    response = requests.get('https://zenquotes.io/api/random')
    data = response.json()[0]
    return jsonify({'text': data['q'], 'author': data['a']})

if __name__ == '__main__':
    app.run(debug=True)