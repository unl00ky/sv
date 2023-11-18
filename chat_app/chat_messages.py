import asyncio
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import websockets

from client.messages import get_messages, create_new_message
from client.contacts import get_contacts
from client.discussions import update_discussion
from chat_app.settings import DOMAIN, PORT, USER_NAME


class ChatMessages(tk.Frame):
    def __init__(self, master=None, discussion_list=None, user_id=None):
        super().__init__(master)
        # self.config(bg="#121212")
        master.grid(row=0, column=1, sticky="nsew")

        self.master = master
        self.user_id = user_id
        self.chat_text = None
        self.message_entry = None
        self.send_button = None
        self.discussion_id = None
        self.add_contact_btn = None
        self.discussion_list = discussion_list

        self.placeholder = 'Type a message...'

        self.discussion_list.listbox_discussions.bind("<<TreeviewSelect>>", self.on_item_select)
        # self.messages = []
        self.websocket = None
        self.create_widgets()

    async def connect_to_websocket_server_recv(self):
        await asyncio.sleep(2)
        try:
            async with websockets.connect(f"ws://{DOMAIN}:{PORT}/ws/{USER_NAME}") as websocket:
                self.websocket = websocket
                while True:

                    response = await websocket.recv()
                    if response == "discussion":
                        self.discussion_list.load_discussions()
                    elif response == "New message":
                        self.on_item_select(response)

        except websockets.ConnectionClosed:
            messagebox.showerror("API error message", "Connection closed.")
        except Exception as e:
            messagebox.showerror("API error message", f"Error: {str(e)}")

    def on_item_select(self, event):
        selected_index = self.discussion_list.listbox_discussions.selection()

        if selected_index:
            selected_item = self.discussion_list.listbox_discussions.selection()[0]
            selected_discussion = self.discussion_list.listbox_discussions.item(selected_item)

            self.discussion_id = str(selected_discussion["values"][0])

            # Get message to API.
            messages = get_messages(self.discussion_list.user_id, self.discussion_id)
            self.display_chat_messages(messages)

    def create_widgets(self):
        self.chat_text = tk.Text(self, height=10, width=40, font=("Arial", 12))
        self.chat_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.message_entry = tk.Text(self, height=2, width=5, bg="white", fg="black", font=("Arial", 12))
        self.message_entry.pack(fill=tk.BOTH, padx=10, pady=10)
        self.message_entry.bind("<Return>", self.send_message_event)

        self.message_entry.insert("1.0", self.placeholder)
        self.message_entry.config(fg="gray")
        self.message_entry.bind("<FocusIn>", self.on_message_focusin)
        self.message_entry.bind("<FocusOut>", self.on_message_focusout)

        self.add_contact_btn = tk.Button(self, text="+", command=self.add_contact_popup,
                                         font=("Arial", 12, "bold"), bg="#1D3461", fg="white",
                                         relief=tk.FLAT
                                         )
        self.add_contact_btn.pack(side=tk.LEFT, padx=10, pady=(10, 40))
        self.send_button = tk.Button(
            self, text="Send Message", command=self.send_message, font=("Arial", 12, "bold"), bg="#1D3461", fg="white",
            relief=tk.FLAT
        )
        self.send_button.pack(fill=tk.NONE, side=tk.RIGHT, padx=10, pady=(10, 40))

    def add_contact_popup(self):
        selected_index = self.discussion_list.listbox_discussions.selection()
        if not selected_index:
            return messagebox.showerror("Error", "Please select a discussion")

        add_contact_popup = tk.Toplevel(self)
        add_contact_popup.title("Select a contact")

        contacts_listbox = ttk.Treeview(add_contact_popup, selectmode="extended")
        contacts_listbox.heading("#0", text="Select a contact")
        contacts = get_contacts()
        for contact in contacts:
            contacts_listbox.insert("", "end", text=contact["name"], values=contact["id"])
        contacts_listbox.pack(padx=10, pady=10)

        def add_contacts():
            selected_contacts = []
            curr_items = contacts_listbox.selection()
            if curr_items:
                for i in curr_items:
                    contacts_id = contacts_listbox.item(i)["values"]
                    selected_contacts.extend(contacts_id)

                update_discussion(self.user_id, selected_contacts, self.discussion_id)
                asyncio.get_event_loop().run_until_complete(self.websocket.send("discussion"))
                add_contact_popup.destroy()

        submit_button = tk.Button(
            add_contact_popup, text="Submit", command=add_contacts, font=("Arial", 12, "bold"), bg="#1D3461",
            fg="white",
            relief="flat"
        )
        submit_button.pack(pady=10)

    def send_message(self):
        selected_index = self.discussion_list.listbox_discussions.selection()

        if selected_index:
            selected_item = self.discussion_list.listbox_discussions.selection()[0]
            selected_discussion = self.discussion_list.listbox_discussions.item(selected_item)

            discussion_id = str(selected_discussion["values"][0])
            message = self.message_entry.get("1.0", tk.END)

            message_obj = {
                "discussion_id": discussion_id,
                "user_id": self.discussion_list.user_id,
                "value": message
            }

            # self.messages.append(message_obj)
            # self.create_new_chat_messages(message_obj)
            create_new_message(message_obj)
            asyncio.get_event_loop().run_until_complete(self.websocket.send("New message"))
            self.message_entry.delete('1.0', tk.END)
            return 'break'

    def on_message_focusin(self, event):
        if self.message_entry.get("1.0", "end-1c") == self.placeholder:
            self.message_entry.delete("1.0", tk.END)
            self.message_entry.config(fg="black")

    def on_message_focusout(self, event):
        if not self.message_entry.get("1.0", "end-1c"):
            self.message_entry.insert("1.0", self.placeholder)
            self.message_entry.config(fg="gray")

    def send_message_event(self, event):
        self.send_message()

    def display_chat_messages(self, messages):
        self.chat_text.delete('1.0', tk.END)
        for message in messages:
            name = message["name"]
            value = message["value"]
            time = message.get("date")
            message_text = f"{time} | {name}: {value}\n"
            self.chat_text.insert(tk.END, message_text)

    # def create_new_chat_messages(self, message):
    #     create_new_message(message)
