import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import re
from db import update_products
class Change(tk.Frame):
    def __init__(self, master, account):
        super().__init__(master, width=400, height=500)
        self.master = master
        self.account = account
        self.file_name = None
        self.pack()
        master.geometry('400x500')
        master.title('変更')
        self.create_widgets()
    def create_widgets(self):
        self.return_button = tk.Button(self, text='×', command=self.return_event)
        self.return_button.place(x=30, y=30)
        self.label1 = tk.Label(self, text='変更したい商品のid')
        self.label1.place(x=150, y=30)
        self.id_entry = tk.Entry(self, width=50)
        self.id_entry.place(x=60, y=50)
        self.label2 = tk.Label(self, text='変更後の名前')
        self.label2.place(x=160, y=80)
        self.name_entry = tk.Entry(self, width=50)
        self.name_entry.place(x=60, y=100)
        self.label3 = tk.Label(self, text='変更後の価格')
        self.label3.place(x=160, y=130)
        self.price_entry = tk.Entry(self, width=50)
        self.price_entry.place(x=60, y=150)
        self.image_button = tk.Button(self, text='変更後の画像を選択する', command=self.image_event)
        self.image_button.place(x=130, y=180)
        self.change_button = tk.Button(self, text='商品詳細を変更する', command=self.change_event)
        self.change_button.place(x=140, y=230)
    def return_event(self):
        from app import Application
        self.destroy()
        Application(self.master, self.account)
    def image_event(self):
        file_type = [('画像ファイル', '*.jpg;*.ico;*.png')]
        self.file_name = filedialog.askopenfilename(filetypes=file_type)
    def change_event(self):
        id = self.id_entry.get()
        if len(id.strip()) <= 0:
            messagebox.showerror('変更', '変更したい商品のidを入力してください。')
            return
        if not re.match(r'^[0-9]+$', id):
            messagebox.showerror('変更', '半角数字で入力してください。')
            return
        id = int(id)
        name = self.name_entry.get()
        if len(name.strip()) <= 0:
            messagebox.showerror('変更', '変更後の商品名を入力してください。')
            return
        price = self.price_entry.get()
        if len(price.strip()) <= 0:
            messagebox.showerror('変更', '変更後の価格を入力してください。')
            return
        if not re.match(r'^[0-9]+$', price):
            messagebox.showerror('変更', '半角数字で入力してください。')
            return
        if self.file_name is None:
            messagebox.showerror('変更', '変更後の商品画像を選択してください。')
            return
        update_products(id, name, price, self.file_name)