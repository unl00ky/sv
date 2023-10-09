import tkinter as tk


class ChatMessages(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        master.grid(row=0, column=1, sticky="nsew")

        self.master = master
        self.chat_text = None
        self.message_entry = None
        self.send_button = None
        self.create_widgets()

    def create_widgets(self):
        self.chat_text = tk.Text(self, height=10, width=40, bg="white", fg="black", font=("Arial", 12))
        self.chat_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.message_entry = tk.Entry(self, font=("Arial", 12))
        self.message_entry.pack(fill=tk.BOTH, padx=10, pady=10)

        self.send_button = tk.Button(
            self, text="Send Message", command=self.send_message, bg="blue", fg="white", font=("Arial", 12, "bold")
        )
        self.send_button.pack(fill=tk.NONE, side=tk.RIGHT, padx=10, pady=(10, 40))

    def send_message(self):
        pass
