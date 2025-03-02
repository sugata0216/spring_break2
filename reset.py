import tkinter as tk
from tkinter import messagebox
from db import update_pw
class Reset(tk.Frame):
    def __init__(self, master, email):
        super().__init__(master)
        self.master = master
        self.email = email
        self.pack()
        master.geometry('400x500')
        master.title('リセット')
        self.create_widgets()
    def create_widgets(self):
        self.label1 = tk.Label(self, text='新しいパスワードを8文字以上でお願いします。')
        self.label1.pack(pady=10)
        self.pw_entry = tk.Entry(self, width=50, show='●')
        self.pw_entry.pack(pady=10)
        self.update_button = tk.Button(self, text='更新', command=self.update_event)
        self.update_button.pack()
    def update_event(self):
        pw = self.pw_entry.get()
        if len(pw.strip()) <= 0:
            messagebox.showerror('リセット', '新しいパスワードを入力してください。')
            return
        if len(pw) < 8:
            messagebox.showerror('リセット', 'パスワードは8文字以上でお願いします。')
            return
        update_pw(self.email, pw)
        from login import Login
        self.destroy()
        Login(self.master)
        