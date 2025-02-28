import tkinter as tk
from PIL import Image, ImageTk
from search import Search
from product_registration import ProductRegistration
from delete import Delete
from change import Change
from history import History
class Application(tk.Frame):
    def __init__(self, master, account):
        super().__init__(master, width=400, height=500)
        self.master = master
        self.account = account
        self.pack()
        master.geometry('400x500')
        master.title('ショッピングアプリ')
        self.create_widgets()
    def create_widgets(self):
        self.label1 = tk.Label(self, text='WEMU', fg='orange', bg='yellow', font=('', 20))
        self.label1.place(x=160, y=30)
        img1 = Image.open("img/lupe (1).png")
        search_img = ImageTk.PhotoImage(img1)
        self.search_label = tk.Label(self, image=search_img, bg='black')
        self.search_img = search_img
        self.search_label.bind('<Button-1>', self.search_event)
        self.search_label.place(x=170, y=80)
        self.order_button = tk.Button(self, text='ご注文', command=self.order_event)
        self.order_button.place(x=180, y=250)
        
        if self.account[5] == 1:
            self.registration_button = tk.Button(self, text='商品登録', command=self.registration_event)
            self.registration_button.place(x=170, y=150)
            self.delete_button = tk.Button(self, text='商品削除', command=self.delete_event)
            self.delete_button.place(x=170, y=180)
            self.change_button = tk.Button(self, text='商品詳細の変更', command=self.change_event)
            self.change_button.place(x=150, y=220)
    def search_event(self, event):
        self.destroy()
        Search(self.master, self.account)
    def registration_event(self):
        self.destroy()
        ProductRegistration(self.master, self.account)
    def delete_event(self):
        self.destroy()
        Delete(self.master, self.account)
    def change_event(self):
        self.destroy()
        Change(self.master, self.account)
    def order_event(self):
        self.destroy()
        History(self.master, self.account)