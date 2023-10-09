import tkinter as tk
from tkinter import ttk


class DiscussionList(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.listbox_discussions = None
        self.button_discussions = None
        master.grid(row=0, column=0, sticky="ns")

        self.button_discussions = None
        self.listbox_discussions = None
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        initial_discussions = ["Alice", "Bob", "Charlie", "David"]
        self.button_discussions = tk.Button(
            self, text="New Chat", command=self.send_message, bg="blue", fg="white", font=("Arial", 12, "bold")
        )

        self.button_discussions.pack(fill=tk.X, padx=10, pady=10)

        self.listbox_discussions = ttk.Treeview(self, selectmode="browse")
        self.listbox_discussions.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Add initial discussions
        for discussion in initial_discussions:
            self.listbox_discussions.insert('', 'end', text=discussion)

    def send_message(self):
        pass
