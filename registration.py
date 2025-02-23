import tkinter as tk
from tkinter import messagebox
from db import select_users, insert_user
class Registration(tk.Frame):
    def __init__(self, master):
        super().__init__(master, width=400, height=500)
        self.master = master
        self.pack()
        master.geometry('400x500')
        master.title('登録')
        self.create_widgets()
    def create_widgets(self):
        self.return_button = tk.Button(self, text='< 戻る', command=self.return_event)
        self.return_button.place(x=30, y=30)
        self.label1 = tk.Label(self, text='登録', font=('', 20, 'bold'))
        self.label1.place(x=180, y=50)
        self.label2 = tk.Label(self, text='お客様のアカウントを作成する',font=('', 9, 'bold'))
        self.label2.place(x=50, y=100)
        self.label3 = tk.Label(self, text='登録は簡単で、パスワードを入力するだけです。')
        self.label3.place(x=50, y=130)
        self.label4 = tk.Label(self, text='メール', font=('', 9, 'bold'))
        self.label4.place(x=50, y=180)
        self.email_entry = tk.Entry(self, width=50)
        self.email_entry.place(x=50, y=200)
        self.label5 = tk.Label(self, text='パスワード', font=('', 9, 'bold'))
        self.label5.place(x=50, y=230)
        self.pw_entry = tk.Entry(self, show='●', width=50)
        self.pw_entry.place(x=50, y=250)
        self.label6 = tk.Label(self, text='パスワードは最低8文字が必要です。\n別のサイトのパスワードや、ペットの名前などの明白すぎるパスワードを\n使用しないでください。', fg='gray')
        self.label6.place(x=50, y=280)
        self.label7 = tk.Label(self, text='名前', font=('', 9, 'bold'))
        self.label7.place(x=50, y=330)
        self.name_entry = tk.Entry(self, width=50)
        self.name_entry.place(x=50, y=350)
        self.registration_button = tk.Button(self, text='登録', fg='white', bg='orange', command=self.registration_event)
        self.registration_button.place(x=190, y=380)
    def return_event(self):
        from boot import Boot
        self.destroy()
        Boot(self.master)
    def registration_event(self):
        email = self.email_entry.get()
        if len(email.strip()) <= 0:
            messagebox.showerror('メールアドレスの入力', 'メールアドレスを入力してください。')
            return
        rows = select_users()
        for row in rows:
            if email == row[3]:
                messagebox.showerror('メールアドレスの入力', 'すでに使われているメールアドレスです。')
                break
        pw = self.pw_entry.get()
        if len(pw.strip()) <= 0:
            messagebox.showerror('パスワードの入力', 'パスワードを入力してください。')
            return
        if len(pw) < 8:
            messagebox.showerror('パスワードの入力', 'パスワードは8文字以上でお願いします。')
            return
        name = self.name_entry.get()
        if len(name.strip()) <= 0:
            messagebox.showerror('名前の入力', '名前を入力してください。')
            return
        for row in rows:
            if name == row[1]:
                messagebox.showerror('名前の入力', 'すでに使われている名前です。')
                break
        insert_user(name, pw, email)
        from boot import Boot
        self.destroy()
        Boot(self.master) 