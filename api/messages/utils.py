from uuid import uuid4
import json

from storage.fake_db import fake_db


def create_new_message(message_data):
    new_message = message_data.model_dump()
    message_id = str(uuid4())

    users = fake_db.get("users", {}).values()
    messages = fake_db.get("messages", {})

    for user in users:
        if message_data.user_id == user["id"]:
            new_message["name"] = user["name"]

    new_message["id"] = message_id
    new_message["value"] = message_data.value

    messages[message_id] = new_message
    with open("storage/messages.json", "w") as file:
        json.dump(messages, file, default=str)
    return messages[message_id]
