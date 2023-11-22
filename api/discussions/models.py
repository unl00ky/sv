from pydantic import BaseModel


class Discussions(BaseModel):
    id: str = None
    contacts: list
    name: str = None
    group_name: str = None
    status: str = None

