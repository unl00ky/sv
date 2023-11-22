import json

from storage.fake_db import fake_db
from uuid import uuid4
from api.websocket_manager.ws import ConnectionManager


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


def update_discussion(discussion_id, contacts):
    discussions = fake_db.get("discussions")
    current_discussion = discussions[discussion_id]
    discussion_contacts = current_discussion["contacts"]
    for contact in contacts:
        if contact not in discussion_contacts:
            discussion_contacts.append(contact)

    if current_discussion.get("group_name"):
        discussion_obj = {
            "id": discussion_id,
            "contacts": discussion_contacts,
            "group_name": current_discussion.get("group_name")
        }
    else:
        discussion_obj = {
            "id": discussion_id,
            "contacts": discussion_contacts,
        }
    discussions[discussion_id] = discussion_obj
    with open("storage/discussions.json", "w") as file:
        json.dump(discussions, file)
    return discussions[discussion_id]
