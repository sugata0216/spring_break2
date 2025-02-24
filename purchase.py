import tkinter as tk
from PIL import Image, ImageTk
class Purchase(tk.Frame):
    def __init__(self, master, account, product_name_list, product_price_list, product_image_list):
        super().__init__(master, width=400, height=500)
        self.master = master
        self.account = account
        self.product_name_list = product_name_list
        self.product_price_list = product_price_list
        self.product_image_list = product_image_list
        self.image_list = []
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
        for i in range(4):
            img1 = Image.open(self.product_image_list[i])
            img1 = img1.resize((50, 50))
            product_img = ImageTk.PhotoImage(product_img)
            self.image_list.append(product_img)
            self.product_image_label = tk.Label(self, image=product_img)
    def return_event(self):
        from search import Search
        self.destroy()
        Search(self.master, self.account)