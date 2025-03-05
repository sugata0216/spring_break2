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
        self.product_id_list = []
        self.products = []
        self.current_page = 0
        self.items_per_page = 4
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
        self.prev_button = tk.Button(self, text='前へ', command=self.prev_page, state=tk.DISABLED)
        self.prev_button.place(x=100, y=450)
        self.next_button = tk.Button(self, text='次へ', command=self.next_page, state=tk.DISABLED)
        self.next_button.place(x=250, y=450)
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
        self.products.clear()
        self.current_page = 0
        keyword = self.search_entry.get().strip()
        if not keyword:
            messagebox.showerror('検索', '検索欄を入力してください。')
            return
        self.products = select_products_by_keyword(keyword)
        if not self.products:
            messagebox.showinfo('検索', '該当する商品が見つかりませんでした。')
            return
        self.update_page()
    def update_page(self):
        for widget in self.widget_list:
            widget.destroy()
        self.widget_list.clear()
        start = self.current_page * self.items_per_page
        end = start + self.items_per_page
        display_items = self.products[start:end]
        y = 120
        for index, row in enumerate(display_items):
            img1 = Image.open(row[3])
            img1 = img1.resize((50, 50))
            product_img = ImageTk.PhotoImage(img1)
            product_image_label = tk.Label(self, image=product_img)
            product_image_label.image = product_img
            self.widget_list.append(product_image_label)
            product_name_label = tk.Label(self, text=row[1])
            self.widget_list.append(product_name_label)
            price_label = tk.Label(self, text=f'{row[2]}円', font=('', 9, 'bold'))
            self.widget_list.append(price_label)
            cart_label = tk.Label(self, image=self.cart_img)
            cart_label.bind('<Button-1>', lambda event, i=index + start: self.cart_event(i))
            self.widget_list.append(cart_label)
            if index % 2 == 0:
                x = 80
            else:
                x = 200
            product_image_label.place(x=x, y=y)
            product_name_label.place(x=x, y=y + 60)
            price_label.place(x=x, y=y + 80)
            cart_label.place(x=x + 50, y=y + 80)
            if index % 2 == 1:
                y += 130
        self.prev_button.config(state=tk.NORMAL if self.current_page > 0 else tk.DISABLED)
        self.next_button.config(state=tk.NORMAL if end < len(self.products) else tk.DISABLED)
    def next_page(self):
        if (self.current_page + 1) * self.items_per_page < len(self.products):
            self.current_page += 1
            self.update_page()
    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_page()
    def cart_event(self, index):
        product_data = self.products[index]
        if product_data[0] not in self.product_id_list:
            self.product_id_list.append(product_data[0])
            self.product_name_list.append(product_data[1])
            self.product_price_list.append(product_data[2])
            self.product_image_list.append(product_data[3])
            self.label2.configure(text=len(self.product_name_list), fg='white', bg='orange')
    def purchase_event(self):
        self.destroy()
        Purchase(self.master, self.account, self.product_id_list, self.product_name_list, self.product_price_list, self.product_image_list)