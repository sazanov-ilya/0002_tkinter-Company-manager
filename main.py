import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
# import tkinter.ttk as ttk
# import sqlite3

# импортируем свои модули
import db_sqlite3 as db
import companies as companies
import connection_types as connection_types
import connections as connections
import logins as logins


# # закрываем на крестик
# def on_closing():
#    if mb.askokcancel("Выход из приложения", "Хотите выйти из приложения?"):
#        root.destroy()


# класс основной формы
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)

        self.init_main()
        self.db = db  # Передаем класс DB
        self.clear_frm_content_all()

    def init_main(self):
        # стили
        self.style = ttk.Style()
        self.style.theme_use("default")

        # главная рамка
        # поле для ввода данных растянуто горизонтально с параметрами fill и expand
        self.pack(fill=tk.BOTH, expand=True)

        # рамка для toolbar главного окна
        frm_main_toolbar = ttk.Frame(self, relief=tk.RAISED, borderwidth=3)  # GROOVE
        frm_main_toolbar.pack(fill=tk.X)

        # кнопки меню с картинками
        # 1
        self.company_img = tk.PhotoImage(file='new_company.gif')
        btn_open_company = tk.Button(frm_main_toolbar, text='Компании', bg='#d7d8e0', bd=1, pady=1, padx=6,
                                     compound=tk.BOTTOM, image=self.company_img, command=self.open_companies)
        btn_open_company.pack(side=tk.LEFT)

        # 2
        self.connections_img = tk.PhotoImage(file='new_company.gif')
        btn_open_connections = tk.Button(frm_main_toolbar, text='Типы доступов', bg='#d7d8e0', bd=1, pady=1, padx=6,
                                         compound=tk.BOTTOM, image=self.company_img, command=self.open_connection_types)
        btn_open_connections.pack(side=tk.LEFT)

        # 3
        self.connections_img = tk.PhotoImage(file='new_company.gif')
        btn_open_connections = tk.Button(frm_main_toolbar, text='Доступы', bg='#d7d8e0', bd=1, pady=1, padx=6,
                                         compound=tk.BOTTOM, image=self.company_img, command=self.open_connections)
        btn_open_connections.pack(side=tk.LEFT)

        ## 4
        #self.frm_content_all_clear_img = tk.PhotoImage(file='new_company.gif')
        #btn_content_all_clear = tk.Button(frm_main_toolbar, text='Тест очистки контента', bg='#d7d8e0', bd=0,
        #                                  compound=tk.BOTTOM,
        #                                  image=self.frm_content_all_clear_img, command=self.clear_frm_content_all)
        #btn_content_all_clear.pack(side=tk.LEFT)

        #self.frm_content_all_logins_img = tk.PhotoImage(file='new_company.gif')
        #btn_content_all_logins = tk.Button(frm_main_toolbar, text='Тест логины', bg='#d7d8e0', bd=1,
        #                                   compound=tk.BOTTOM,
        #                                   image=self.frm_content_all_logins_img, command=self.open_logins)
        #btn_content_all_logins.pack(side=tk.LEFT)

        # рамка контента главного окна
        self.frm_content_all = ttk.Frame(self, relief=tk.RAISED, borderwidth=3)
        self.frm_content_all.pack(fill=tk.BOTH, anchor=tk.N, expand=True)

    ## работает 1
    # def content_all_clear(self):
    #    self.frm_content_all.pack_forget()

    # работает 2
    def clear_frm_content_all(self):
        for widget in self.frm_content_all.winfo_children():
            # widget.pack_forget()
            widget.destroy()

    def open_logins(self):
        # self.pack(fill=tk.BOTH, expand=True)
        self.clear_frm_content_all()
        id_connection = 4
        self.logins = logins.Logins(self.frm_content_all, app, id_connection)

    def open_companies(self):
        # self.pack(fill=tk.BOTH, expand=True)
        self.clear_frm_content_all()
        # companies.Companies(self.frm_content_all)
        self.companies = companies.Companies(self.frm_content_all, app)

    def open_connection_types(self):
        # self.pack(fill=tk.BOTH, expand=True)
        self.clear_frm_content_all()
        # Companies()
        self.connection_types = connection_types.ConnectionTypes(self.frm_content_all, app)

    def open_connections(self):
        # self.pack(fill=tk.BOTH, expand=True)
        self.clear_frm_content_all()
        # Companies()
        self.connections = connections.Connections(self.frm_content_all, app)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    root = tk.Tk()

    # # закрываем на крестик
    # root.protocol("WM_DELETE_WINDOW", on_closing)  # клик по крестику

    db = db.DB()  # Добавляем класс DB
    app = Main(root)  # добавляем класс Main

    app.pack()
    root.title("База списка подключений")
    root.geometry("700x450+300+200")
    # root.resizable(False, False)

    # отключил 20210807 (не помню для чего)
    #root.event_add('<<Paste>>', '<Control-igrave>')
    #root.event_add("<<Copy>>", "<Control-ntilde>")

    root.mainloop()