import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
# import tkinter.ttk as ttk
#import sqlite3

# импортируем свои модули
# import new_login_by_id_connection as new_login_by_id_connection
import login as login
import connections as connections


class Logins(tk.Frame):
    """ Базовый класс формы логинов """
    def __init__(self, root, app, id_connection):
        super().__init__(root)
        self.root = root
        self.app = app  # Передаем класс Main
        self.id_connection = id_connection

        self.init_logins()

        self.show_logins_by_id_connection()
        self.show_company_name()

    def init_logins(self):
        #self.title('Список логинов')
        #self.geometry("700x450+300+200")
        #self.resizable(False, False)

        # резиновая ячейка с таблицей
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        # для отображения данных на форме
        self.pack(fill=tk.BOTH, expand=True)

        ## базовая рамка для модуля
        #frm_logins = ttk.Frame(self, relief=tk.RAISED, borderwidth=0)
        #frm_logins.pack(fill=tk.BOTH, expand=True)

        # рамка для toolbar
        #frm_logins_top_toolbar = ttk.Frame(frm_logins, relief=tk.RAISED, borderwidth=0)
        #frm_logins_top_toolbar.pack(fill=tk.X)
        frm_logins_top_toolbar = ttk.Frame(self, relief=tk.RAISED, borderwidth=0)
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
        btn_open_update_login = tk.Button(frm_logins_top_toolbar, text='Редактировать',
                                          bg='#d7d8e0', bd=0, compound=tk.BOTTOM, relief=tk.GROOVE,
                                          borderwidth=5, pady=2, padx=2,
                                          command=self.open_update_login
                                          )
        btn_open_update_login.pack(side=tk.LEFT, padx=5, pady=7)
        # 4
        btn_open_delete_logins = tk.Button(frm_logins_top_toolbar, text='Удалить',
                                           bg='#d7d8e0', bd=0, compound=tk.BOTTOM, relief=tk.GROOVE,
                                           borderwidth=5, pady=2, padx=2,
                                           command=self.delete_logins
                                           )
        btn_open_delete_logins.pack(side=tk.LEFT, padx=5, pady=7)

        # рамка вывода названия компании и типа подключения
        frm_logins_title = ttk.Frame(self, relief=tk.RAISED, borderwidth=0)
        frm_logins_title.grid(row=1, column=0, columnspan=2, sticky='nwse')
        ## тут
        #data = self.app.db.get_company_connection_type_by_id_connection(self.id_connection)
        ##clipboard = data[1] + '\n' + data[2] + '\n' + data[3]
        #label = data  # data[1] + ' ' + data[2] + ' ' + data[3]

        self.lbl_company_name = tk.Label(frm_logins_title, bg='#d7d8e0', text='Компания - > Тип подключения')
        self.lbl_company_name.pack(side=tk.LEFT, padx=5, pady=7)

        ## контент модуля
        #frm_logins_content = ttk.Frame(frm_logins, relief=tk.RAISED, borderwidth=0)
        #frm_logins_content.pack(fill=tk.BOTH, expand=True)

        # список Treeview
        self.logins_table = ttk.Treeview(self, columns=('id_login', 'login_name', 'login_password', 'login_description'),
                                         height=10, show='headings')
        #self.logins_table = ttk.Treeview(frm_logins_content,
        #                                 columns=('id_login', 'login_name', 'login_password', 'login_description'),
        #                                 height=10, show='headings')
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

        #self.logins_table.pack(fill="both", side='left', expand=True)
        self.logins_table.grid(row=2, column=0, sticky='nwse')
        # вешаем контекстное меню на ЛКМ
        self.logins_table.bind('<Button-3>', self.show_context_menu)

        # полоса прокрутки для таблицы
        scroll = tk.Scrollbar(self, command=self.logins_table.yview)
        #scroll.pack(side=tk.RIGHT, fill=tk.Y)
        scroll.grid(row=2, column=1, sticky='nwse')
        self.logins_table.configure(yscrollcommand=scroll.set)

        ## полоса прокрутки для списка
        #scroll = tk.Scrollbar(frm_logins_content, command=self.logins_table.yview)
        #scroll.pack(side=tk.RIGHT, fill=tk.Y)
        #self.logins_table.configure(yscrollcommand=scroll.set)


        # рамка для нижнего toolbar
        #frm_logins_bottom_toolbar = ttk.Frame(frm_logins, relief=tk.RAISED, borderwidth=0)
        #frm_logins_bottom_toolbar.pack(fill=tk.BOTH, expand=True)
        frm_logins_bottom_toolbar = ttk.Frame(self, relief=tk.RAISED, borderwidth=0)
        frm_logins_bottom_toolbar.grid(row=3, column=0, columnspan=2, sticky='nwse')
        # Кнопки
        # 1
        self.btn_ligins_back = tk.Button(frm_logins_bottom_toolbar, text='Назад',
                                           bg='#d7d8e0', bd=0, compound=tk.BOTTOM, relief=tk.GROOVE,
                                           borderwidth=5, pady=2, padx=10,
                                           command=self.open_connections
                                           )
        self.btn_ligins_back.pack(side=tk.RIGHT, padx=17, pady=10)

        # контекстное меню для копирования
        self.context_menu = tk.Menu(self.logins_table, tearoff=0)
        self.context_menu.add_command(
            command=self.copy_to_clipboard,
            label="Копировать")

    def copy_to_clipboard(self):
        """ Процедура копирования в буфер обмена """
        id_login = self.logins_table.set(self.logins_table.selection()[0], '#1')

        data_company = self.app.db.get_company_connection_type_by_id_connection(self.id_connection)
        data_login = self.app.db.get_login_by_id(id_login)

        #print(data_login)

        #clipboard =   data_login[1] + '\n' + data_login[2] + '\n' + data_login[3]
        clipboard = data_company[1] + '\n===\n' + data_company[2] + '\n===\n' + \
                    data_login[1] + '\n---\n' + data_login[2] + '\n---\n' + data_login[3]
        self.root.clipboard_clear()
        self.root.clipboard_append(clipboard)

    def show_context_menu(self, event):
        """ Процедура вывода контекстного меню
        :param event:
        :return:
        """
        if (self.logins_table.focus() != ''):
            self.logins_table.identify_row(event.y)
            self.context_menu.post(event.x_root, event.y_root)

    def show_company_name(self):
        """ Процедура выводв на форму названия компании и типа подклюжчения """
        data = self.app.db.get_company_connection_type_by_id_connection(self.id_connection)
        label = (data[1]) + '  ->  ' + (data[2])
        self.lbl_company_name.config(text=label)

    def show_logins_by_id_connection(self):
        """ Процедура перезаполнения списка логинов """
        # очистка таблицы
        [self.logins_table.delete(i) for i in self.logins_table.get_children()]
        #
        id_connection = self.id_connection
        data = self.app.db.get_logins_list_by_id_connection(id_connection)
        # [self.companies_list.insert('', 'end', values=row) for row in self.db.c_sqlite3.fetchall()]

        [self.logins_table.insert('', 'end', values=row) for row in data]

    def open_new_login(self):
        """ Открываем окно для ввода нового логина по выбранному подключению
        Передаем app и id первого выбранного в списке подключения """
        login.NewLogin(self.app, self, self.id_connection)
        self.show_logins_by_id_connection()

    def open_update_login(self):
        """ Открываем окно для обновления выбранного подключения """
        if self.logins_table.focus() != '':
            id_login = self.logins_table.set(self.logins_table.selection()[0], '#1')
            login.UpdateLogin(self.app, self, self.id_connection, id_login)
        else:
            mb.showwarning('Предупреждение', 'Выберите тип подключения')

    def open_connections(self):
        """ Возврат на окно со списком подключений """
        # чистим форму
        self.app.clear_frm_content_all()
        # убиваем текушую форму
        self.destroy()
        # вывод подключений
        self.connections = connections.Connections(self.app.frm_content_all, self.app)

    def delete_logins(self):
        """ Процедура удаления выбранных типов подключения """
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




