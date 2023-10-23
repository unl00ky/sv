import tkinter as tk
from tkinter import ttk

from chat_app.settings import USER_NAME
from client.contacts import get_contacts
from client.discussions import create_new_discussion, get_discussions


class DiscussionList(tk.Frame):
    def __init__(self, master=None, user_id=None):
        super().__init__(master)
        self.listbox_discussions = None
        self.button_discussions = None
        master.grid(row=0, column=0, sticky="ns")

        self.user_id = user_id
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self, text=f"Hello {USER_NAME}")
        label.pack()  # Place the label in the window

        discussions = get_discussions(self.user_id)

        self.button_discussions = tk.Button(
            self, text="New Chat", command=self.open_contact_popup, font=("Arial", 12, "bold")
        )

        self.button_discussions.pack(fill=tk.X, padx=10, pady=10)

        self.listbox_discussions = ttk.Treeview(self, selectmode="browse")
        self.listbox_discussions.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.listbox_discussions.heading("#0", text="Discussions")

        # Add initial discussions
        for discussion in discussions:
            self.listbox_discussions.insert('', 'end', text=discussion["name"], values=(discussion["id"]))

    def open_contact_popup(self):
        contact_popup = tk.Toplevel(self)
        contact_popup.title("Select a Contact")
        contact_popup.transient(self)

        contact_listbox = ttk.Treeview(contact_popup)

        contacts = get_contacts()
        for contact in contacts:
            contact_listbox.insert('', 'end', text=contact["name"], values=(contact["id"]))

        contact_listbox.pack(padx=10, pady=10)

        def add_selected_contact():
            selected_index = contact_listbox.selection()

            if selected_index:
                selected_item = contact_listbox.selection()[0]
                selected_discussion = contact_listbox.item(selected_item)

                selected_contact_id = str(selected_discussion["values"][0])
                text = selected_discussion["text"]

                discussion = create_new_discussion(self.user_id, selected_contact_id)
                if discussion:
                    self.listbox_discussions.insert('', 'end', text=text, values=(discussion["id"]))

                contact_popup.destroy()

        submit_button = tk.Button(
            contact_popup, text="Submit", command=add_selected_contact, font=("Arial", 12, "bold")
        )
        submit_button.pack(pady=10)

