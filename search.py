import tkinter as tk
from db import select_products_by_keyword
from tkinter import messagebox
from PIL import Image, ImageTk
from purchase import Purchase
class Search(tk.Frame):
    def __init__(self, master, account):
        super().__init__(master, width=400, height=500)
        self.master = master
        self.account = account
        self.image_list = []
        self.cart_list = []
        self.cart_label_list = []
        self.widget_list = []
        self.product_name_list = []
        self.product_price_list = []
        self.product_image_list = []
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
        cart_img = ImageTk.PhotoImage(cimg)
        self.cart_img = cart_img
        self.label2 = tk.Label(self, text='')
        self.label2.place(x=300, y=400)
        self.cart_button = tk.Button(self, text='カート', fg='green', command=self.purchase_event)
        self.cart_button.place(x=270, y=420)
    def return_event(self):
        from app import Application
        self.destroy()
        Application(self.master, self.account)
    def delete_event(self):
        self.search_entry.delete(0, tk.END)
    def search_event(self):
        for widget in self.widget_list:
            widget.destroy()
        self.image_list.clear()
        self.cart_list.clear()
        self.cart_label_list.clear()
        self.widget_list.clear()
        index = 0
        y = 0
        keyword = self.search_entry.get()
        if len(keyword.strip()) <= 0:
            messagebox.showerror('検索', '検索欄を入力してください。')
            return
        rows = select_products_by_keyword(keyword)
        for row in rows:
            img1 = Image.open(row[3])
            img1 = img1.resize((50, 50))
            product_img = ImageTk.PhotoImage(img1)
            self.product_image_label = tk.Label(self, image=product_img)
            self.widget_list.append(self.product_image_label)
            self.product_img = product_img
            self.image_list.append(self.product_img)
            self.product_name_label = tk.Label(self, text=row[1])
            self.widget_list.append(self.product_name_label)
            self.price_label = tk.Label(self, text=f'{row[2]}円', font=('', 9, 'bold'))
            self.widget_list.append(self.price_label)
            self.cart_label = tk.Label(self, image=self.cart_img)
            self.cart_label.bind('<Button-1>', lambda event, i = index: self.cart_event(i, rows))
            self.cart_list.append(self.cart_label)
            self.widget_list.append(self.cart_label)
            if index % 2 == 0:
                self.product_image_label.place(x=80, y=y * 130 + 130)
                self.product_name_label.place(x=80, y=y * 180 + 180)
                self.price_label.place(x=80, y=y * 200 + 200)
                self.cart_label.place(x=130, y=y * 200 + 200)
                y += 1
            elif index % 2 == 1:
                self.product_image_label.place(x=180, y=y * 130 + 130)
                self.product_name_label.place(x=180, y=y * 180 + 180)
                self.price_label.place(x=180, y=y * 200 + 200)
                self.cart_label.place(x=230, y=y * 200 + 200)
                y += 1
                index += 1
    def cart_event(self, index, rows):
        product_data = rows[index]
        self.product_name_list.append(product_data[1])
        self.product_price_list.append(product_data[2])
        self.product_image_list.append(product_data[3])
        # print(self.product_list)
        self.label2.configure(text=len(self.product_name_list), fg='white', bg='orange')
    def purchase_event(self):
        self.destroy()
        Purchase(self.master, self.account, self.product_name_list, self.product_price_list, self.product_image_list)