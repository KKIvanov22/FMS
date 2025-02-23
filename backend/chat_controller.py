import logging
from flask import jsonify, request
from firebase_admin import db
from datetime import datetime

def create_chat_handler():
    data = request.get_json()
    participants = data.get('participants')
    user_id = request.cookies.get('user_id')

    if not user_id:
        return jsonify({"error": "User ID not found in cookies"}), 400

    if not participants or not isinstance(participants, list):
        return jsonify({"error": "Participants must be a list"}), 400

    if user_id not in participants:
        participants.append(user_id)

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
            user_chats = accounts_chats_ref.get() or []
            if not isinstance(user_chats, list):
                user_chats = []
            user_chats.append(str(chat_id))
            accounts_chats_ref.set(user_chats)

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
    logging.debug("get_chats_handler called")
    user_id = request.cookies.get('user_id')
    if not user_id:
        logging.debug("User ID not found in cookies.")
        return jsonify({"error": "User ID not found"}), 400

    try:
        logging.debug(f"Fetching chats for user_id: {user_id}")
        user_chats_ref = db.reference(f'Accounts/{user_id}/Chats')
        user_chats = user_chats_ref.get() or []
        logging.debug(f"user_chats: {user_chats}")

        if not isinstance(user_chats, list):
            logging.debug("Invalid data format for user chats")
            return jsonify({"error": "Invalid data format for user chats"}), 500

        chats = {}
        users = []
        for chat_id in user_chats:
            logging.debug(f"Fetching chat data for chat_id: {chat_id}")
            chat_data = db.reference(f'Chats/{chat_id}').get() or {}
            logging.debug(f"chat_data: {chat_data}")
            chats[chat_id] = chat_data

            # Collect user data
            for participant in chat_data.get("Participants", []):
                user_data = db.reference(f'Accounts/{participant}').get()
                if user_data:
                    users.append({"uid": participant, "Username": user_data.get("Username")})

        username = db.reference(f'Accounts/{user_id}/Username').get()
        logging.debug(f"username: {username}")
        return jsonify({
            "chats": chats,
            "username": username,
            "users": users
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