import uuid
import hashlib
import datetime
from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Postgres database connection
conn = psycopg2.connect(
    host="containers-us-west-36.railway.app",
    database="railway",
    user="postgres",
    password="QI1B5PcTFIekHXgUjjzo",
    port = "7775"
)

# Cursor
cur = conn.cursor()


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    firstname = data['firstname']
    lastname = data['lastname']
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    try:
        cur.execute("INSERT INTO users (username, password, firstname, lastnmae) VALUES (%s, %s, %s, %s)", (username, hashed_password, firstname, lastname))
        conn.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    try:
        cur.execute("SELECT id FROM users WHERE username=%s AND password=%s", (username, hashed_password))
        user_id = cur.fetchone()
        if user_id:
            token = str(uuid.uuid4())
            expiration = datetime.datetime.now() + datetime.timedelta(hours=1)
            cur.execute("INSERT INTO sessions (user_id, token, expiration) VALUES (%s, %s, %s)", (user_id[0], token, expiration))
            conn.commit()
            return jsonify({'success': True, 'token': token})
        else:
            return jsonify({'success': False, 'error': 'Invalid username or password'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
     app.run(debug=True, port=os.getenv("PORT", default=5000))
