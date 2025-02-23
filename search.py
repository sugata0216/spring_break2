import tkinter as tk
from db import select_products_by_keyword
from tkinter import messagebox
from PIL import Image, ImageTk
class Search(tk.Frame):
    def __init__(self, master, account):
        super().__init__(master, width=400, height=500)
        self.master = master
        self.account = account
        self.image_list = []
        self.cart_list = []
        self.pack()
        master.geometry('400x500')
        master.title('検索')
        self.create_widgets()
    def create_widgets(self):
        self.label1 = tk.Label(self, text='WEMU', fg='orange', bg='yellow', font=('', 20))
        self.label1.place(x=160, y=30)
        self.return_button = tk.Button(self, text='<', command=self.return_event)
        self.return_button.place(x=30, y=80)
        self.search_entry = tk.Entry(self, width=25)
        self.search_entry.place(x=120, y=80)
        self.delete_button = tk.Button(self, text='×', fg='white', bg='gray', command=self.delete_event)
        self.delete_button.place(x=280, y=80)
        self.search_button = tk.Button(self, text='検索', command=self.search_event)
        self.search_button.place(x=330, y=80)
        cimg = Image.open("img/illustkun-05776-shopping-cart (1).png")
    def return_event(self):
        from app import Application
        self.destroy()
        Application(self.master, self.account)
    def delete_event(self):
        self.search_entry.delete(0, tk.END)
    def search_event(self):
        index = 0
        keyword = self.search_entry.get()
        if len(keyword.strip()) <= 0:
            messagebox.showerror('検索', '検索欄を入力してください。')
            return
        rows = select_products_by_keyword(keyword)
        for row in rows:
            img1 = Image.open(row[3])
            product_img = ImageTk.PhotoImage(img)
            self.product_image_label = tk.Label(self, image=product_img)
            self.product_img = product_img
            self.image_list.append(self.product_img)
            self.product_name_label = tk.Label(self, text=row[1])
            self.price_label = tk.Label(self, text=f'{row[2]}円')
            img2 = 
            if index % 2 == 0:
                