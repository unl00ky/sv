from pydantic import BaseModel

class Messages(BaseModel):
  id: str = None
  discussion_id: str
  user_id: str
  value: str
  name: str = None
