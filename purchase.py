import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from db import insert_orders, insert_order_details, select_orders, update_point, get_account_by_email
import random
class Purchase(tk.Frame):
    def __init__(self, master, account, product_id_list, product_name_list, product_price_list, product_image_list):
        super().__init__(master, width=400, height=500)
        self.master = master
        self.account = account
        self.product_id_list = product_id_list
        self.product_name_list = product_name_list
        self.product_price_list = product_price_list
        self.product_image_list = product_image_list
        self.image_list = []
        self.quantities = [1] * len(product_id_list)
        self.current_page = 0
        self.items_per_page = 4
        self.pack()
        master.geometry('400x500')
        master.title('購入')
        self.create_widgets()
        self.update_page()
    def create_widgets(self):
        self.return_button = tk.Button(self, text='<', command=self.return_event)
        self.return_button.place(x=30, y=30)
        self.label1 = tk.Label(self, text='注文確認')
        self.label1.place(x=180, y=30)
        self.label2 = tk.Label(self, text=f'商品の詳細({len(self.product_name_list)})')
        self.label2.place(x=30, y=80)
        self.product_images = []
        self.price_labels = []
        self.quantity_labels = []
        self.minus_buttons = []
        self.plus_buttons = []
        for i in range(self.items_per_page):
            product_img_label = tk.Label(self)
            product_img_label.place(x=i * 60 + 30, y=100)
            self.product_images.append(product_img_label)
            price_label = tk.Label(self, fg='orange')
            price_label.place(x=i * 60 + 30, y=150)
            self.price_labels.append(price_label)
            minus_button = tk.Button(self, text='-', bg='gray', command=lambda idx=i: self.update_quantity(idx, -1))
            minus_button.place(x=i * 60 + 40, y=180)
            self.minus_buttons.append(minus_button)
            quantity_label = tk.Label(self, text="1")
            quantity_label.place(x=i * 60 + 60, y=180)
            self.quantity_labels.append(quantity_label)
            plus_button = tk.Button(self, text='+', bg='gray', command=lambda idx=i: self.update_quantity(idx, 1))
            plus_button.place(x=i * 60 + 80, y=180)
            self.plus_buttons.append(plus_button)
        self.prev_button = tk.Button(self, text='前へ', command=self.prev_page, state=tk.DISABLED)
        self.prev_button.place(x=100, y=350)
        self.next_button = tk.Button(self, text='次へ', command=self.next_page)
        self.next_button.place(x=250, y=350)
        self.label7 = tk.Label(self, text='総額')
        self.label7.place(x=30, y=400)
        self.label8 = tk.Label(self, text='0', font=('', 13, 'bold'))
        self.label8.place(x=60, y=400)
        self.label9 = tk.Label(self, text='円', font=('', 8))
        self.label9.place(x=130, y=405)
        self.confirmed_button = tk.Button(self, text='注文を確定', fg='white', bg='orange', command=self.confirmed_event)
        self.confirmed_button.place(x=300, y=400)
    def update_page(self):
        start_index = self.current_page * self.items_per_page
        end_index = start_index + self.items_per_page
        self.image_list.clear()
        for i in range(self.items_per_page):
            idx = start_index + i
            if idx < len(self.product_image_list):
                img = Image.open(self.product_image_list[idx])
                img = img.resize((50, 50))
                product_img = ImageTk.PhotoImage(img)
                self.image_list.append(product_img)
                self.product_images[i].config(image=product_img)
                self.price_labels[i].config(text=f'{self.product_price_list[idx]}円')
                self.quantity_labels[i].config(text=str(self.quantities[idx]))
                self.minus_buttons[i].config(state=tk.NORMAL)
                self.plus_buttons[i].config(state=tk.NORMAL)
            else:
                self.product_images[i].config(image=None)
                self.price_labels[i].config(text='')
                self.quantity_labels[i].config(text='')
                self.minus_buttons[i].config(state=tk.DISABLED)
                self.plus_buttons[i].config(state=tk.DISABLED)
        self.prev_button.config(state=tk.NORMAL if self.current_page > 0 else tk.DISABLED)
        self.next_button.config(state=tk.NORMAL if end_index < len(self.product_image_list) else tk.DISABLED)
        self.update_total_price()
    def update_quantity(self, button_index, change):
        product_index = self.current_page * self.items_per_page + button_index
        if 0 <= product_index < len(self.quantities):
            new_quantity = self.quantities[product_index] + change
            if new_quantity > 0:
                self.quantities[product_index] = new_quantity
                self.quantity_labels[button_index].config(text=str(new_quantity))
                self.update_total_price()
            else:
                response = messagebox.askyesno('カートから削除', 'この商品をカートから削除しますか?')
                if response:
                    self.quantities[product_index] = 0
                    self.quantity_labels[button_index].config(text="×")
                    self.minus_buttons[button_index].config(state=tk.DISABLED)
                    self.plus_buttons[button_index].config(state=tk.DISABLED)
                    self.update_total_price()
    def update_total_price(self):
        total_price = sum(self.product_price_list[i] * self.quantities[i] for i in range(len(self.product_price_list)))
        self.label8.config(text=f'{total_price}')
    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_page()
    def next_page(self):
        if (self.current_page + 1) * self.items_per_page < len(self.product_image_list):
            self.current_page += 1
            self.update_page()
    def return_event(self):
        from search import Search
        self.destroy()
        Search(self.master, self.account)
    def confirmed_event(self):
        total = sum(self.product_price_list[i] * self.quantities[i] for i in range(len(self.product_price_list)))
        insert_orders(self.account[0], total)
        row = select_orders()
        for i in range(len(self.product_id_list)):
            if self.quantities[i] > 0:
                insert_order_details(row[0], self.product_id_list[i], self.quantities[i], self.product_price_list[i] * self.quantities[i])
        if total >= 10000:
            point = random.choice([1, 2, 3, 5, 10, 100, 1000, 10000])
            new_point = self.account[6] + point
            update_point(new_point, self.account[0])
            self.account = get_account_by_email(self.account[4])