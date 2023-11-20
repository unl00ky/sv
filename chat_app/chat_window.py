import tkinter as tk
import asyncio
import websockets
from tkinter import messagebox

from .discussion_list import DiscussionList
from .chat_messages import ChatMessages
from .settings import DOMAIN, PORT, USER_NAME


class ChatWindow:
    def __init__(self, root=None, user_id=None):
        self.root = root
        self.user_id = user_id
        self.discussion_list = None
        self.chat_messages = None
        self.websocket = None

    async def connect_to_websocket_server_recv(self):
        # await asyncio.sleep(2)
        try:
            async with websockets.connect(f"ws://{DOMAIN}:{PORT}/ws/{USER_NAME}") as websocket:
                self.websocket = websocket
                while True:

                    response = await websocket.recv()
                    if response == "discussion":
                        self.discussion_list.load_discussions()
                    elif response == "New message":
                        self.chat_messages.on_item_select(response)

        except websockets.ConnectionClosed:
            messagebox.showerror("API error message", "Connection closed.")
        except Exception as e:
            messagebox.showerror("API error message", f"Error: {str(e)}")

    def create_widgets(self):
        discussion_frame = tk.Frame(self.root)
        self.discussion_list = DiscussionList(discussion_frame, self.user_id, self.websocket)
        self.discussion_list.pack(side="left", fill="both", expand=True)

        chat_frame = tk.Frame(self.root)
        self.chat_messages = ChatMessages(chat_frame, self.discussion_list, self.user_id, self.websocket)
        self.chat_messages.pack(side="right", fill="both", expand=True)
