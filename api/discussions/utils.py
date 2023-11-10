import json

from storage.fake_db import fake_db
from uuid import uuid4
from .models import Discussions


def remove_duplicate(contacts):
    return list(dict.fromkeys(contacts))


def get_discussions(contacts):
    discussions = fake_db.get("discussions", {}).values()
    for discussion in discussions:
        if set(discussion["contacts"]) == set(contacts):
            return True



def create_new_discussion(contacts, group_name):
    discussions = fake_db.get("discussions", {})
    discussion_id = str(uuid4())

    if group_name:
        discussion_obj = {
            "id": discussion_id,
            "contacts": contacts,
            "group_name": group_name
        }
    else:
        discussion_obj = {
            "id": discussion_id,
            "contacts": contacts,
        }
        

    discussions[discussion_id] = discussion_obj
    with open("storage/discussions.json", "w") as file:
        json.dump(discussions, file)
    return discussion_obj
