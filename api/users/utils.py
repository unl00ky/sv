import json
from uuid import uuid4

from storage.fake_db import fake_db


def get_user_data(data):
    users = fake_db.get("users", {}).values()
    for user in users:
        name = user.get("name")
        password = user.get("password")

        if name == data.name and password == data.password:
            return user
    return None


def create_user(data):
    users = fake_db.get("users", {})

    user_id = str(uuid4())

    user_data = data.model_dump()
    user_data["id"] = user_id
    users[user_id] = user_data

    with open("storage/users.json", "w") as f:
        json.dump(users, f, default=str)
    return user_data
