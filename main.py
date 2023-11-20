import asyncio
import threading
import tkinter as tk

from chat_app.chat_window import ChatWindow
from client.authenticate import authenticate


def start_async_task():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(chat_app.connect_to_websocket_server_recv())


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Chat App")

    # Change font and color
    root.configure(bg="black")

    response_obj = authenticate()
    user_id = str(response_obj.get("id"))

    chat_app = ChatWindow(root, user_id)

    thread = threading.Thread(target=start_async_task)
    thread.start()

    while not chat_app.websocket:
        pass

    chat_app.create_widgets()

    # Set the column and row extensions to make the window resizable."
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)

    root.geometry("800x600")

    root.mainloop()
