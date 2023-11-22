import tkinter as tk

from .discussion_list import DiscussionList
from .chat_messages import ChatMessages


class ChatWindow:
    def __init__(self, root=None, user_id=None):
        self.root = root
        self.user_id = user_id
        self.discussion_list = None
        self.chat_messages = None

    def create_widgets(self):
        discussion_frame = tk.Frame(self.root)
        self.discussion_list = DiscussionList(discussion_frame, self.user_id)
        self.discussion_list.pack(side="left", fill="both", expand=True)

        chat_frame = tk.Frame(self.root)
        self.chat_messages = ChatMessages(chat_frame, self.discussion_list)
        self.chat_messages.pack(side="right", fill="both", expand=True)
