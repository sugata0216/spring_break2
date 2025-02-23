import tkinter as tk
from registration import Registration
from login import Login
class Boot(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()
        master.geometry('400x500')
        master.title('起動')
        self.create_widgets()
    def create_widgets(self):
        self.registration_button = tk.Button(self, text='登録', command=self.registration_event)
        self.registration_button.pack(pady=30)
        self.login_button = tk.Button(self, text='ログイン', command=self.login_event)
        self.login_button.pack()
    def registration_event(self):
        self.destroy()
        Registration(self.master)
    def login_event(self):
        self.destroy()
        Login(self.master)
if __name__ == '__main__':
    root = tk.Tk()
    app = Boot(master=root)
    app.mainloop()