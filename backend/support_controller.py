from flask import jsonify, request
from firebase_admin import db

def add_support_handler():
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

def get_support_handler():
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

def update_support_handler():
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