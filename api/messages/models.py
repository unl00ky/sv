from pydantic import BaseModel

class Messages(BaseModel):
  id: str = None
  discussion_id: str
  user_id: str
  value: str
  name: str = None

class GetMessages(BaseModel):
  user_id: str
  discussion_id: str