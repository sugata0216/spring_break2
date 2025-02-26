import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import re
from db import insert_products
class ProductRegistration(tk.Frame):
    def __init__(self, master, account):
        super().__init__(master)
        self.pack()
        master.geometry('400x500')
        master.title('商品登録')
        self.create_widgets()
    def create_widgets(self):
        self.label1 = tk.Label(self, text='商品名')
        self.label1.pack()
        self.name_entry = tk.Entry(self, width=50)
        self.name_entry.pack()
        self.label2 = tk.Label(self, text='価格')
        self.label2.pack()
        self.price_entry = tk.Entry(self, width=50)
        self.price_entry.pack()
        self.image_button = tk.Button(self, text='商品の画像を選択する', command=self.image_event)
        self.image_button.pack(pady=10)
        self.registration_button = tk.Button(self, text='商品を登録する', command=self.registration_event)
        self.registration_button.pack()
    def image_event(self):
        file_type = [('画像ファイル', '*.jpg;*.ico;*.png')]
        self.file_name = filedialog.askopenfilename(filetypes=file_type)
    def registration_event(self):
        name = self.name_entry.get()
        if len(name.strip()) <= 0:
            messagebox.showerror('商品名の入力', '商品名を入力してください。')
            return
        price = self.price_entry.get()
        if len(price.strip()) <= 0:
            messagebox.showerror('価格の入力', '価格を入力してください。')
            return
        if not re.match(r'^[0-9]+$', price):
            messagebox.showerror('価格の入力', '半角数字で入力してください。')
            return
        if self.file_name == None:
            messagebox.showerror('商品の画像', '商品の画像を選択してください。')
            return
        insert_products(name, price, self.file_name)