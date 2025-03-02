import tkinter as tk
from tkinter import messagebox
from db import select_users, send_mail
import random
from input import Input
class Forgot(tk.Frame):
    def __init__(self, master):
        super().__init__(master, width=400, height=500)
        self.master = master
        self.email_flg = False
        self.pack()
        master.geometry('400x500')
        master.title('PWリセット')
        self.create_widgets()
    def create_widgets(self):
        self.return_button = tk.Button(self, text='×', command=self.return_event)
        self.return_button.place(x=30, y=30)
        self.label1 = tk.Label(self, text='メールアドレス')
        self.label1.place(x=30, y=80)
        self.email_entry = tk.Entry(self, width=50)
        self.email_entry.place(x=30, y=100)
        self.send_button = tk.Button(self, text='送信', command=self.send_event)
        self.send_button.place(x=180, y=130)
    def return_event(self):
        from login import Login
        self.destroy()
        Login(self.master)
    def send_event(self):
        email = self.email_entry.get()
        if len(email.strip()) <= 0:
            messagebox.showerror('PWリセット', 'メールアドレスを入力してください。')
            return
        rows = select_users()
        for row in rows:
            if email == row[4]:
                self.email_flg = True
                break
        if not self.email_flg:
            messagebox.showerror('PWリセット', '入力されたメールアドレスは使われていません。')
            return
        code = ''
        random_source = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        for i in range(6):
            code += random.choice(random_source)
        to = email
        subject = 'PWリセット'
        body = f'確認コードは{code}です。'
        send_mail(to, subject, body)
        self.destroy()
        Input(self.master, email, code)
            