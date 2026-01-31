from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

# PostgreSQL database configuration
db_config = {
    'dbname': 'dbname',
    'user': 'postgres',
    'password': 'Madhu1234',
    'host': '10.0.2.61',  # Replace with your PostgreSQL host
    'port': '5432'         # Replace with your PostgreSQL port
}

# Create a 'guestbook' table in PostgreSQL with columns 'id', 'name', 'message', and 'timestamp'
def create_guestbook_table():
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS guestbook (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            message TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# Ensure the 'guestbook' table exists
create_guestbook_table()

@app.route('/')
def index():
    messages = get_messages()
    return render_template('index.html', messages=messages)

@app.route('/add', methods=['GET', 'POST'])
def add_message():
    if request.method == 'POST':
        name = request.form['name']
        message_text = request.form['message']
        add_message_to_db(name, message_text)
        return redirect('/')
    return render_template('add_message.html')

def get_messages():
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM guestbook ORDER BY timestamp DESC")
    messages = cursor.fetchall()
    conn.close()
    return messages

def add_message_to_db(name, message_text):
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO guestbook (name, message) VALUES (%s, %s)", (name, message_text))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
