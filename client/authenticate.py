from chat_app.settings import USER_NAME, PASSWORD
from client.client import Client
from client.urls import AUTHENTICATE_ENDPOINT


def authenticate():
    client = Client()
    body = {
        "name": USER_NAME,
        "password": PASSWORD,
    }

    return client.post(AUTHENTICATE_ENDPOINT, body)