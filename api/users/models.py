from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    password: str
    id: str = None
