
from client.client import Client
from client.urls import MESSAGES_ENDPOINT


def get_messages(user_id, discussion_id):
    messages = Client().get(f"{MESSAGES_ENDPOINT}/?user_id={user_id}&discussion_id={discussion_id}")
    if not messages:
        return []

    return messages


def create_new_message(message_obj):
    client = Client()
    return client.post(MESSAGES_ENDPOINT, message_obj)

