from flask import jsonify, request
from firebase_admin import db

def add_team_handler():
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

def get_teams_handler():
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

def update_team_handler():
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

def add_team_material_handler():
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
        for material in materials:
            material_id = material.get('id')
            quantity = material.get('quantity')
            if not material_id or not quantity:
                print("Material id or quantity missing.")
                return jsonify({"error": "Material id or quantity missing"}), 400
            ref.child(material_id).set({"quantity": quantity})
        print(f"Materials added successfully to team {target_team} in company {target_company}.")
        return jsonify({"message": "Materials added successfully"}), 200
    except Exception as e:
        logging.error(f"Error adding materials: {e}")
        return jsonify({"error": str(e)}), 500
        
def get_team_material_handler():
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
            material_list = [{"id": key, "quantity": value["quantity"]} for key, value in materials.items()]
            print(f"Materials for team {team} in company {company} fetched successfully.")
            return jsonify(material_list), 200
        else:
            print(f"No materials found for team {team} in company {company}.")
            return jsonify({"error": "No materials found"}), 404
    except Exception as e:
        logging.error(f"Error fetching materials: {e}")
        return jsonify({"error": str(e)}), 500

def update_team_material_handler():
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