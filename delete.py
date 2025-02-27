import tkinter as tk
from db import select_products, delete_products, delete_order_details
from tkinter import messagebox
import re
class Delete(tk.Frame):
    def __init__(self, master, account):
        super().__init__(master, width=400, height=500)
        self.master = master
        self.account = account
        self.pack()
        master.geometry('400x500')
        master.title('削除')
        self.create_widgets()
    def create_widgets(self):
        self.return_button = tk.Button(self, text='×', command=self.return_event)
        self.return_button.place(x=30, y=30)
        self.label1 = tk.Label(self, text='削除したい商品のid')
        self.label1.place(x=150, y=30)
        self.id_entry = tk.Entry(self, width=50)
        self.id_entry.place(x=60, y=50)
        self.delete_button = tk.Button(self, text='削除', command=self.delete_event)
        self.delete_button.place(x=180, y=80)
    def return_event(self):
        from app import Application
        self.destroy()
        Application(self.master, self.account)
    def delete_event(self):
        id_flg = False
        id = self.id_entry.get()
        if len(id.strip()) <= 0:
            messagebox.showerror('削除', '削除したい商品のidを入力してください。')
            return
        if not re.match(r'^[0-9]+$', id):
            messagebox.showerror('削除', 'idは半角数字で入力してください。')
            return
        id = int(id)
        rows = select_products()
        for row in rows:
            if id == row[0]:
                id_flg = True
                break
        if not id_flg:
            messagebox.showerror('削除', '入力された商品のidは見つかりませんでした。')
            return
        delete_order_details(id)
        delete_products(id)
        