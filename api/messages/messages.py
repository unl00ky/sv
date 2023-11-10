from fastapi import APIRouter, HTTPException

from api.messages.models import Messages

from storage.fake_db import fake_db
from api.messages.utils import create_new_message

messages_router = APIRouter()

  #  "20bf9761-3dc8-4081-ab1a-08a746edb16b":{
  #     "id":"20bf9761-3dc8-4081-ab1a-08a746edb16b",
  #     "discussion_id":"1a8a6517-29b4-4604-a653-566279404c47",
  #     "user_id":"35b12302-a87a-4fbd-b5d2-ff1a9f168dff",
  #     "value":"salut\n",
  #     "name":"Andrei"
  #  },

@messages_router.post("/api/messages")
def create_message(message_data: Messages):
  discussions = fake_db.get("discussions", {}).values()

  for discussion in discussions:
    if message_data.discussion_id == discussion["id"] and message_data.user_id in discussion["contacts"]:
      new_message = create_new_message(message_data)
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

