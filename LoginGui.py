import tkinter as tk
from Gui import Gui


class LoginGui:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Password Manager")
        self.window.geometry('335x200')
        self.user_password_entry = None
        self.user_password = None
        self.draw_components()
        self.window.mainloop()

    def draw_components(self):
        tk.Label(text="Enter Your database password").grid(row=0, column=0, padx=15, pady=15)
        self.user_password_entry = tk.Entry(width=50, show='*')
        self.user_password_entry.grid(row=1, column=0, padx=15, pady=15)
        tk.Button(text="Submit", anchor='w', command=self.submit_password).grid(row=2, column=0, padx=5, pady=5)

    def submit_password(self):
        self.user_password = self.user_password_entry.get()
        self.window.destroy()
        Gui()

