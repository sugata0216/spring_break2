import tkinter as tk
from tkinter import messagebox
from db import insert_user, send_mail
class Confirmation(tk.Frame):
    def __init__(self, master, email, pw, name, authority, code):
        super().__init__(master)
        self.master = master
        self.email = email
        self.pw = pw
        self.name = name
        self.authority = authority
        self.code = code
        self.pack()
        master.geometry('400x500')
        master.title('確認')
        self.create_widgets()
    def create_widgets(self):
        self.label1 = tk.Label(self, text='入力されたメールアドレスに送信された確認コードを入力してください。')
        self.label1.pack(pady=10)
        self.code_entry = tk.Entry(self, width=50)
        self.code_entry.pack(pady=10)
        self.certification_button = tk.Button(self, text='認証', command=self.certification_event)
        self.certification_button.pack()
    def certification_event(self):
        input_code = self.code_entry.get()
        if len(input_code.strip()) <= 0:
            messagebox.showerror('確認', '確認コードを入力してください。')
            return
        if self.code != input_code:
            messagebox.showerror('確認', '確認コードが間違っています。')
            return
        insert_user(self.name, self.pw, self.email, self.authority)
        to = self.email
        subject = 'ユーザ登録時の登録完了メール'
        body = 'ユーザ登録が完了しました。'
        send_mail(to, subject, body)
        from boot import Boot
        self.destroy()
        Boot(self.master) 