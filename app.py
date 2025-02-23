import firebase_admin
from firebase_admin import credentials, db, auth
from flask import Flask, jsonify, request, make_response, redirect
from werkzeug.security import generate_password_hash, check_password_hash
import logging
import requests
from flask_cors import CORS
import subprocess
from datetime import datetime

companyCookie = "default_company"

cred = credentials.Certificate("adminsdk.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://noit10-bks-default-rtdb.europe-west1.firebasedatabase.app/"
})

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.DEBUG)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    company = data.get("company", "default_company")
    role = data.get("role", "employee")
    role_in_company = data.get("roleInCompany", "employee")

    if not username or not password or not email:
        return jsonify({"error": "Missing username, password, or email"}), 400

    try:
        user_record = auth.create_user(email=email, password=password, display_name=username)
        ref = db.reference('Accounts')
        ref.child(user_record.uid).set({
            "Username": username,
            "Email": email,
            "Company": company,
            "Role": role,
            "RoleInCompany": role_in_company
        })
        response = make_response(jsonify({"message": "registered successful"}), 200)
        response.set_cookie("user_id", user_record.uid, httponly=False, samesite='None', secure=True)
        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 400
    
    try:
        user_record = auth.get_user_by_email(email)
        user_data = db.reference('Accounts').child(user_record.uid).get()
        if user_data:
            response = make_response(jsonify({
                "message": "Login successful",
                "role": user_data.get("Role")
            }), 200)
            response.set_cookie("user_id", user_record.uid, httponly=False, samesite='None', secure=True)
            return response
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 401

