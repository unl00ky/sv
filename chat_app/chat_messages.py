import json
import tkinter as tk

CONNECTED_NAME = "Andrei"


class ChatMessages(tk.Frame):
    def __init__(self, master=None, discussion_list=None):
        super().__init__(master)
        master.grid(row=0, column=1, sticky="nsew")

        self.master = master
        self.chat_text = None
        self.message_entry = None
        self.send_button = None
        self.discussion_list = discussion_list

        self.placeholder = 'Type a message...'

        self.discussion_list.listbox_discussions.bind("<<TreeviewSelect>>", self.on_item_select)

        self.chat_messages = self.load_messages_list()

        self.create_widgets()

    def on_item_select(self, event):
        selected_index = self.discussion_list.listbox_discussions.selection()

        if selected_index:
            selected_item = self.discussion_list.listbox_discussions.selection()[0]
            selected_discussion = self.discussion_list.listbox_discussions.item(selected_item)

            contact_id = str(selected_discussion["values"][0])
            self.display_chat_messages(contact_id)

    def create_widgets(self):
        self.chat_text = tk.Text(self, height=10, width=40, bg="white", fg="black", font=("Arial", 12))
        self.chat_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.message_entry = tk.Text(self, height=2, width=5, bg="white", fg="black", font=("Arial", 12))
        self.message_entry.pack(fill=tk.BOTH, padx=10, pady=10)

        self.message_entry.bind("<Return>", self.send_message_event)

        self.message_entry.insert("1.0", self.placeholder)
        self.message_entry.config(fg="gray")
        self.message_entry.bind("<FocusIn>", self.on_message_focusin)
        self.message_entry.bind("<FocusOut>", self.on_message_focusout)

        self.send_button = tk.Button(
            self, text="Send Message", command=self.send_message, bg="blue", fg="white", font=("Arial", 12, "bold")
        )
        self.send_button.pack(fill=tk.NONE, side=tk.RIGHT, padx=10, pady=(10, 40))

    def send_message(self):
        selected_index = self.discussion_list.listbox_discussions.selection()

        if selected_index:
            selected_item = self.discussion_list.listbox_discussions.selection()[0]
            selected_discussion = self.discussion_list.listbox_discussions.item(selected_item)

            contact_id = str(selected_discussion["values"][0])
            message = self.message_entry.get("1.0", tk.END)

            message_obj = {
                "name": CONNECTED_NAME,
                "value": message
            }
            if contact_id in self.chat_messages:
                self.chat_messages[contact_id].append(
                    message_obj
                )
            else:
                self.chat_messages[contact_id] = [message_obj]

            self.display_new_chat_messages(message_obj)
            self.message_entry.delete('1.0', tk.END)

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

    def display_chat_messages(self, contact_id):
        self.chat_text.delete('1.0', tk.END)
        for message in self.chat_messages.get(contact_id, []):
            name = message["name"]
            value = message["value"]
            message_text = f"{name}: {value}\n\n"
            self.chat_text.insert(tk.END, message_text)

    def display_new_chat_messages(self, message):
        name = message["name"]
        value = message["value"]
        message_text = f"{name}: {value}\n"
        self.chat_text.insert(tk.END, message_text)

    @staticmethod
    def load_messages_list():
        with open("../chat_app/resources/messages.json", "r") as file:
            data = json.load(file)

        return data