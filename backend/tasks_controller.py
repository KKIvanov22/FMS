from flask import jsonify, request
from firebase_admin import db
import logging

def add_team_tasks_handler():
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

def get_team_tasks_handler():
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
