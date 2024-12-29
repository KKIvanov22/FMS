import firebase_admin
from firebase_admin import credentials, db
from flask import Flask, jsonify, request, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import logging
from flask_cors import CORS
import subprocess

cred = credentials.Certificate("adminsdk.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://noit10-bks-default-rtdb.europe-west1.firebasedatabase.app/"
})

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.DEBUG)

@app.route('/register', methods=['POST'])
def register():
    print("Register endpoint called.")
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    company = data.get("company", "default_company")
    role = data.get("role", "default_role")
    role_in_company = data.get("roleInCompany", "default_role_in_company")

    if not username or not password or not email:
        print("Missing username, password, or email.")
        return jsonify({"error": "Missing username, password, or email"}), 400

    try:
        ref = db.reference('Accounts')
        users = ref.get() or {}
        if username in users or any(user.get("Email") == email for user in users.values()):
            print(f"Username {username} or email {email} already exists.")
            return jsonify({"error": "Username or email already exists"}), 409

        password_hash = generate_password_hash(password)
        ref.child(username).set({
            "Password": password_hash,
            "Email": email,
            "Company": company,
            "Role": role,
            "RoleInCompany": role_in_company
        })

        print(f"User {username} registered successfully.")
        response = make_response(jsonify({"message": "registered successful"}), 200)
        response.set_cookie("username", username, httponly=False, samesite='None', secure=True)
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500

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
        ref = db.reference(f'Accounts/{username}')
        user = ref.get()

        if user and check_password_hash(user["Password"], password):
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

@app.route('/user', methods=['GET'])
def get_user():
    print("User endpoint called.")
    username = request.cookies.get('username')

    if not username:
        print("Username not found in cookies.")
        return jsonify({"error": "Username not found in cookies"}), 400

    try:
        ref = db.reference(f'Accounts/{username}')
        user = ref.get()

        if user:
            print(f"User data for {username} fetched successfully.")
            return jsonify(user), 200
        else:
            print(f"User {username} not found.")
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        logging.error(f"Error fetching user data: {e}")
        return jsonify({"error": str(e)}), 500

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
        electron_process
