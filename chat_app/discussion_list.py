import tkinter as tk
from tkinter import ttk
import asyncio

from chat_app.settings import USER_NAME
from client.contacts import get_contacts
from client.discussions import create_new_discussion, get_discussions


class DiscussionList(tk.Frame):
    def __init__(self, master=None, user_id=None):
        super().__init__(master)
        master.grid(row=0, column=0, sticky="ns")
        self.master = master

        self.listbox_discussions = None
        self.new_discussion_btn = None
        # self.config(bg="#121212")

        self.user_id = user_id
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self, text=f"{USER_NAME}", font=("Arial", 12, "bold"), pady=5, bg="#121212", fg="white")
        label.pack(fill=tk.X, padx=10, pady=(10, 0))

        self.new_discussion_btn = tk.Button(
            self, text="New Chat", command=self.open_contact_popup, font=("Arial", 12, "bold"), bg="#1D3461",
            fg="white", relief=tk.FLAT
        )
        self.new_discussion_btn.pack(fill=tk.X, padx=10, pady=10)

        self.listbox_discussions = ttk.Treeview(self, selectmode="browse", columns=2)
        self.listbox_discussions.heading("#0", text="Discussions")
        self.listbox_discussions.heading("#1", text="Status")
        self.listbox_discussions.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.load_discussions()

    def load_discussions(self):
        discussions = get_discussions(self.user_id)
        self.listbox_discussions.delete(*self.listbox_discussions.get_children())
        for discussion in discussions:
            status = discussion.get("status")
            if discussion.get("group_name"):
                self.listbox_discussions.insert('', 'end', text=discussion.get("group_name"),
                                                values=(status, discussion["id"]))
            else:
                self.listbox_discussions.insert('', 'end', text=discussion["name"], values=(status, discussion["id"]))

    def open_contact_popup(self):
        contact_popup = tk.Toplevel(self)
        contact_popup.title("Select a Contact")

        contact_listbox = ttk.Treeview(contact_popup, selectmode="extended")
        contact_listbox.heading("#0", text="Select a contact")

        contacts = get_contacts()
        for contact in contacts:
            contact_listbox.insert('', 'end', text=contact["name"], values=(contact["id"]))

        contact_listbox.pack(fill=tk.BOTH, padx=10, pady=10)

        def add_selected_contact():
            selected_contacts = []
            selected_names = []
            curr_items = contact_listbox.selection()

            if curr_items:
                for i in curr_items:
                    contacts_id = contact_listbox.item(i)["values"]
                    contacts_names = contact_listbox.item(i)["text"]
                    selected_contacts.extend(contacts_id)
                    selected_names.append(contacts_names)
                    # print(selected_contacts)
                    # print(selected_names)

                group_name = group_name_entry.get("1.0", "end-1c")

                create_new_discussion(self.user_id, selected_contacts, group_name)

                # self.load_discussions()
                contact_popup.destroy()

        group_name_label = tk.Label(contact_popup, text="Group name", font=("Arial", 12, "bold"))
        group_name_label.pack(fill=tk.X, padx=10)
        group_name_entry = tk.Text(contact_popup, height=1.2, width=5, bg="white", fg="black", font=("Arial", 12))
        group_name_entry.pack(fill=tk.X, padx=10, pady=10)

        submit_button = tk.Button(
            contact_popup, text="Submit", command=add_selected_contact, font=("Arial", 12, "bold"), bg="#1D3461",
            fg="white", relief="flat"
        )
        submit_button.pack(pady=10)
