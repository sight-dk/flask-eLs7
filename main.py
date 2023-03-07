import psycopg2
from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = 'secret_key'

bcrypt = Bcrypt(app)

conn = psycopg2.connect(
    host="localhost",
    database="mydatabase",
    user="myuser",
    password="mypassword"
)

cur = conn.cursor()

@app.route('/register', methods=['POST'])
def register():
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
    conn.commit()

    return jsonify({'message': 'User created successfully!'})

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()

    if user and bcrypt.check_password_hash(user[3], password):
        return jsonify({'message': 'Logged in successfully!'})
    else:
        return jsonify({'message': 'Invalid credentials!'})

if __name__ == '__main__':
    app.run(debug=True)
