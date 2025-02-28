import tkinter as tk
from db import select_order_details
from PIL import Image, ImageTk
class History(tk.Frame):
    def __init__(self, master, account):
        super().__init__(master, width=400, height=500)
        self.master = master
        self.account = account
        self.image_list = []
        self.pack()
        master.geometry('400x500')
        master.title('履歴')
        self.create_widgets()
    def create_widgets(self):
        self.return_button = tk.Button(self, text='<', command=self.return_event)
        self.return_button.place(x=30, y=30)
        self.label1 = tk.Label(self, text='ご注文', font=('', 20))
        self.label1.place(x=160, y=30)
        index = 0
        rows = select_order_details(self.account[0])
        for row in rows:
            img = Image.open(row[3])
            img = img.resize((50, 50))
            self.product_img = ImageTk.PhotoImage(img)
            self.image_list.append(self.product_img)
            self.label2 = tk.Label(self, image=self.product_img)
            self.label2.place(x=index * 50 + 30, y=80)
            index += 1
    def return_event(self):
        from app import Application
        self.destroy()
        Application(self.master, self.account)