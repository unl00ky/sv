from client.client import Client
from client.urls import DISCUSSIONS_ENDPOINT


def create_new_discussion(user_id, selected_contact_id, name=None):
    client = Client()
    body = {
        "contacts": [user_id, selected_contact_id]
    }

    return client.post(DISCUSSIONS_ENDPOINT, body)


def get_discussions(user_id):
    client = Client()

    discussions = client.get(f"{DISCUSSIONS_ENDPOINT}/?user_id={user_id}")

    if not discussions:
        return []
    return discussions
