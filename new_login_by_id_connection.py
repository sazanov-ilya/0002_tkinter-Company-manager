import ctypes
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
# import re

# импортируем свои модули
import __general_procedures as gp
import logins as logins



class NewLoginByIdConnection(tk.Toplevel):
    """ Класс формы добавления логина по id_connection """
    def __init__(self, app, parent, id_connection):
        super().__init__()
        # self.geometry("500x300+300+200")

        self.init_new_login_by_id_connection()
        self.app = app  # Передаем класс Main
        self.parent = parent  # класс Logins
        self.id_connection = id_connection

    def init_new_login_by_id_connection(self):
        self.title("Добавить новый логин")
        # self.style = ttk.Style()
        # self.style.theme_use("default")

        # Добавляем функции модального, прехватываем фокус до закрытия
        self.grab_set()
        self.focus_set()

        # базовая рамка для модуля
        frm_new_login = ttk.Frame(self, relief=tk.RAISED, borderwidth=0)
        frm_new_login.pack(fill=tk.BOTH, expand=True)

        frm_new_login_name = ttk.Frame(frm_new_login, relief=tk.RAISED, borderwidth=0)
        frm_new_login_name.pack(fill=tk.X)
        lbl_new_login_name = ttk.Label(frm_new_login_name, text="Логин", width=10)
        lbl_new_login_name.pack(side=tk.LEFT, padx=5, pady=5)
        self.ent_new_login_name = ttk.Entry(frm_new_login_name)
        self.ent_new_login_name.pack(fill=tk.X, padx=5, expand=True)
        self.ent_new_login_name.bind("<Control-KeyPress>", gp.keys)

        frm_new_login_password = ttk.Frame(frm_new_login, relief=tk.RAISED, borderwidth=0)
        frm_new_login_password.pack(fill=tk.X)
        lbl_new_login_password = ttk.Label(frm_new_login_password, text="Пароль", width=10)
        lbl_new_login_password.pack(side=tk.LEFT, padx=5, pady=5)
        self.ent_new_login_password = ttk.Entry(frm_new_login_password)
        self.ent_new_login_password.pack(fill=tk.X, padx=5, expand=True)
        self.ent_new_login_password.bind("<Control-KeyPress>", gp.keys)

        # На все свободное место
        self.frm_new_login_description = ttk.Frame(frm_new_login, relief=tk.RAISED, borderwidth=0)
        self.frm_new_login_description.pack(fill=tk.BOTH, expand=True)
        lbl_new_login_description = ttk.Label(self.frm_new_login_description, text="Описание", width=10)
        lbl_new_login_description.pack(side=tk.LEFT, anchor=tk.N, padx=5, pady=5)
        self.txt_new_login_description = tk.Text(self.frm_new_login_description)
        self.txt_new_login_description.pack(fill=tk.BOTH, pady=5, padx=5, expand=True)
        self.txt_new_login_description.bind("<Control-KeyPress>", gp.keys)

        # Рамка для кнопок
        self.frm_new_login_btn = ttk.Frame(frm_new_login, relief=tk.RAISED, borderwidth=0)
        self.frm_new_login_btn.pack(fill=tk.X)

        self.btn_new_login_cancel = ttk.Button(self.frm_new_login_btn, text='Отмена',
                                               command=self.destroy)
        self.btn_new_login_cancel.pack(side=tk.RIGHT, pady=7, padx=7)

        self.btn_new_login_save = ttk.Button(self.frm_new_login_btn, text='Сохранить',
                                             command=self.save_new_login)
        self.btn_new_login_save.pack(side=tk.RIGHT, pady=7, padx=7)

    def check_empty(self):
        """ Процедура проверки на пустые поля формы
        :return: True/False
        """
        if len(self.ent_new_login_name.get()) == 0:
            mb.showwarning('Предупреждение', 'Введите логин')
            return False
        elif len(self.ent_new_login_password.get()) == 0:
            mb.showwarning('Предупреждение', 'Введите пароль')
            return False
        return True

    def check_exists(self):
        """ Процедура проверки дублей по введенным данным
        :return: True/False
        """
        id_connection = self.id_connection
        login_name = self.ent_new_login_name.get()
        data = self.app.db.get_login_name_for_check_exists(id_connection, login_name)
        if (data):
            mb.showwarning('Предупреждение', 'Дубль логина <' + data + '> для выбранного подключения')
            return False
        return True

    def save_new_login(self):
        """ Процедура сохранения нового логина """
        if (self.check_empty() and self.check_exists()):  # проверка на пустые поля и дубль
            # получаем поля с формы
            id_connection = self.id_connection
            login_name = self.ent_new_login_name.get()
            login_password = self.ent_new_login_password.get()
            login_description = self.txt_new_login_description.get('1.0', tk.END)
            # сохраняем
            self.app.db.insert_new_login(id_connection, login_name, login_password, login_description)
            # выводим списко логинов
            self.parent.show_logins_by_id_connection()
            # имитация клика по "Отмена"
            self.btn_new_login_cancel.invoke()