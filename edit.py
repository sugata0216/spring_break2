import tkinter as tk
from tkinter import messagebox
from db import update_users, get_account_by_email
class Edit(tk.Frame):
    def __init__(self, master, account):
        super().__init__(master, width=400, height=500)
        self.master = master
        self.account = account
        self.pack()
        master.geometry('400x500')
        master.title('編集')
        self.create_widgets()
    def create_widgets(self):
        self.return_button = tk.Button(self, text='×', command=self.return_event)
        self.return_button.place(x=30, y=30)
        self.label1 = tk.Label(self, text='変更後のユーザー名')
        self.label1.place(x=150, y=30)
        self.name_entry = tk.Entry(self, width=50)
        self.name_entry.place(x=40, y=80)
        self.edit_button = tk.Button(self, text='編集', command=self.edit_event)
        self.edit_button.place(x=180, y=130)
    def edit_event(self):
        name = self.name_entry.get()
        if len(name.strip()) <= 0:
            messagebox.showerror('編集', '変更後のユーザー名を入力してください。')
            return
        update_users(self.account[0], name)
        self.account = get_account_by_email(self.account[4])
    def return_event(self):
        from app import Application
        self.destroy()
        Application(self.master, self.account)