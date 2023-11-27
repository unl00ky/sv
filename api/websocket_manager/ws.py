from starlette.websockets import WebSocket

from storage.fake_db import fake_db


class SingletonMeta(type):
    """
    A Singleton metaclass that creates a Singleton instance.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        If an instance of the class doesn't exist, create one. Otherwise, return the existing instance.
        """
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ConnectionManager(metaclass=SingletonMeta):
    def __init__(self):
        self.active_connections: {} = {}

    async def connect(self, websocket: WebSocket, client_id):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        # print(self.active_connections)

        discussions = fake_db.get("discussions", {}).values()

        clients = []
        for discussion in discussions:
            if client_id in discussion["contacts"]:
                for contact_id in self.active_connections.keys():
                    if contact_id in discussion["contacts"] and contact_id != client_id:
                        clients.append(contact_id)
        await self.broadcast("disconnected", clients)

    async def disconnect(self, websocket: WebSocket, client_id):
        self.active_connections.pop(client_id)
        # print(self.active_connections)
        discussions = fake_db.get("discussions", {}).values()

        clients = []
        for discussion in discussions:
            if client_id in discussion["contacts"]:
                for contact_id in self.active_connections.keys():
                    if contact_id in discussion["contacts"] and contact_id != client_id:
                        clients.append(contact_id)
        await self.broadcast("disconnected", clients)

    async def broadcast(self, message: str, users):
        for contact_id in users:
            # print(self.active_connections.get(contact_id))
            connection = self.active_connections.get(contact_id)
            if connection:
                await connection.send_text(message)
                # print(f"sent to {contact_id}")