@app.route('/user', methods=['GET'])
def get_user():
    print("User endpoint called.")
    user_id = request.cookies.get('user_id')
    print(f"user_id from cookies: {user_id}")

    if not user_id:
        print("User ID not found in cookies.")
        return jsonify({"error": "User ID not found in cookies"}), 400

    try:
        ref = db.reference(f'Accounts/{user_id}')
        user = ref.get()

        if user:
            print(f"User data for {user_id} fetched successfully.")
            print(user)        
            return jsonify(user), 200
        else:
            print(f"User {user_id} not found.")
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        logging.error(f"Error fetching user data: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/update_company', methods=['PUT'])
def update_company():
    print("Update company endpoint called.")
    user_id = request.cookies.get('user_id')
    data = request.get_json()
    new_company = data.get("company")

    if not user_id:
        print("User ID not found in cookies.")
        return jsonify({"error": "User ID not found in cookies"}), 400

    if not new_company:
        print("New company not provided.")
        return jsonify({"error": "New company not provided"}), 400

    try:
        ref = db.reference(f'Accounts/{user_id}')
        user = ref.get()

        if user:
            ref.update({"Company": new_company})
            print(f"Company for user {user_id} updated successfully to {new_company}.")
            return jsonify({
                "message": "Company updated successfully",
                "username": user.get("Username")
            }), 200
        else:
            print(f"User {user_id} not found.")
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        logging.error(f"Error updating company: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/add_team', methods=['POST'])
def add_team():
    print("Add team endpoint called.")
    print(request.get_json())
    data = request.get_json()
    print("Received data:", data)  
    company = data.get("company")
    team_name = data.get("teamName")
    members = data.get("members")

    if not company or not team_name or not members:
        print("Missing company, team name, or members.")
        return jsonify({"error": "Missing company, team name, or members"}), 400

    try:
        ref = db.reference(f'Companies/{company}/Teams')
        teams = ref.get() or {}

        if team_name in teams:
            print(f"Team {team_name} already exists in company {company}.")
            return jsonify({"error": "Team already exists"}), 409

        ref.child(team_name).set({
            "Members": members
        })

        print(f"Team {team_name} added successfully to company {company}.")
        return jsonify({"message": "Team added successfully"}), 200
    except Exception as e:
        logging.error(f"Error adding team: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/get_teams', methods=['GET'])
def get_teams():
    print("Get teams endpoint called.")
    company = request.args.get('company')

    if not company:
        print("Company not provided.")
        return jsonify({"error": "Company not provided"}), 400

    try:
        ref = db.reference(f'Companies/{company}/Teams')
        teams = ref.get()

        if teams:
            print(f"Teams for company {company} fetched successfully.")
            return jsonify(teams), 200
        else:
            print(f"No teams found for company {company}.")
            return jsonify({"error": "No teams found"}), 404
    except Exception as e:
        logging.error(f"Error fetching teams: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/update_team', methods=['PUT'])
def update_team():
    print("Update team endpoint called.")
    data = request.get_json()
    company = data.get("company")
    old_team_name = data.get("oldTeamName")
    new_team_name = data.get("newTeamName")
    members = data.get("members")

    if not company or not old_team_name or not new_team_name or not members:
        print("Missing company, old team name, new team name, or members.")
        return jsonify({"error": "Missing company, old team name, new team name, or members"}), 400

    try:
        ref = db.reference(f'Companies/{company}/Teams')
        teams = ref.get() or {}

        if old_team_name not in teams:
            print(f"Team {old_team_name} does not exist in company {company}.")
            return jsonify({"error": "Team does not exist"}), 404

        if old_team_name != new_team_name and new_team_name in teams:
            print(f"Team {new_team_name} already exists in company {company}.")
            return jsonify({"error": "New team name already exists"}), 409

        if old_team_name != new_team_name:
            ref.child(old_team_name).delete()
        ref.child(new_team_name).set({
            "Members": members
        })

        print(f"Team {old_team_name} updated successfully to {new_team_name} in company {company}.")
        return jsonify({"message": "Team updated successfully"}), 200
    except Exception as e:
        logging.error(f"Error updating team: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/update_user', methods=['PUT'])
def update_user():
    print("Update user endpoint called.")
    user_id = request.cookies.get('user_id')
    data = request.get_json()
    new_email = data.get("email")
    new_password = data.get("password")
    new_role = data.get("role")
    new_role_in_company = data.get("roleInCompany")
    new_profile_picture_url = data.get("profilePictureUrl")

    if not user_id:
        print("User ID not found in cookies.")
        return jsonify({"error": "User ID not found in cookies"}), 400

    if not new_email and not new_password and not new_role and not new_role_in_company and not new_profile_picture_url:
        print("No new data provided to update.")
        return jsonify({"error": "No new data provided to update"}), 400

    try:
        ref = db.reference(f'Accounts/{user_id}')
        user = ref.get()

        if user:
            updates = {}
            if new_email:
                updates["Email"] = new_email
            if new_password:
                updates["Password"] = generate_password_hash(new_password)
            if new_role:
                updates["Role"] = new_role
            if new_role_in_company:
                updates["RoleInCompany"] = new_role_in_company
            if new_profile_picture_url:
                updates["ProfilePictureUrl"] = new_profile_picture_url

            ref.update(updates)
            print(f"User {user_id} updated successfully.")
            return jsonify({
                "message": "User updated successfully",
                "username": user.get("Username")
            }), 200
        else:
            print(f"User {user_id} not found.")
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        logging.error(f"Error updating user: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/add_team_material', methods=['POST'])
def add_team_material():
    print("Add team material endpoint called.")
    data = request.get_json()
    target_company = data.get("company")
    target_team = data.get("team")
    materials = data.get("materials")

    if not target_company or not target_team or not materials:
        print("Missing company, team, or materials.")
        return jsonify({"error": "Missing company, team, or materials"}), 400

    try:
        ref = db.reference(f'Companies/{target_company}/Teams/{target_team}/Materials')
        ref.set(materials)
        print(f"Materials added successfully to team {target_team} in company {target_company}.")
        return jsonify({"message": "Materials added successfully"}), 200
    except Exception as e:
        logging.error(f"Error adding materials: {e}")
        return jsonify({"error": str(e)}), 500  

@app.route('/get_team_material', methods=['GET'])
def get_team_material():
    print("Get team material endpoint called.")
    company = request.args.get('company')
    team = request.args.get('team')

    if not company:
        print("Company not provided.")
        return jsonify({"error": "Company not provided"}), 400

    if not team:
        print("Team not provided.")
        return jsonify({"error": "Team not provided"}), 400

    try:
        ref = db.reference(f'Companies/{company}/Teams/{team}/Materials')
        materials = ref.get()

        if materials:
            print(f"Materials for team {team} in company {company} fetched successfully.")
            return jsonify(materials), 200
        else:
            print(f"No materials found for team {team} in company {company}.")
            return jsonify({"error": "No materials found"}), 404
    except Exception as e:
        logging.error(f"Error fetching materials: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/update_team_material', methods=['POST'])
def update_team_material():
    print("Update team material endpoint called.")
    data = request.get_json()
    company = data.get('company')
    team = data.get('team')
    materials = data.get('materials')

    if not company:
        print("Company not provided.")
        return jsonify({"error": "Company not provided"}), 400

    if not team:
        print("Team not provided.")
        return jsonify({"error": "Team not provided"}), 400

    if not materials:
        print("Materials not provided.")
        return jsonify({"error": "Materials not provided"}), 400

    try:
        ref = db.reference(f'Companies/{company}/Teams/{team}/Materials')
        ref.set(materials)
        print(f"Materials for team {team} in company {company} updated successfully.")
        return jsonify({"message": "Materials updated successfully"}), 200
    except Exception as e:
        logging.error(f"Error updating materials: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/add_company_material', methods=['POST'])
def add_company_material():
    print("Add company material endpoint called.")
    data = request.get_json()
    company = data.get("company")
    materials = data.get("materials")

    if not company or not materials:
        print("Missing company or materials.")
        return jsonify({"error": "Missing company or materials"}), 400

    try:
        ref = db.reference(f'Companies/{company}/Materials')
        ref.set(materials)
        print(f"Materials added successfully to company {company}.")
        return jsonify({"message": "Materials added successfully"}), 200
    except Exception as e:
        logging.error(f"Error adding materials: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/get_company_material', methods=['GET'])
def get_company_material():
    print("Get company material endpoint called.")
    company = request.args.get('company')

    if not company:
        print("Company not provided.")
        return jsonify({"error": "Company not provided"}), 400

    try:
        ref = db.reference(f'Companies/{company}/Materials')
        materials = ref.get()

        if materials:
            print(f"Materials for company {company} fetched successfully.")
            return jsonify(materials), 200
        else:
            print(f"No materials found for company {company}.")
            return jsonify({"error": "No materials found"}), 404
    except Exception as e:
        logging.error(f"Error fetching materials: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/update_company_material', methods=['POST'])
def update_company_material():
    print("Update company material endpoint called.")
    data = request.get_json()
    company = data.get('company')
    materials = data.get('materials')

    if not company:
        print("Company not provided.")
        return jsonify({"error": "Company not provided"}), 400

    if not materials:
        print("Materials not provided.")
        return jsonify({"error": "Materials not provided"}), 400

    try:
        ref = db.reference(f'Companies/{company}/Materials')
        ref.set(materials)
        print(f"Materials for company {company} updated successfully.")
        return jsonify({"message": "Materials updated successfully"}), 200
    except Exception as e:
        logging.error(f"Error updating materials: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/get_companies', methods=['GET'])
def get_companies():
    try:
        ref = db.reference('Companies')
        companies = ref.get()
        company_list = [{"name": name} for name in companies.keys()]
        return jsonify(company_list), 200
    except Exception as e:
        logging.error(f"Error fetching companies: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/update_company_name', methods=['PUT'])
def update_company_name():
    data = request.get_json()
    old_name = data.get('oldName')
    new_name = data.get('newName')

    if not old_name or not new_name:
        return jsonify({"error": "Old name and new name are required"}), 400

    try:
        ref = db.reference('Companies')
        companies = ref.get()

        if old_name not in companies:
            return jsonify({"error": "Company not found"}), 404

        if new_name in companies:
            return jsonify({"error": "New company name already exists"}), 409

        company_data = companies.pop(old_name)
        ref.child(old_name).delete()
        ref.child(new_name).set(company_data)

        return jsonify({"message": "Company name updated successfully"}), 200
    except Exception as e:
        logging.error(f"Error updating company name: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/add_team_tasks', methods=['POST'])
def add_team_tasks():
    print("Add team tasks endpoint called.")
    data = request.get_json()
    company = data.get("company")
    team_name = data.get("teamName")
    task_name = data.get("taskName")
    description = data.get("description")

    if not company or not team_name or not task_name or not description:
        print("Missing company, team name, task name, or description.")
        return jsonify({"error": "Missing company, team name, task name, or description"}), 400

    try:
        ref = db.reference(f'Companies/{company}/Teams/{team_name}/Tasks')
        tasks = ref.get() or {}

        if task_name in tasks:
            print(f"Task {task_name} already exists in team {team_name} of company {company}.")
            return jsonify({"error": "Task already exists"}), 409

        ref.child(task_name).set({
            "Description": description,
            "isDone": 0
        })

        print(f"Task {task_name} added successfully to team {team_name} in company {company}.")
        return jsonify({"message": "Task added successfully"}), 200
    except Exception as e:
        logging.error(f"Error adding task: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/get_users', methods=['GET'])
def get_users():
    query = request.args.get('query', '')
    try:
        ref = db.reference('Accounts')
        users = ref.order_by_child('Username').start_at(query).end_at(query + "\uf8ff").get()
        user_list = [{"uid": uid, "Username": user_data.get("Username")} for uid, user_data in users.items()]
        return jsonify(user_list), 200
    except Exception as e:
        logging.error(f"Error fetching users: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/get_team_tasks', methods=['GET'])
def get_team_tasks():
    print("Get team tasks endpoint called.")
    company = request.args.get('company')
    team = request.args.get('team')

    if not company:
        print("Company not provided.")
        return jsonify({"error": "Company not provided"}), 400

    if not team:
        print("Team not provided.")
        return jsonify({"error": "Team not provided"}), 400

    try:
        ref = db.reference(f'Companies/{company}/Teams/{team}/Tasks')
        tasks = ref.get()

        if tasks:
            print(f"Tasks for team {team} in company {company} fetched successfully.")
            return jsonify(tasks), 200
        else:
            print(f"No tasks found for team {team} in company {company}.")
            return jsonify({"error": "No tasks found"}), 404
    except Exception as e:
        logging.error(f"Error fetching tasks: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/get_employee_tasks', methods=['GET'])
def get_employee_tasks():
    print("Get employee tasks endpoint called.")
    user_id = request.cookies.get('user_id')

    if not user_id:
        print("User ID not found in cookies.")
        return jsonify({"error": "User ID not found in cookies"}), 400

    try:
        ref = db.reference(f'Accounts/{user_id}')
        user = ref.get()

        if not user:
            return jsonify({"error": "User not found"}), 404

        if user.get("RoleInCompany") != "employee":
            return jsonify({"error": "Not an employee"}), 403

        company = user.get("Company")
        teams_ref = db.reference(f'Companies/{company}/Teams')
        teams = teams_ref.get()

        if not teams:
            return jsonify({"error": "No teams found"}), 404

        employee_tasks = {}
        for team_name, team_data in teams.items():
            tasks_ref = db.reference(f'Companies/{company}/Teams/{team_name}/Tasks')
            tasks = tasks_ref.get() or {}
            for task_name, task_info in tasks.items():
                if "assignedTo" in task_info and task_info["assignedTo"] == user_id:
                    employee_tasks.setdefault(team_name, {})[task_name] = task_info

        print(f"Tasks for employee {user_id} fetched successfully.")
        return jsonify({
            "tasks": employee_tasks,
            "username": user.get("Username")
        }), 200
    except Exception as e:
        logging.error(f"Error fetching employee tasks: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/add_support', methods=['POST'])
def add_support():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    done = data.get('done', False)

    if not name or not description:
        return jsonify({"error": "Name and description are required"}), 400

    try:
        ref = db.reference('Support')
        ref.push({
            "Name": name,
            "Description": description,
            "Done": done
        })
        return jsonify({"message": "Support request added successfully"}), 200
    except Exception as e:
        logging.error(f"Error adding support request: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/get_support', methods=['GET'])
def get_support():
    try:
        ref = db.reference('Support')
        support_requests = ref.get()
        if support_requests:
            return jsonify(support_requests), 200
        else:
            return jsonify({"error": "No support requests found"}), 404
    except Exception as e:
        logging.error(f"Error fetching support requests: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/update_support', methods=['PUT'])
def update_support():
    data = request.get_json()
    support_id = data.get('id')
    name = data.get('name')
    description = data.get('description')
    done = data.get('done')

    if not support_id:
        return jsonify({"error": "Support ID is required"}), 400

    try:
        ref = db.reference(f'Support/{support_id}')
        support_request = ref.get()

        if not support_request:
            return jsonify({"error": "Support request not found"}), 404

        updates = {}
        if name:
            updates["Name"] = name
        if description:
            updates["Description"] = description
        if done is not None:
            updates["Done"] = done

        ref.update(updates)
        return jsonify({"message": "Support request updated successfully"}), 200
    except Exception as e:
        logging.error(f"Error updating support request: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/create_chat', methods=['POST'])
def create_chat():
    data = request.get_json()
    participants = data.get('participants')

    if not participants or not isinstance(participants, list):
        return jsonify({"error": "Participants must be a list"}), 400

    try:
        chats_ref = db.reference('Chats')
        all_chats = chats_ref.get() or {}
        chat_id = len(all_chats)  
        chat_ref = chats_ref.child(str(chat_id))

        chat_ref.set({
            "Participants": participants,
            "Messages": []
        })

        for participant in participants:
            accounts_chats_ref = db.reference(f'Accounts/{participant}/Chats')
            accounts_chats_ref.update({str(chat_id): True})

        return jsonify({"message": "Chat created", "chatId": chat_id}), 200
    except Exception as e:
        logging.error(f"Error creating chat: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    chat_id = data.get('chatId')
    message = data.get('message')
    sender = data.get('sender')

    if chat_id is None or not message or not sender:
        return jsonify({"error": "chatId, message, and sender are required"}), 400

    try:
        chat_ref = db.reference(f'Chats/{chat_id}/Messages')
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_message = {
            "message": message,
            "sender": sender,
            "time": timestamp
        }
        messages = chat_ref.get() or []
        messages.append(new_message)
        chat_ref.set(messages)

        return jsonify({"message": "Message sent"}), 200
    except Exception as e:
        logging.error(f"Error sending message: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/get_chats', methods=['GET'])
def get_chats():
    user_id = request.cookies.get('user_id')
    if not user_id:
        print("User ID not found in cookies.")
        return jsonify({"error": "User ID not found"}), 400

    try:
        user_chats_ref = db.reference(f'Accounts/{user_id}/Chats')
        user_chats = user_chats_ref.get() or {}

        if not isinstance(user_chats, dict):
            return jsonify({"error": "No chats found"}), 404

        chats = {}
        for chat_id in user_chats.keys():
            chat_data = db.reference(f'Chats/{chat_id}').get() or {}
            chats[chat_id] = chat_data

        username = db.reference(f'Accounts/{user_id}/Username').get()
        return jsonify({
            "chats": chats,
            "username": username
        }), 200
    except Exception as e:
        logging.error(f"Error fetching chats: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/get_messages', methods=['GET'])
def get_messages():
    chat_id = request.args.get('chatId')
    if chat_id is None:
        return jsonify({"error": "chatId is required"}), 400

    try:
        chat_ref = db.reference(f'Chats/{chat_id}/Messages')
        messages = chat_ref.get() or []
        return jsonify(messages), 200
    except Exception as e:
        logging.error(f"Error fetching messages: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/update_user_role', methods=['PUT'])
def update_user_role():
    data = request.get_json()
    username = data.get('username')
    new_role = data.get('role')

    if not username or not new_role:
        return jsonify({"error": "Username and new role are required"}), 400

    try:
        ref = db.reference('Accounts')
        users = ref.order_by_child('Username').equal_to(username).get()

        if not users:
            return jsonify({"error": "User not found"}), 404

        user_id = list(users.keys())[0]
        user_ref = db.reference(f'Accounts/{user_id}')
        user_ref.update({"Role": new_role})

        return jsonify({"message": "User role updated successfully"}), 200
    except Exception as e:
        logging.error(f"Error updating user role: {e}")
        return jsonify({"error": str(e)}), 500

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