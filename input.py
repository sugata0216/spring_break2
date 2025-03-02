import tkinter as tk
from tkinter import messagebox
from reset import Reset
class Input(tk.Frame):
    def __init__(self, master, email, code):
        super().__init__(master)
        self.master = master
        self.email = email
        self.code = code
        self.pack()
        master.geometry('400x500')
        master.title('入力')
        self.create_widgets()
    def create_widgets(self):
        self.label1 = tk.Label(self, text='送信された確認コードを入力してください。')
        self.label1.pack(pady=10)
        self.code_entry = tk.Entry(self, width=50)
        self.code_entry.pack(pady=10)
        self.confirmed_button = tk.Button(self, text='確定', command=self.confirmed_event)
        self.confirmed_button.pack()
    def confirmed_event(self):
        input_code = self.code_entry.get()
        if len(input_code.strip()) <= 0:
            messagebox.showerror('入力', '確認コードを入力してください。')
            return
        if self.code != input_code:
            messagebox.showerror('入力', '確認コードが間違っています。')
            return
        self.destroy()
        Reset(self.master, self.email)