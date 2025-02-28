from flask import jsonify, request
from firebase_admin import db
import logging

def update_company_handler():
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
            old_company = user.get("Company")
            ref.update({"Company": new_company})
            print(f"Company for user {user_id} updated successfully to {new_company}.")

            company_ref = db.reference(f'Companies/{old_company}')
            company_data = company_ref.get()
            if company_data:
                db.reference(f'Companies/{new_company}').set(company_data)
                company_ref.delete()
                print(f"Company {old_company} updated to {new_company} in Companies collection.")

            users_ref = db.reference('Accounts')
            users = users_ref.order_by_child('Company').equal_to(old_company).get()
            for uid, user_data in users.items():
                users_ref.child(uid).update({"Company": new_company})
                print(f"Updated company for user {uid} to {new_company}.")

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

def get_companies_handler():
    try:
        ref = db.reference('Companies')
        companies = ref.get()
        company_list = [{"name": name} for name in companies.keys()]
        return jsonify(company_list), 200
    except Exception as e:
        logging.error(f"Error fetching companies: {e}")
        return jsonify({"error": str(e)}), 500

def add_company_material_handler():
    print("Add company material endpoint called.")
    data = request.get_json()
    company = data.get("company")
    materials = data.get("materials")

    if not company or not materials:
        print("Missing company or materials.")
        return jsonify({"error": "Missing company or materials"}), 400

    try:
        ref = db.reference(f'Companies/{company}/Materials')
        ref.push(materials)
        print(f"Materials added successfully to company {company}.")
        return jsonify({"message": "Materials added successfully"}), 200
    except Exception as e:
        logging.error(f"Error adding materials: {e}")
        return jsonify({"error": str(e)}), 500

def get_company_material_handler():
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

def update_company_material_handler():
    print("Update company material endpoint called.")
    data = request.get_json()
    company = data.get('company')
    material_id = data.get('material_id')
    material_data = data.get('material_data')

    if not company:
        print("Company not provided.")
        return jsonify({"error": "Company not provided"}), 400

    if not material_id or not material_data:
        print("Material ID or material data not provided.")
        return jsonify({"error": "Material ID or material data not provided"}), 400

    try:
        ref = db.reference(f'Companies/{company}/Materials/{material_id}')
        ref.update(material_data)
        print(f"Material {material_id} for company {company} updated successfully.")
        return jsonify({"message": "Material updated successfully"}), 200
    except Exception as e:
        logging.error(f"Error updating material: {e}")
        return jsonify({"error": str(e)}), 500

def update_company_name_handler():
    data = request.get_json()
    username = data.get('username')
    user_id = request.cookies.get('user_id')

    if not username or not user_id:
        return jsonify({"error": "Username and user ID are required"}), 400

    try:
        user_ref = db.reference(f'Accounts/{user_id}')
        user = user_ref.get()
        if not user:
            return jsonify({"error": "User not found"}), 404

        new_company = user.get('Company')
        if not new_company:
            return jsonify({"error": "User's company not found"}), 404

        users_ref = db.reference('Accounts')
        users = users_ref.order_by_child('Username').equal_to(username).get()
        if not users:
            return jsonify({"error": "User not found"}), 404

        for uid, user_data in users.items():
            users_ref.child(uid).update({"Company": new_company})
            print(f"Updated company for user {uid} to {new_company}.")

        return jsonify({"message": "User's company updated successfully"}), 200
    except Exception as e:
        logging.error(f"Error updating user's company: {e}")
        return jsonify({"error": str(e)}), 500
    

def get_company_user_count_handler():
    user_id = request.cookies.get('user_id')

    if not user_id:
        return jsonify({"error": "User ID not found in cookies"}), 400

    try:
        ref = db.reference(f'Accounts/{user_id}')
        user = ref.get()

        if not user:
            return jsonify({"error": "User not found"}), 404

        company = user.get("Company")
        if not company:
            return jsonify({"error": "User does not belong to any company"}), 400

        company_users_ref = db.reference('Accounts')
        company_users = company_users_ref.order_by_child('Company').equal_to(company).get()

        user_count = len(company_users)
        return jsonify({"company_user_count": user_count}), 200
    except Exception as e:
        logging.error(f"Error fetching company user count: {e}")
        return jsonify({"error": str(e)}), 500