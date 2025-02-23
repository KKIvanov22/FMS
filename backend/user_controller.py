from flask import jsonify, request
from firebase_admin import db, auth
import logging

def update_user_handler():
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
        logging.error(f"Error updating user: {e}")
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

def update_user_role_handler():
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
        user_ref.update({"RoleInCompany": new_role})

        return jsonify({"message": "User role updated successfully"}), 200
    except Exception as e:
        logging.error(f"Error updating user role: {e}")
        return jsonify({"error": str(e)}), 500

def get_users_handler():
    query = request.args.get('query', '')
    try:
        ref = db.reference('Accounts')
        users = ref.order_by_child('Username').start_at(query).end_at(query + "\uf8ff").get()
        user_list = [{"uid": uid, "Username": user_data.get("Username")} for uid, user_data in users.items()]
        return jsonify(user_list), 200
    except Exception as e:
        logging.error(f"Error fetching users: {e}")
        return jsonify({"error": str(e)}), 500


def get_employee_tasks_handler():
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
