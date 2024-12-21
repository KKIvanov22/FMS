import sqlite3
import subprocess
from flask import Flask, jsonify, request, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import logging
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.DEBUG)

DATABASE = 'data/accounts.db'

def get_db_connection():
    print("Establishing database connection...")
    conn = sqlite3.connect(DATABASE)
    print("Database connection established.")
    return conn

@app.route('/register', methods=['POST'])
def register():
    print("Register endpoint called.")
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    company = data.get("company")
    role = data.get("role")
    role_in_company = data.get("roleInCompany")
    
    if not username or not password or not email:
        print("Missing username, password, or email.")
        return jsonify({"error": "Missing username, password, or email"}), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT 1 FROM Accounts WHERE Username = ? OR Email = ?", (username, email))
        if cursor.fetchone():
            print(f"Username {username} or email {email} already exists.")
            return jsonify({"error": "Username or email already exists"}), 409
        
        password_hash = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO Accounts (Username, Password, Email, Company, Role, RoleInCompany) VALUES (?, ?, ?, ?, ?, ?)",
            (username, password_hash, email, company, role, role_in_company)
        )
        conn.commit()
        print(f"User {username} registered successfully.")
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    print("Login endpoint called.")
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        print("Missing username or password.")
        return jsonify({"error": "Missing username or password"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT Password FROM Accounts WHERE Username = ?", (username,))
        row = cursor.fetchone()

        if row and check_password_hash(row[0], password):
            response = make_response(jsonify({"message": "Login successful"}), 200)
            response.set_cookie("username", username, httponly=False, samesite='None', secure=True)
            print(f"User {username} logged in successfully.")
            return response
        else:
            print(f"Invalid username or password for user {username}.")
            return jsonify({"error": "Invalid username or password"}), 401
    except Exception as e:
        logging.error(f"Error during login: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/user', methods=['GET'])
def get_user():
    print("User endpoint called.")
    username = request.cookies.get('username')
    
    if not username:
        print("Username not found in cookies.")
        return jsonify({"error": "Username not found in cookies"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT Username, Email, Company, Role, RoleInCompany FROM Accounts WHERE Username = ?", (username,))
        row = cursor.fetchone()

        if row:
            user_data = {
                "username": row[0],
                "email": row[1],
                "company": row[2],
                "role": row[3],
                "roleInCompany": row[4]
            }
            print(f"User data for {username} fetched successfully.")
            return jsonify(user_data), 200
        else:
            print(f"User {username} not found.")
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        logging.error(f"Error fetching user data: {e}")
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