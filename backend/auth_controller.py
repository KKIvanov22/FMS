from flask import jsonify, request, make_response
from firebase_admin import auth, db
import logging

def register_handler():
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
        "RoleInCompany": role_in_company,
        "Level": 1
        })
        response = make_response(jsonify({"message": "registered successful"}), 200)
        response.set_cookie("user_id", user_record.uid, httponly=False, samesite='None', secure=True)
        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def login_handler():
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

def get_user_handler():
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

def link_google_handler():
    print("link_google_handler called")
    try:
        data = request.get_json()
        print(f"Received data: {data}")
        id_token = data.get("idToken")
        print(f"ID Token: {id_token}")

        decoded_token = auth.verify_id_token(id_token)
        print(f"Decoded token: {decoded_token}")
        google_uid = decoded_token["uid"]
        print(f"Google UID: {google_uid}")

        current_user = auth.get_user(google_uid)
        print(f"Current user: {current_user}")

        google_client_id = firebase_admin.get_app().credential.service_account_info.get("google_client_id")
        print(f"Google Client ID: {google_client_id}")

        if not google_client_id:
            print("Google Client ID is missing from the config")
            return jsonify({"error": "Google Client ID is missing from the config"}), 400

        google_credential = auth.OAuthProvider("google.com").credential(id_token)
        print(f"Google credential: {google_credential}")

        auth.update_user(current_user.uid, provider_to_link=google_credential)
        print("Google account linked successfully")

        return jsonify({"message": "Google account linked successfully!"}), 200

    except Exception as e:
        print(f"Error linking Google account: {e}")
        return jsonify({"error": str(e)}), 400