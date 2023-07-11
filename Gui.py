import tkinter as tk
from DatabaseService import DatabaseService
from functools import partial


# password b'y4hCz3NXgj2NfCsEIPWYfh3p29x3d6GcZGuLftSeHl0='

class Gui:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Password Manager")
        self.database = DatabaseService()
        self.link = None
        self.page_login = None
        self.page_password = None
        self.loaded_passwords = None
        self.is_password_visible = False
        self.draw_components()
        self.window.mainloop()

    def draw_components(self):
        tk.Label(text="Page").grid(row=0, column=0, sticky="nw", padx=5, pady=5)
        self.link = tk.Entry(width=50)
        self.link.grid(row=1, column=0, padx=5, pady=5)

        tk.Label(text="Login").grid(row=2, column=0, sticky="nw", padx=5, pady=5)
        self.page_login = tk.Entry(width=50)
        self.page_login.grid(row=3, column=0, padx=5, pady=5)

        tk.Label(text="Password").grid(row=4, column=0, sticky="nw", padx=5, pady=5)
        self.page_password = tk.Entry(width=50, show='*')
        self.page_password.grid(row=5, column=0, padx=5, pady=5)

        submit_button = tk.Button(text="Submit", command=self.save_to_database)
        submit_button.grid(row=6, column=0, sticky="ne", padx=5, pady=5)

        tk.Label(text="Your passwords: ", anchor='w').grid(row=0, column=1, padx=5, pady=5)
        tk.Label(text="Link", anchor='w').grid(row=1, column=1, padx=5, pady=5)
        tk.Label(text="Login", anchor='w').grid(row=1, column=2, padx=5, pady=5)
        tk.Label(text="Password", anchor='w').grid(row=1, column=3, padx=5, pady=5)
        tk.Label(text="Created", anchor='w').grid(row=1, column=4, padx=5, pady=5)
        tk.Button(text="S", anchor='w', command=self.show_password).grid(row=1, column=5, padx=5, pady=5)

        for lp, item in enumerate(self.database.getAllResultsFromDatabase()):
            link = tk.StringVar(value=item[0])
            login = tk.StringVar(value=item[1])
            password = tk.StringVar(value=self.database.decryptPassword(item[2]).decode())
            creation_date = tk.StringVar(value=item[3][:10])
            tk.Entry(width=20, state='readonly', textvariable=link).grid(row=lp + 2, column=1, padx=5, pady=5)
            tk.Entry(width=15, state='readonly', textvariable=login).grid(row=lp + 2, column=2, padx=5, pady=5)
            if self.is_password_visible:
                tk.Entry(width=25, state='readonly', textvariable=password).grid(row=lp + 2, column=3, padx=5, pady=5)
            else:
                tk.Entry(width=25, state='readonly', textvariable=password, show='*').grid(row=lp + 2, column=3,
                                                                                           padx=5, pady=5)
            tk.Entry(width=10, state='readonly', textvariable=creation_date).grid(row=lp + 2, column=4, padx=5, pady=5)
            delete_button = tk.Button(text="D", command=partial(self.delete_from_database, item[3]))
            delete_button.grid(row=lp + 2, column=5, sticky="ne", padx=5, pady=5)

    def save_to_database(self):
        link, page_login, page_password = self.get_data_from_entries()
        self.database.createTableIfNotExists()
        self.database.addPasswordToDatabase(page_login, page_password, link)
        self.clear_entries()
        self.refresh_window()

    def delete_from_database(self, creation_date):
        self.database.removeResultFromDatabase(creation_date)
        self.refresh_window()

    def get_data_from_entries(self):
        link = self.link.get()
        page_login = self.page_login.get()
        page_password = self.page_password.get()
        return link, page_login, page_password

    def clear_entries(self):
        self.link.delete(0, tk.END)
        self.page_login.delete(0, tk.END)
        self.page_password.delete(0, tk.END)

    def refresh_window(self):
        widgets_list = self.window.grid_slaves()
        for widget in widgets_list:
            widget.destroy()
        self.draw_components()

    @staticmethod
    def resolve_date_string(long_date_format):
        year = long_date_format.strftime("%Y")
        month = long_date_format.strftime("%M")
        day = long_date_format.strftime("%d")
        return f'{year}-{month}-{day}'

    def show_password(self):
        if self.is_password_visible:
            self.is_password_visible = False
        else:
            self.is_password_visible = True
        self.refresh_window()
