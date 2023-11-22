from fastapi import APIRouter, HTTPException

from api.messages.models import Messages

from storage.fake_db import fake_db
from api.messages.utils import create_new_message

from api.websocket_manager.ws import ConnectionManager

messages_router = APIRouter()


@messages_router.post("/api/messages")
async def create_message(message_data: Messages):
    discussions = fake_db.get("discussions", {}).values()

    for discussion in discussions:
        if message_data.discussion_id == discussion["id"] and message_data.user_id in discussion["contacts"]:
            new_message = create_new_message(message_data)

            clients = []
            for contact in discussion["contacts"]:
                clients.append(contact)

            connection_manager = ConnectionManager()
            await connection_manager.broadcast("new message", clients)
            return new_message


@messages_router.get("/api/messages/")
def get_messages(user_id, discussion_id):
    discussions = fake_db.get("discussions", {}).values()
    messages = fake_db.get("messages", {}).values()
    all_messages = []
    for discussion in discussions:
        if discussion_id == discussion["id"] and user_id in discussion["contacts"]:
            for message in messages:
                if discussion_id == message["discussion_id"]:
                    all_messages.append(message)

    return all_messages
