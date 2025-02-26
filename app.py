import logging
import subprocess
from flask import Flask
from flask_cors import CORS
from firebase_admin import credentials, db, auth
import firebase_admin

from datetime import datetime

from backend.auth_controller import register_handler, login_handler, get_user_handler, link_google_handler
from backend.company_controller import update_company_handler, get_companies_handler, add_company_material_handler, get_company_material_handler, update_company_material_handler, update_company_name_handler
from backend.team_controller import add_team_handler, get_teams_handler, update_team_handler, add_team_material_handler, get_team_material_handler, update_team_material_handler
from backend.user_controller import update_user_handler, update_user_role_handler, get_users_handler, get_employee_tasks_handler, get_all_users_handler
from backend.tasks_controller import add_team_tasks_handler, get_team_tasks_handler
from backend.support_controller import add_support_handler, get_support_handler, update_support_handler
from backend.chat_controller import create_chat_handler, send_message_handler, get_chats_handler, get_messages_handler

cred = credentials.Certificate("adminsdk.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://noit10-bks-default-rtdb.europe-west1.firebasedatabase.app/"
})

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG)

# ----------------------------------------------------------------
# Auth routes
@app.route('/register', methods=['POST'])
def register():
    return register_handler()

@app.route('/login', methods=['POST'])
def login():
    return login_handler()

@app.route('/user', methods=['GET'])
def get_user():
    return get_user_handler()

@app.route('/link-google', methods=['POST'])
def link_google():
    return link_google_handler()

# ----------------------------------------------------------------
# Company routes
@app.route('/update_company', methods=['PUT'])
def update_company():
    return update_company_handler()

@app.route('/get_companies', methods=['GET'])
def get_companies():
    return get_companies_handler()

@app.route('/add_company_material', methods=['POST'])
def add_company_material():
    return add_company_material_handler()

@app.route('/get_company_material', methods=['GET'])
def get_company_material():
    return get_company_material_handler()

@app.route('/update_company_material', methods=['POST'])
def update_company_material():
    return update_company_material_handler()

@app.route('/update_company_name', methods=['PUT'])
def update_company_name():
    return update_company_name_handler()

# ----------------------------------------------------------------
# Team routes
@app.route('/add_team', methods=['POST'])
def add_team():
    return add_team_handler()

@app.route('/get_teams', methods=['GET'])
def get_teams():
    return get_teams_handler()

@app.route('/update_team', methods=['PUT'])
def update_team():
    return update_team_handler()

@app.route('/add_team_material', methods=['POST'])
def add_team_material():
    return add_team_material_handler()

@app.route('/get_team_material', methods=['GET'])
def get_team_material():
    return get_team_material_handler()

@app.route('/update_team_material', methods=['POST'])
def update_team_material():
    return update_team_material_handler()

# ----------------------------------------------------------------
# User routes
@app.route('/update_user', methods=['PUT'])
def update_user():
    return update_user_handler()

@app.route('/update_user_role', methods=['PUT'])
def update_user_role():
    return update_user_role_handler()

@app.route('/get_users', methods=['GET'])
def get_users():
    return get_users_handler()

@app.route('/get_employee_tasks', methods=['GET'])
def get_employee_tasks():
    return get_employee_tasks_handler()
@app.route('/get_all_users', methods=['GET'])
def get_all_users():
    return get_all_users_handler()
# ----------------------------------------------------------------
# Tasks routes
@app.route('/add_team_tasks', methods=['POST'])
def add_team_tasks():
    return add_team_tasks_handler()

@app.route('/get_team_tasks', methods=['GET'])
def get_team_tasks():
    return get_team_tasks_handler()

# ----------------------------------------------------------------
# Support routes
@app.route('/add_support', methods=['POST'])
def add_support():
    return add_support_handler()

@app.route('/get_support', methods=['GET'])
def get_support():
    return get_support_handler()

@app.route('/update_support', methods=['PUT'])
def update_support():
    return update_support_handler()

# ----------------------------------------------------------------
# Chat routes
@app.route('/create_chat', methods=['POST'])
def create_chat():
    return create_chat_handler()

@app.route('/send_message', methods=['POST'])
def send_message():
    return send_message_handler()

@app.route('/get_chats', methods=['GET'])
def get_chats():
    return get_chats_handler()

@app.route('/get_messages', methods=['GET'])
def get_messages():
    return get_messages_handler()

# ----------------------------------------------------------------
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