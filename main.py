import psycopg2
from flask import Flask, request, jsonify, session
import hashlib
import os
from datetime import timedelta
from functools import wraps

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

@app.route('/register', methods=['GET', 'POST'])
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
    print(email)
    print(hashed_password)


    cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, hashed_password))
    user = cur.fetchone()
    print("DONE QUERY")
    print(user)

    if user:
        session['email'] = email
        name = user[1]
        session['name'] = name
        print(name)
        print(email)
        response = jsonify({'message': 'Logged in!', 'name': name, 'email': email})
        response.set_cookie('session', value=session['email'], httponly=True, secure=True, max_age=timedelta(days=30))
        return response
    else:
        return jsonify({'message': 'Invalid credentials!'})






def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_cookie_value = request.cookies.get('session')
        if not session_cookie_value:
            return jsonify({'message': 'You are not authenticated. Please log in.'}), 401
        # You can also check for other conditions here, like checking if the session cookie has expired.
        return f(*args, **kwargs)
    return decorated_function



@app.route('/dashboard')
@login_required
def dashboard():
    # Do something with the authenticated user
    # ...
    if 'name' in session:
        return jsonify({'name': session['name']})

    
    return jsonify({'message': 'You are authenticated and authorized to access the dashboard.'})

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('email', None)
    return jsonify({'message': 'Logged out successfully!'})


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
