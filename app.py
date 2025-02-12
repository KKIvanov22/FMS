import firebase_admin
from firebase_admin import credentials, db
from flask import Flask, jsonify, request, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import logging
from flask_cors import CORS
import subprocess

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
        return response
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
            response = make_response(jsonify({"message": "Login successful", "role": user["Role"]}), 200)
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
    print(f"Username from cookies: {username}")

    if not username:
        print("Username not found in cookies.")
        return jsonify({"error": "Username not found in cookies"}), 400

    try:
        ref = db.reference(f'Accounts/{username}')
        user = ref.get()

        if user:
            print(f"User data for {username} fetched successfully.")
            print(user)        
            return jsonify(user), 200
        else:
            print(f"User {username} not found.")
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        logging.error(f"Error fetching user data: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/update_company', methods=['PUT'])
def update_company():
    print("Update company endpoint called.")
    username = request.cookies.get('username')
    data = request.get_json()
    new_company = data.get("company")

    if not username:
        print("Username not found in cookies.")
        return jsonify({"error": "Username not found in cookies"}), 400

    if not new_company:
        print("New company not provided.")
        return jsonify({"error": "New company not provided"}), 400

    try:
        ref = db.reference(f'Accounts/{username}')
        user = ref.get()

        if user:
            ref.update({"Company": new_company})
            print(f"Company for user {username} updated successfully to {new_company}.")
            return jsonify({"message": "Company updated successfully"}), 200
        else:
            print(f"User {username} not found.")
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
    username = request.cookies.get('username')
    data = request.get_json()
    new_email = data.get("email")
    new_password = data.get("password")
    new_role = data.get("role")
    new_role_in_company = data.get("roleInCompany")

    if not username:
        print("Username not found in cookies.")
        return jsonify({"error": "Username not found in cookies"}), 400

    if not new_email and not new_password and not new_role and not new_role_in_company:
        print("No new data provided to update.")
        return jsonify({"error": "No new data provided to update"}), 400

    try:
        ref = db.reference(f'Accounts/{username}')
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

            ref.update(updates)
            print(f"User {username} updated successfully.")
            return jsonify({"message": "User updated successfully"}), 200
        else:
            print(f"User {username} not found.")
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        logging.error(f"Error updating user: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/update_user_role', methods=['PUT'])
def update_user_role():
    print("Update user role endpoint called.")
    current_username = request.cookies.get('username')
    data = request.get_json()
    target_username = data.get("username")
    new_role = data.get("role")

    if not current_username:
        print("Current username not found in cookies.")
        return jsonify({"error": "Current username not found in cookies"}), 400

    if not target_username or not new_role:
        print("Target username or new role not provided.")
        return jsonify({"error": "Target username or new role not provided"}), 400

    try:
        current_user_ref = db.reference(f'Accounts/{current_username}')
        current_user = current_user_ref.get()

        if not current_user:
            print(f"Current user {current_username} not found.")
            return jsonify({"error": "Current user not found"}), 404

        target_user_ref = db.reference(f'Accounts/{target_username}')
        target_user = target_user_ref.get()

        if not target_user:
            print(f"Target user {target_username} not found.")
            return jsonify({"error": "Target user not found"}), 404

        updates = {
            "Company": current_user["Company"],
            "Role": new_role
        }
        target_user_ref.update(updates)
        print(f"User {target_username} updated successfully with new role {new_role} and company {current_user['Company']}.")
        return jsonify({"message": "User role and company updated successfully"}), 200
    except Exception as e:
        logging.error(f"Error updating user role: {e}")
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