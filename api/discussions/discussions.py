import json
from .models import Discussions

from fastapi import APIRouter, HTTPException

from storage.fake_db import fake_db
from .utils import remove_duplicate, get_discussions, create_new_discussion

discussions_router = APIRouter()


# "contacts": ["9a398f4e-09ea-4544-993e-dfaa35db139c", "c59cafe9-a6fe-40bf-be41-d63a640d253c"]


@discussions_router.post("/api/discussions")
def create_discussion(data: Discussions):
    contacts = data.contacts
    group_name = data.group_name
    users = fake_db.get("users", {})
    for contact in contacts:
        if contact not in users:
            raise HTTPException(status_code=404, detail="user not found")

    contacts = remove_duplicate(contacts)

    discussion = get_discussions(contacts)
    if discussion:
        raise HTTPException(status_code=404, detail="discussion already exists")

    discussion = create_new_discussion(contacts, group_name)
    return discussion


@discussions_router.get("/api/discussions/")
def get_discussion(user_id: str):
    users = fake_db.get("users", {})
    discussions = fake_db.get("discussions", {}).values()
    
    if user_id is None:
        return list(discussions)
    
    user_discussions = []
    for discussion in discussions:
        if user_id in discussion["contacts"]:
            user_discussions.append(discussion)

    for discussion in user_discussions:
        if len(discussion["contacts"]) >= 2:
            users_in_discussion = []
            for contact in discussion["contacts"]:
                if contact != user_id:
                    users_in_discussion.append(users[contact]["name"])
                    contacts_str = ", ".join(users_in_discussion)
                    discussion["name"] = contacts_str
        elif len(discussion["contacts"]) == 1:
            discussion["name"] = users[user_id]["name"]
    return user_discussions
            

