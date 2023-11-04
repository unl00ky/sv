from fastapi import APIRouter, HTTPException

from api.users.models import UserCreate
from storage.fake_db import fake_db

contacts_router = APIRouter()


@contacts_router.get("/api/contacts")
def get_all_contacts():
    users = fake_db.get("users", {}).values()
    return list(users)


@contacts_router.get("/api/contacts/{user_id}", response_model=UserCreate)
def get_contact(user_id):
    user = fake_db.get("users", {}).get(str(user_id))

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
