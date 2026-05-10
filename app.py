from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            amount INTEGER,
            created_at TEXT
        )
    ''')

    conn.commit()
    conn.close()


@app.route('/')
def index():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM expenses ORDER BY id DESC')
    data = cursor.fetchall()

    total = sum(item[2] for item in data)

    conn.close()

    return render_template(
        'index.html',
        data=data,
        total=total
    )


@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    amount = request.form['amount']

    created_at = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    cursor.execute(
        '''
        INSERT INTO expenses (title, amount, created_at)
        VALUES (?, ?, ?)
        ''',
        (title, amount, created_at)
    )

    conn.commit()
    conn.close()

    return redirect('/')


@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    cursor.execute(
        'DELETE FROM expenses WHERE id=?',
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/')


@app.route('/health')
def health():
    return {
        'status': 'healthy'
    }


@app.route('/time')
def time():
    return {
        'server_time': datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    }


if __name__ == '__main__':
    init_db()
    app.run(debug=True)