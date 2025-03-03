import tkinter as tk
from db import select_order_details
from PIL import Image, ImageTk
class History(tk.Frame):
    def __init__(self, master, account):
        super().__init__(master, width=400, height=500)
        self.master = master
        self.account = account
        self.image_list = []
        self.current_images = []
        self.page = 0
        self.items_per_page = 4
        self.pack()
        master.geometry('400x500')
        master.title('履歴')
        self.rows = select_order_details(self.account[0])
        self.create_widgets()
        self.update_display()
    def create_widgets(self):
        self.return_button = tk.Button(self, text='<', command=self.return_event)
        self.return_button.place(x=30, y=30)
        self.label1 = tk.Label(self, text='ご注文', font=('', 20))
        self.label1.place(x=160, y=30)
        self.prev_button = tk.Button(self, text='前へ', command=self.prev_page)
        self.prev_button.place(x=100, y=450)
        self.next_button = tk.Button(self, text='次へ', command=self.next_page)
        self.next_button.place(x=250, y=450)
    def update_display(self):
        for label in self.current_images:
            label.destroy()
        self.current_images.clear()
        start = self.page * self.items_per_page
        end = start + self.items_per_page
        rows_to_display = self.rows[start:end]
        for index, row in enumerate(rows_to_display):
            img = Image.open(row[3])
            img = img.resize((50, 50))
            product_img = ImageTk.PhotoImage(img)
            self.image_list.append(product_img)
            label = tk.Label(self, image=product_img)
            label.place(x=index * 100 + 30, y=80)
            self.current_images.append(label)
        self.prev_button.config(state=tk.NORMAL if self.page > 0 else tk.DISABLED)
        self.next_button.config(state=tk.NORMAL if end < len(self.rows) else tk.DISABLED)
    def next_page(self):
        if (self.page + 1) * self.items_per_page < len(self.rows):
            self.page += 1
            self.update_display()
    def prev_page(self):
        if self.page > 0:
            self.page -= 1
            self.update_display()
    def return_event(self):
        from app import Application
        self.destroy()
        Application(self.master, self.account)
