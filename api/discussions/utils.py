import json

from storage.fake_db import fake_db
from uuid import uuid4
from .models import Discussions


def remove_duplicate(contacts):
    return list(dict.fromkeys(contacts))


def get_discussions(contacts):
    discussions = fake_db.get("discussions", {}).values()
    for discussion in discussions:
        if discussion["contacts"] == list(contacts):
            return True



def create_new_discussion(contacts):
    discussions = fake_db.get("discussions", {})
    discussion_id = str(uuid4())

    discussion_obj = {
        "id": discussion_id,
        "contacts": list(contacts),
        "name": None
    }

    discussions[discussion_id] = discussion_obj
    with open("storage/discussions.json", "w") as file:
        json.dump(discussions, file)
    return discussion_obj
