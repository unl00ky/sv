from client.client import Client
from client.urls import DISCUSSIONS_ENDPOINT


def create_new_discussion(user_id, selected_contacts, group_name):
    client = Client()
    contacts = [user_id]
    contacts.extend(selected_contacts)
    if group_name:
        body = {
            "contacts": contacts,
            "group_name": group_name
        }
    else:
        body = {
            "contacts": contacts
        }

    return client.post(DISCUSSIONS_ENDPOINT, body)


def update_discussion(user_id, selected_contacts, discussion_id):
    client = Client()
    contacts = [user_id]
    contacts.extend(selected_contacts)
    body = {
        "id": discussion_id,
        "contacts": contacts
    }
    return client.post(DISCUSSIONS_ENDPOINT, body)


def get_discussions(user_id):
    client = Client()

    discussions = client.get(f"{DISCUSSIONS_ENDPOINT}/?user_id={user_id}")

    if not discussions:
        return []
    return discussions
