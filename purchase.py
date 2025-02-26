import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from db import insert_orders, insert_order_details, select_orders
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
        self.product_list = []
        self.pack()
        master.geometry('400x500')
        master.title('購入')
        self.create_widgets()
    def create_widgets(self):
        self.return_button = tk.Button(self, text='<', command=self.return_event)
        self.return_button.place(x=30, y=30)
        self.label1 = tk.Label(self, text='注文確認')
        self.label1.place(x=180, y=30)
        self.label2 = tk.Label(self, text=f'商品の詳細({len(self.product_name_list)})')
        self.label2.place(x=30, y=80)
        if len(self.product_image_list) < 5:
            num = len(self.product_image_list)
        else:
            num = 4
        for i in range(num):
            img1 = Image.open(self.product_image_list[i])
            img1 = img1.resize((50, 50))
            product_img = ImageTk.PhotoImage(img1)
            self.image_list.append(product_img)
            self.product_image_label = tk.Label(self, image=product_img)
            self.product_image_label.place(x=i * 60 + 30, y=100)
            self.price_label = tk.Label(self, text=f'{self.product_price_list[i]}円', fg='orange')
            self.price_label.place(x=i * 60 + 30, y=150)
            self.product_list.append(self.product_price_list[i])
        self.minus_button1 = tk.Button(self, text='-', command=self.minus_event1, bg='gray')
        self.minus_button1.place(x=30, y=180)
        self.label3 = tk.Label(self, text=1)
        self.label3.place(x=50, y=180)
        self.plus_button1 = tk.Button(self, text='+', command=self.plus_event1, bg='gray')
        self.plus_button1.place(x=70, y=180)
        if num > 1:
            self.minus_button2 = tk.Button(self, text='-', bg='gray', command=self.minus_event2)
            self.minus_button2.place(x=90, y=180)
            self.label4 = tk.Label(self, text=1)
            self.label4.place(x=110, y=180)
            self.plus_button2 = tk.Button(self, text='+', bg='gray', command=self.plus_event2)
            self.plus_button2.place(x=130, y=180)
        if num > 2:
            self.minus_button3 = tk.Button(self, text='-', bg='gray', command=self.minus_event3)
            self.minus_button3.place(x=150, y=180)
            self.label5 = tk.Label(self, text=1)
            self.label5.place(x=170, y=180)
            self.plus_button3 = tk.Button(self, text='+', bg='gray', command=self.plus_event3)
            self.plus_button3.place(x=190, y=180)
        if num == 4:
            self.minus_button4 = tk.Button(self, text='-', bg='gray', command=self.minus_event4)
            self.minus_button4.place(x=210, y=180)
            self.label6 = tk.Label(self, text=1)
            self.label6.place(x=230, y=180)
            self.plus_button4 = tk.Button(self, text='-', bg='gray', command=self.plus_event4)
        self.label7 = tk.Label(self, text='総額')
        self.label7.place(x=30, y=400)
        self.label8 = tk.Label(self, text=sum(self.product_list), font=('', 13, 'bold'))
        self.label8.place(x=60, y=400)
        self.label9 = tk.Label(self, text='円', font=('', 8))
        self.label9.place(x=100, y=405)
        self.confirmed_button = tk.Button(self, text='注文を確定', fg='white', bg='orange', command=self.confirmed_event)
        self.confirmed_button.place(x=300, y=400)
    def return_event(self):
        from search import Search
        self.destroy()
        Search(self.master, self.account)
    def minus_event1(self):
        product_num1 = self.label3.cget('text')
        if product_num1 > 1:
            self.label3.configure(text=product_num1 - 1)
            self.product_list[0] -= self.product_price_list[0]
            self.label8.configure(text=sum(self.product_list))
        else:
            response = messagebox.askyesno('カートから削除', 'この商品をカートから削除しますか?')
            if response:
                self.label3.configure(text='×')
                self.minus_button1.configure(state='disabled')
                self.plus_button1.configure(state='disabled')
                self.product_list[0] = 0
                self.label8.configure(text=sum(self.product_list))
    def plus_event1(self):
        product_num1 = self.label3.cget('text')
        self.label3.configure(text=product_num1 + 1)
        self.product_list[0] += self.product_price_list[0]
        self.label8.configure(text=sum(self.product_list))
    def minus_event2(self):
        product_num2 = self.label4.cget('text')
        if product_num2 > 1:
            self.label4.configure(text=product_num2 - 1)
            self.product_list[1] -= self.product_price_list[1]
            self.label8.configure(text=sum(self.product_list))
        else:
            response = messagebox.askyesno('カートから削除', 'この商品をカートから削除しますか?')
            if response:
                self.label4.configure(text='×')
                self.minus_button2.configure(state='disabled')
                self.plus_button2.configure(state='disabled')
                self.product_list[1] = 0
                self.label8.configure(text=sum(self.product_list))
    def plus_event2(self):
        product_num2 = self.label4.cget('text')
        self.label4.configure(text=product_num2 + 1)
        self.product_list[1] += self.product_price_list[1]
        self.label8.configure(text=sum(self.product_list))
    def minus_event3(self):
        product_num3 = self.label5.cget('text')
        if product_num3 > 1:
            self.label5.configure(text=product_num3 - 1)
            self.product_list[2] -= self.product_price_list[2]
            self.label8.configure(text=sum(self.product_list))
        else:
            response = messagebox.askyesno('カートから削除', 'この商品をカートから削除しますか?')
            if response:
                self.label5.configure(text='×')
                self.minus_button3.configure(state='disabled')
                self.plus_button3.configure(state='disabled')
                self.product_list[2] = 0
                self.label8.configure(text=sum(self.product_list))
    def plus_event3(self):
        product_num3 = self.label5.cget('text')
        self.label5.configure(text=product_num3 + 1)
        self.product_list[2] += self.product_price_list[2]
        self.label8.configure(text=sum(self.product_list))
    def minus_event4(self):
        product_num4 = self.label6.cget('text')
        if product_num4 > 1:
            self.label6.configure(text=product_num4 - 1)
            self.product_list[3] -= self.product_price_list[3]
            self.label8.configure(text=sum(self.product_list))
        else:
            response = messagebox.askyesno('カートから削除', 'この商品をカートから削除しますか?')
            if response:
                self.label6.configure(text='×')
                self.minus_button4.configure(state='disabled')
                self.plus_button4.configure(state='disabled')
                self.product_list[3] = 0
                self.label8.configure(text=sum(self.product_list))
    def plus_event4(self):
        product_num4 = self.label6.cget('text')
        self.label6.configure(product_num4 + 1)
        self.product_list[3] += self.product_price_list[3]
        self.label8.configure(text=sum(self.product_list))
    def confirmed_event(self):
        insert_orders(self.account[0], sum(self.product_list))
        row = select_orders()
        for i in range(len(self.product_list)):
            if self.product_list[i] != 0:
                insert_order_details(row[0], self.product_id_list[i], self.product_list[i] // self.product_price_list[i], self.product_list[i])