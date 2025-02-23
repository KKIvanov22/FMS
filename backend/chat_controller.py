from flask import jsonify, request
from firebase_admin import db
from datetime import datetime

def create_chat_handler():
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

def send_message_handler():
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


def get_chats_handler():
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

def get_messages_handler():
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