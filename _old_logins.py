import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
# import tkinter.ttk as ttk
#import sqlite3

# импортируем свои модули
import new_login_by_id_connection as new_login_by_id_connection


class Logins(tk.Toplevel):
    '''
    Базовый класс формы логинов
    '''
    def __init__(self, app, id_connection):
        super().__init__()
        self.id_connection = id_connection

        self.init_logins()
        self.app = app  # Передаем класс Main
        self.show_logins_by_id_connection()

    def init_logins(self):
        self.title('Список логинов')
        self.geometry("700x450+300+200")
        #self.resizable(False, False)

        # Добавляем функции модального, т.е прехватываем фокус не нем до закрытия
        self.grab_set()
        self.focus_set()

        # резиновая ячейка с таблицей
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # рамка для toolbar
        frm_logins_top_toolbar = ttk.Frame(self, relief=tk.RAISED, borderwidth=0)
        #frm_logins_top_toolbar.pack(fill=tk.BOTH, expand=True, anchor='n')
        frm_logins_top_toolbar.grid(row=0, column=0, columnspan=2, sticky='nwse')
        # Кнопки
        ## 1
        #btn_open_connection_filter = tk.Button(frm_logins_top_toolbar, text='Фильтр',
        #                                       bg='#d7d8e0', bd=0, compound=tk.BOTTOM, relief=tk.GROOVE,
        #                                       borderwidth=5, pady=2, padx=2,
        #                                       #command=self.open_filter_connection
        #                                       )
        #btn_open_connection_filter.pack(side=tk.LEFT, padx=5, pady=7)
        # 2
        btn_open_new_login = tk.Button(frm_logins_top_toolbar, text='Добавить',
                                        bg='#d7d8e0', bd=0, compound=tk.BOTTOM, relief=tk.GROOVE, borderwidth=5,
                                        pady=2, padx=2,
                                        command=self.open_new_login
                                        )
        btn_open_new_login.pack(side=tk.LEFT, padx=5, pady=7)
        # 3
        btn_open_update_login = tk.Button(frm_logins_top_toolbar, text='Обновить',
                                          bg='#d7d8e0', bd=0, compound=tk.BOTTOM, relief=tk.GROOVE,
                                          borderwidth=5, pady=2, padx=2
                                          #, command=self.open_updade_connection_type
                                          )
        btn_open_update_login.pack(side=tk.LEFT, padx=5, pady=7)
        # 4
        btn_open_delete_logins = tk.Button(frm_logins_top_toolbar, text='Удалить',
                                           bg='#d7d8e0', bd=0, compound=tk.BOTTOM, relief=tk.GROOVE,
                                           borderwidth=5, pady=2, padx=2,
                                           command=self.delete_logins
                                           )
        btn_open_delete_logins.pack(side=tk.LEFT, padx=5, pady=7)

        # рамка для контента
        #frm_logins_content = ttk.Frame(self, relief=tk.RAISED, borderwidth=0)
        #frm_logins_content.grid(row=1, column=0, sticky='nw')

        # список Treeview
        self.logins_table = ttk.Treeview(self, columns=('id_login', 'login_name', 'login_password', 'login_description'),
                                         height=10, show='headings')
        # параметры столбцов
        self.logins_table.column("id_login", width=40, anchor=tk.CENTER)
        self.logins_table.column("login_name", anchor=tk.CENTER)
        self.logins_table.column("login_password", anchor=tk.CENTER)
        self.logins_table.column("login_description", anchor=tk.CENTER)
        # названия столбцов
        self.logins_table.heading('id_login', text='ID')
        self.logins_table.heading('login_name', text='Логин')
        self.logins_table.heading('login_password', text='Пароль')
        self.logins_table.heading('login_description', text='Описание')
        # вывод с выравниванием по левой стороне
        #self.logins_table.pack(fill="both", side='left', expand=True)
        self.logins_table.grid(row=1, column=0, sticky='nwse')

        # полоса прокрутки для таблицы
        scroll = tk.Scrollbar(self, command=self.logins_table.yview)
        #scroll.pack(side=tk.RIGHT, fill=tk.Y)
        scroll.grid(row=1, column=1, sticky='nwse')
        self.logins_table.configure(yscrollcommand=scroll.set)

        # рамка для нижнего toolbar
        frm_logins_bottom_toolbar = ttk.Frame(self, relief=tk.RAISED, borderwidth=0)
        frm_logins_bottom_toolbar.grid(row=2, column=0, columnspan=2, sticky='nwse')
        # Кнопки
        # 1
        self.btn_ligins_cancel = tk.Button(frm_logins_bottom_toolbar, text='Назад',
                                           bg='#d7d8e0', bd=0, compound=tk.BOTTOM, relief=tk.GROOVE,
                                           borderwidth=5, pady=2, padx=10,
                                           command=self.destroy
                                           )
        self.btn_ligins_cancel.pack(side=tk.RIGHT, padx=17, pady=10)

# вывод списка компаний форму
    def show_logins_by_id_connection(self):
        '''
        Процедура перезаполнения списка логинов
        '''
        # очистка таблицы
        [self.logins_table.delete(i) for i in self.logins_table.get_children()]
        #
        id_connection = self.id_connection
        data = self.app.db.get_logins_list_by_id_connection(id_connection)
#        [self.companies_list.insert('', 'end', values=row) for row in self.db.c_sqlite3.fetchall()]
        print(len(data))
        [self.logins_table.insert('', 'end', values=row) for row in data]

    def open_new_login(self):
        '''
        Открываем окно для ввода нового логтна по выбранному подключению
        Передаем app и id первого выбранного в списке подключения
        '''
        new_login_by_id_connection.NewLoginByIdConnection(self.app, self.id_connection)
        self.show_logins_by_id_connection()

    def delete_logins(self):
        '''
        Процедура удаления выбранных типов подключения
        '''
        if (self.logins_table.focus() != ''):
            answer = mb.askyesno(title='Запрос действия',
                                 message="Хотите удалить выбранные элементы?")
            if (answer):  # если Да = True
                ids = []  # кортеж id выделенных элементов
                for selection_item in self.logins_table.selection():
                    ids.append(self.logins_table.set(selection_item, '#1'),)
                self.app.db.delete_logins(ids)
                self.show_logins_by_id_connection()  # перезагружаем список
        else:
            mb.showwarning('Предупреждение', 'Выберите логин (логины)')




