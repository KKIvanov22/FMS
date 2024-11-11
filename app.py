import subprocess
from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
import pyodbc
import logging
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.DEBUG)

server = 'noit-10b.database.windows.net'
database = 'noit-10b'
username = ''
password = ''
driver = '{ODBC Driver 17 for SQL Server}'

def get_db_connection():
    print("Establishing database connection...")
    conn = pyodbc.connect(
        f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}'
    )
    print("Database connection established.")
    return conn


@app.route('/register', methods=['POST'])
def register():
    print("Register endpoint called.")
    data = request.get_json()
    print(f"Received data: {data}")
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")

    print(f"Received registration data: username={username}, email={email}")

    if not username or not password or not email:
        print("Missing username, password, or email.")
        return jsonify({"error": "Missing username, password, or email"}), 400

    password_hash = generate_password_hash(password)
    print(f"Generated password hash for {username}.")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Accounts (Username, PasswordHash, Email) VALUES (?, ?, ?)
        """, (username, password_hash, email))
        conn.commit()
        print(f"User {username} registered successfully.")
    except Exception as e:
        logging.error(f"Error during registration: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    print("Login endpoint called.")
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    print(f"Received login data: username={username}")

    if not username or not password:
        print("Missing username or password.")
        return jsonify({"error": "Missing username or password"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT PasswordHash FROM Accounts WHERE Username = ?", (username,))
        row = cursor.fetchone()

        if row and check_password_hash(row[0], password):
            print(f"User {username} logged in successfully.")
            return jsonify({"message": "Login successful"}), 200
        else:
            print(f"Invalid username or password for user {username}.")
            return jsonify({"error": "Invalid username or password"}), 401
    except Exception as e:
        logging.error(f"Error during login: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/hello', methods=['GET'])
def hello():
    print("Hello endpoint called.")
    return jsonify({"message": "Hello from the backend!"})

def run_electron():
    try:
        subprocess.run(["npm", "start"], check=True)
    except subprocess.CalledProcessError as e:
        print("Error starting Electron:", e)

if __name__ == "__main__":
    electron_process = subprocess.Popen(["npm", "start"], shell=True)

    try:
        app.run(port=5000) 
    finally:
        electron_process.terminate()
