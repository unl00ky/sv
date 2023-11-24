from fastapi import APIRouter

from api.users.models import UserCreate
from api.users.utils import get_user_data, create_user
from api.websocket_manager.ws import ConnectionManager

users_router = APIRouter()


@users_router.post("/api/authenticate", response_model=UserCreate)
async def authenticate_user(user_data: UserCreate):
    user = get_user_data(user_data)
    if not user:
        user = create_user(user_data)

    return user
