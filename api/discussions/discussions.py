from .models import Discussions

from fastapi import APIRouter, HTTPException

from storage.fake_db import fake_db
from .utils import remove_duplicate, get_discussions, create_new_discussion

discussions_router = APIRouter()


# "contacts": ["9a398f4e-09ea-4544-993e-dfaa35db139c", "c59cafe9-a6fe-40bf-be41-d63a640d253c"]


@discussions_router.post("/api/discussions", response_model=Discussions)
def create_discussion(data: Discussions):
    contacts = data.contacts
    users = fake_db.get("users", {})
    for contact in contacts:
        if contact not in users:
            raise HTTPException(status_code=404, detail="user not found")

    contacts = remove_duplicate(contacts)

    discussion = get_discussions(contacts)
    if discussion:
        raise HTTPException(status_code=404, detail="discussion already exists")

    new_discussion = create_new_discussion(contacts)
    return new_discussion


@discussions_router.get("/api/discussions/{user_id}")
def get_discussion(user_id):
    users = fake_db.get("users", {})
    discussions = fake_db.get("discussions", {}).values()
    for discussion in discussions:
        if user_id in discussion["contacts"]:
            for contact in discussion["contacts"]:
                if user_id != contact:
                    discussion["name"] = users[contact].get("name")
                    return discussion
                elif len(discussion["contacts"]) == 1:
                    discussion["name"] = users[user_id].get("name")
