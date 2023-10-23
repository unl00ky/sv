import asyncio
import tkinter as tk
import tracemalloc

from chat_app.chat_window import ChatWindow
from client.authenticate import authenticate

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Chat App")

    # Change font and color
    root.configure(bg="lightgray")

    response_obj = authenticate()
    user_id = str(response_obj.get("id"))

    chat_app = ChatWindow(root, user_id)
    chat_app.create_widgets()

    # Set the column and row extensions to make the window resizable."
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)

    root.geometry("800x600")

    # tracemalloc.start()
    # chat_app.chat_messages.connect_to_websocket_server()
    root.mainloop()
    # asyncio.get_event_loop().run_until_complete(chat_app.chat_messages.connect_to_websocket_server())
