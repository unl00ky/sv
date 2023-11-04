from fastapi import FastAPI

from api.users.users import users_router
from api.contacts.contacts import contacts_router
from api.discussions.discussions import discussions_router

app = FastAPI()
app.include_router(users_router)
app.include_router(contacts_router)
app.include_router(discussions_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
