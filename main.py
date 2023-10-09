import tkinter as tk
from chat_app.chat_window import ChatWindow


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Chat App")

    # Change font and color
    root.configure(bg="lightgray")

    chat_app = ChatWindow(root)
    chat_app.create_widgets()

    # Set the column and row extensions to make the window resizable."
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)

    root.geometry("800x600")
    root.mainloop()
