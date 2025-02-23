import tkinter as tk
from tkinter import messagebox
from db import login
from app import Application
class Login(tk.Frame):
    def __init__(self, master):
        super().__init__(master, width=400, height=500)
        self.master = master
        self.pack()
        master.geometry('400x500')
        master.title('ログイン')
        self.create_widgets()
    def create_widgets(self):
        self.return_button = tk.Button(self, text='×', command=self.return_event)
        self.return_button.place(x=30, y=30)
        self.label1 = tk.Label(self, text='WEMU', fg='orange', font=('', 20))
        self.label1.place(x=170, y=30)
        self.label2 = tk.Label(self, text='JP')
        self.label2.place(x=250, y=50)
        self.label3 = tk.Label(self, text='メール', fg='gray')
        self.label3.place(x=30, y=100)
        self.email_entry = tk.Entry(self, width=50)
        self.email_entry.place(x=30, y=130)
        self.label4 = tk.Label(self, text='パスワード', fg='gray')
        self.label4.place(x=30, y=150)
        self.pw_entry = tk.Entry(self, show='●', width=50)
        self.pw_entry.place(x=30, y=180)
        self.continue_button = tk.Button(self, text='続ける', fg='white', bg='orange', command=self.continue_event)
        self.continue_button.place(x=190, y=230)
    def return_event(self):
        from boot import Boot
        self.destroy()
        Boot(self.master)
    def continue_event(self):
        email = self.email_entry.get()
        if len(email.strip()) <= 0:
            messagebox.showerror('メールアドレスの入力', 'メールアドレスを入力してください。')
        pw = self.pw_entry.get()
        if len(pw.strip()) <= 0:
            messagebox.showerror('パスワードの入力', 'パスワードを入力してください。')
        account = login(email, pw)
        if account is None:
            messagebox.showerror('ログイン', 'ログインに失敗しました。')
            return
        self.destroy()
        Application(self.master, account)
        