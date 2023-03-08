import psycopg2
from flask import Flask, request, jsonify
import hashlib
import os

app = Flask(__name__)
app.secret_key = 'secret_key'

conn = psycopg2.connect(
    host="containers-us-west-36.railway.app",
    database="railway",
    user="postgres",
    password="QI1B5PcTFIekHXgUjjzo",
    port="7775"
)

cur = conn.cursor()

@app.route('/register', methods=['POST'])
def register():
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')

    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    cur.execute(f"INSERT INTO users (username, email, password) VALUES ('{name}', '{email}', '{hashed_password}')")
    conn.commit()

    return jsonify({'message': 'User created successfully!'})

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, hashed_password))
    user = cur.fetchone()
    print("DONE QUERY")
    print(user)

    if user:
        return jsonify({'message': 'Logged in successfully!'})
    else:
        return jsonify({'message': 'Invalid credentials!'})


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
