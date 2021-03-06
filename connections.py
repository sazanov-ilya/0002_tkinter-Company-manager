import ctypes
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
import re

# импортируем свои модули
import __general_procedures as gp
import logins as logins
# import new_login_by_id_connection as new_login_by_id_connection
# import connection_types as connection_types


# словать фильтров
# connections_filter_dict = {'id_company': '', 'id_connection_type': '', 'connection_ip': '', 'connection_description': ''}
connections_filter_dict = {}


class Connections(tk.Frame):
    """ Базовый класс формы списка подключений """
    def __init__(self, root, app):
        super().__init__(root)
        self.init_connections()
        self.app = app  # Main

        self.show_connections()

        # self.db = db.DB(root)  # Передаем класс DB
        # self.show_connection_types()  # загружаем данные на форму

    def init_connections(self):
        # для отображения на полное окно
        self.pack(fill=tk.BOTH, expand=True)

        # базовая рамка для модуля
        # frm_conns = ttk.Frame(app.frm_content_all, relief=tk.RAISED, borderwidth=3)
        frm_conns = ttk.Frame(self, relief=tk.RAISED, borderwidth=0)
        frm_conns.pack(fill=tk.BOTH, expand=True)

        # рамка toolbar для кнопок
        frm_conns_toolbar = ttk.Frame(frm_conns, relief=tk.RAISED, borderwidth=0)
        frm_conns_toolbar.pack(fill=tk.X)

        # Кнопки
        # 1
        self.btn_open_connection_filter = tk.Button(frm_conns_toolbar, text='Фильтр', bg='#d7d8e0', bd=0,
                                                    compound=tk.BOTTOM, relief=tk.GROOVE, borderwidth=5, pady=2, padx=2,
                                                    command=self.open_filter_connection)
        self.btn_open_connection_filter.pack(side=tk.LEFT)
        # 2
        btn_open_connection_new = tk.Button(frm_conns_toolbar, text='Добавить',
                                            bg='#d7d8e0', bd=0, compound=tk.BOTTOM, relief=tk.GROOVE, borderwidth=5,
                                            pady=2, padx=2,
                                            command=self.open_new_connection)
        btn_open_connection_new.pack(side=tk.LEFT)
        # 3
        btn_open_connection_update = tk.Button(frm_conns_toolbar, text='Редактировать',
                                               bg='#d7d8e0', bd=0, compound=tk.BOTTOM, relief=tk.GROOVE,
                                               borderwidth=5, pady=2, padx=2,
                                               command=self.open_update_connection)
        btn_open_connection_update.pack(side=tk.LEFT)
        # 4
        btn_open_connection_types_delete = tk.Button(frm_conns_toolbar, text='Удалить',
                                                     bg='#d7d8e0', bd=0, compound=tk.BOTTOM, relief=tk.GROOVE,
                                                     borderwidth=5, pady=2, padx=2,
                                                     command=self.delete_connections)
        btn_open_connection_types_delete.pack(side=tk.LEFT)
        ## 6
        #btn_open_new_login = tk.Button(frm_conns_toolbar, text='Добавить логин',
        #                               bg='#d7d8e0', bd=0, compound=tk.BOTTOM, relief=tk.GROOVE,
        #                               borderwidth=5, pady=2, padx=2,
        #                               command=self.open_new_login
        #                               )
        #btn_open_new_login.pack(side=tk.LEFT)
        # 7
        btn_open_all_login = tk.Button(frm_conns_toolbar, text='Открыть логины',
                                       bg='#d7d8e0', bd=0, compound=tk.BOTTOM, relief=tk.GROOVE,
                                       borderwidth=5, pady=2, padx=2,
                                       command=self.open_logins
                                       )
        btn_open_all_login.pack(side=tk.LEFT)

        # контент модуля
        frm_conns_content = ttk.Frame(frm_conns, relief=tk.RAISED, borderwidth=0)
        frm_conns_content.pack(fill=tk.BOTH, expand=True)

        # список Treeview
        self.treeview_list = ttk.Treeview(frm_conns_content,
                                          columns=('id_connection', 'company_name', 'connection_type_name',
                                                   'connection_ip', 'connection_description'),
                                          height=10, show='headings')
        # параметры столбцов
        self.treeview_list.column("id_connection", width=40, anchor=tk.CENTER)
        self.treeview_list.column("company_name", width=110, anchor=tk.CENTER)
        self.treeview_list.column("connection_type_name", width=110, anchor=tk.CENTER)
        self.treeview_list.column("connection_ip", width=100, anchor=tk.CENTER)
        self.treeview_list.column("connection_description", width=300, anchor=tk.CENTER)

        # названия столбцов
        self.treeview_list.heading('id_connection', text='ID')
        self.treeview_list.heading('company_name', text='Компания')
        self.treeview_list.heading('connection_type_name', text='Тип подключения')
        self.treeview_list.heading('connection_ip', text='Ip-адрес (домен)')
        self.treeview_list.heading('connection_description', text='Описание для подключения')
        # вывод с выравниванием по левой стороне
        self.treeview_list.pack(fill="both", side='left', expand=True)

        # полоса прокрутки для списка
        scroll = tk.Scrollbar(frm_conns_content, command=self.treeview_list.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.treeview_list.configure(yscrollcommand=scroll.set)

        # # рамка для toolbar
        # frm_toolbar = tk.Frame(frm_conns, bg='#d7d8e0', bd=4, relief=tk.GROOVE)
        # frm_toolbar.pack(side=tk.TOP, fill=tk.X)

    def show_connections(self):
        """ Процедура перезаполнения списка тиов подключения согласно данных БД и фильтров """
        self.color_connection_filter()  # цвет кнопки фильтра
        [self.treeview_list.delete(i) for i in self.treeview_list.get_children()]  # чистим таблицу
        # получаем данные фильтра
        id_company = connections_filter_dict.get('id_company', '')
        id_connection_type = connections_filter_dict.get('id_connection_type', '')
        connection_ip = connections_filter_dict.get('connection_ip', '')
        connection_description = connections_filter_dict.get('connection_description', '')
        data = self.app.db.get_connections_by_filter(id_company,
                                                     id_connection_type,
                                                     connection_ip,
                                                     connection_description)

        [self.treeview_list.insert('', 'end', values=row) for row in data]  # выводим список на форму

    def delete_connections(self):
        """ Процедура удаления выбранных типов подключения """
        if self.treeview_list.focus() != '':
            answer = mb.askyesno(title='Запрос действия',
                                 message="Хотите удалить выбранные элементы?")
            if answer:  # если Да = True
                ids = []  # кортеж id выделенных элементов
                for selection_item in self.treeview_list.selection():
                    ids.append(self.treeview_list.set(selection_item, '#1'), )
                self.app.db.delete_connections(ids)
                self.show_connections()  # перезагружаем список
        else:
            mb.showwarning('Предупреждение', 'Выберите подключение')

    def open_update_connection(self):
        """ Открываем окно для обновления выбранного подключения """
        if self.treeview_list.focus() != '':
            id_connection = self.treeview_list.set(self.treeview_list.selection()[0], '#1')
            UpdateConnection(self.app, self, id_connection)
        else:
            mb.showwarning('Предупреждение', 'Выберите подключение')

    def open_new_connection(self):
        """ Открываем окно ввода данных нового подключения """
        NewConnection(self.app)

    def open_filter_connection(self):
        """ Открываем окно фильтров списка подключений """
        FilterConnections(self.app)

    def color_connection_filter(self):
        """ Процедкра смены цвета кнопки Фильтр """
        if connections_filter_dict:  # если есть фильтры
            self.btn_open_connection_filter.configure(bg='#A9A9A9')
        else:
            self.btn_open_connection_filter.configure(bg='#d7d8e0')

    def set_connection_filter(self, id_company, id_connection_type, connection_ip, connection_description):
        """ Процедура применения фильтра
        :param id_company:
        :param id_connection_type:
        :param connection_ip:
        :param connection_description:
        :return: No
        """
        connections_filter_dict.clear()  # Чистим словарь
        # Пересоздаем словарь
        if id_company:
            connections_filter_dict['id_company'] = id_company
        if id_connection_type:
            connections_filter_dict['id_connection_type'] = id_connection_type
        if connection_ip:
            connections_filter_dict['connection_ip'] = connection_ip
        if connection_description:
            connections_filter_dict['connection_description'] = connection_description

        # self.color_connection_filter()  # цвет кнопки фильтра
        self.show_connections()  # перезегружаем список

    def clear_connection_filter(self):
        """ Процедура очистки фильтров подключений """
        connections_filter_dict.clear()  # чистим словарь
        # self.color_connection_filter()  # цвет кнопки фильтра
        self.show_connections()  # перезегружаем список

    def open_logins(self):
        """ Открывааем окно со списком всех логинов выделенного подключения
        Передаем app и id первого выбранного в списке подключения """
        if self.treeview_list.focus() != '':
            id_connection = self.treeview_list.set(self.treeview_list.selection()[0], '#1')
            # чистим форму
            self.app.clear_frm_content_all()
            # открываем логины
            self.logins = logins.Logins(self.app.frm_content_all, self.app, id_connection)

            # Companies()
            # self.connection_types = connection_types.ConnectionTypes(self.app.frm_content_all, self.app)
        else:
            mb.showwarning('Предупреждение', 'Выберите подключение в списке')

#    def set_connection_filter(self, id_company, id_connection_type, connection_ip, connection_description):
#        """ Сеттер для словаря фильтра
#        :param id_company:
#        :param id_connection_type:
#        :param connection_ip:
#        :param connection_description:
#        :return No
#        """
#        # сохраняем фильтр в словарь
#        self.connections_filter_dict['id_company'] = id_company
#        self.connections_filter_dict['id_connection_type'] = id_connection_type
#        self.connections_filter_dict['connection_ip'] = connection_ip
#        self.connections_filter_dict['connection_description'] = connection_description
#        self.show_connections()  # перезагружаем список
#
#    def clear_connection_filter(self):
#        """ Процедура очистки фильтра подключений """
#        for key in self.connections_filter_dict:
#            self.connections_filter_dict[key] = ''  # обнуляем ключи
#            self.show_connections()  # перезегружаем список


class Connection(tk.Toplevel):
    """ Базовый класс всплывающего окна подключений """
    def __init__(self, app):
        super().__init__()
        # self.geometry("500x300+300+200")
        self.init_connections()
        self.app = app  # Передаем класс Main
        # self.get_comps_list()
        # self.get_conn_types_list()

    # Кнопка печать всего в csv

    def init_connections(self):
        # self.master.title("Оставить отзыв")
        # self.style = ttk.Style()
        # self.style.theme_use("default")

        # переделать позиционирование через grid, чтобы рамка кнопок внизу была
        # self.geometry('415x200+400+300')
        # self.resizable(False, False)

        # добавляем функции модального, прехватываем фокус до закрытия
        self.grab_set()
        self.focus_set()

        # self.comps_list = []
        # self.conn_types_list = []

        # Первая рамка является базовой. На ней располагаются все остальные рамки
        # для отображения на полное окно
        # self.pack(fill=tk.BOTH, expand=True)

        # базовая рамка для модуля
        frm_conns = ttk.Frame(self, relief=tk.RAISED, borderwidth=0)
        frm_conns.pack(fill=tk.BOTH, expand=True)

        frm_comps_list = ttk.Frame(frm_conns, relief=tk.RAISED, borderwidth=0)
        frm_comps_list.pack(fill=tk.X)
        lbl_comps_list = ttk.Label(frm_comps_list, text="Компания", width=17)
        lbl_comps_list.pack(side=tk.LEFT, padx=5, pady=5, anchor=tk.E)
        self.cmb_comps_list = ttk.Combobox(frm_comps_list, width=50, height=20)
        # cmb_comps_list['values'] = companies_list_items
        self.cmb_comps_list.pack(fill=tk.X, padx=5, expand=True)

        frm_conn_types_list = ttk.Frame(frm_conns, relief=tk.RAISED, borderwidth=0)
        frm_conn_types_list.pack(fill=tk.X)
        lbl_conn_types_list = ttk.Label(frm_conn_types_list, text="Тип подключения", width=17)
        lbl_conn_types_list.pack(side=tk.LEFT, padx=5, pady=5)
        self.cmb_conn_types_list = ttk.Combobox(frm_conn_types_list, width=50, height=20)
        # cmb_conn_types_list['values'] = companies_list_items
        self.cmb_conn_types_list.pack(fill=tk.X, padx=5, expand=True)

        frm_conn_name = ttk.Frame(frm_conns, relief=tk.RAISED, borderwidth=0)
        frm_conn_name.pack(fill=tk.X)
        lbl_conn_name = ttk.Label(frm_conn_name, text="Ip-адрес/домен", width=17)
        lbl_conn_name.pack(side=tk.LEFT, padx=5, pady=5)
        self.ent_conn_name = ttk.Entry(frm_conn_name)
        self.ent_conn_name.pack(fill=tk.X, padx=5, expand=True)
        self.ent_conn_name.bind("<Control-KeyPress>", gp.keys)

        # на все свободное место
        self.frm_conn_description = ttk.Frame(frm_conns, relief=tk.RAISED, borderwidth=0)
        self.frm_conn_description.pack(fill=tk.BOTH, expand=True)
        lbl_conn_description = ttk.Label(self.frm_conn_description, text="Описание", width=17)
        lbl_conn_description.pack(side=tk.LEFT, anchor=tk.N, padx=5, pady=5)
        self.txt_conn_description = tk.Text(self.frm_conn_description)
        self.txt_conn_description.pack(fill=tk.BOTH, pady=5, padx=5, expand=True)
        self.txt_conn_description.bind("<Control-KeyPress>", gp.keys)

        # рамка для кнопок
        self.frm_conn_btn = ttk.Frame(frm_conns, relief=tk.RAISED, borderwidth=0)
        self.frm_conn_btn.pack(fill=tk.X)
        self.btn_cancel = ttk.Button(self.frm_conn_btn, text='Закрыть', command=self.destroy)
        # self.btn_cancel.place(x=305, y=160)
        self.btn_cancel.pack(side=tk.RIGHT, pady=7, padx=7)

    def get_comps_list(self):
        """ Процедура заполнения списка компаний """
        self.comps_list = self.app.db.get_company_for_list()
        # first, second- первые 2 элемента, *other - все остальные элементы
        # self.cmb_comps_list['values'] = [second for first, second, *other in data]
        self.cmb_comps_list['values'] = [elem[1] for elem in self.comps_list]
        # self.cmb_comps_list.current(0)
        # print(self.comps_list)

    def get_conn_types_list(self):
        """ Процедура заполнения списка типов подключения """
        self.conn_types_list = self.app.db.get_connection_type_for_list()
        # first, second- первые 2 элемента, *other - все остальные элементы
        # self.cmb_comps_list['values'] = [second for first, second, *other in data]
        self.cmb_conn_types_list['values'] = [elem[1] for elem in self.conn_types_list]
        # self.cmb_conn_types_list.current(0)
        # print(self.conn_types_list)

    def check_empty(self):
        """ Процедкра проверки на пустые поля
        :return: True/False
        """
        if (self.cmb_comps_list.current()) == -1:
            mb.showwarning('Предупреждение', 'Выберите компанию')
            return False
        elif (self.cmb_conn_types_list.current()) == -1:
            mb.showwarning('Предупреждение', 'Выберите тип доступа')
            return False
        elif len(self.ent_conn_name.get()) == 0:
            mb.showwarning('Предупреждение', 'Введите Ip-адрес/домен')
            return False
        return True

    def check_exists(self):
        """ Процедура проверки дублей по введенным данным
        :return: True/False
        """
        id_company = self.comps_list[self.cmb_comps_list.current()][0]
        id_connection_type = self.conn_types_list[self.cmb_conn_types_list.current()][0]
        conn_name = self.ent_conn_name.get()
        data = self.app.db.get_connection_ip_for_check_exists(id_company, id_connection_type, conn_name)
        if data:
            mb.showwarning('Предупреждение', 'Данное подключение уже существует')
            return False
        return True


class FilterConnections(Connection):
    """ Класс формы ввода фильтров для списка подключений """
    def __init__(self, app):  # Конструктор
        super().__init__(app)
        self.init_filter_connection()
        self.app = app  # Передаем класс Main
        # self.db = db  # Передаем класс DB
        self.get_comps_list()  # Список компаний
        self.get_conn_types_list()  # Список типов подключения
        self.get_connection_filter()

    def init_filter_connection(self):
        self.title('Фильтр подключений')

        # # переопределяем поле для комментария
        # self.txt_conn_description = ttk.Entry(self.frm_conn_description)
        # #self.txt_conn_description.pack(fill=tk.BOTH, pady=5, padx=5, expand=True)
        # self.txt_conn_description.pack(fill=tk.X, padx=5, expand=True)

        self.btn_apply_connection_filter = ttk.Button(self.frm_conn_btn, text='Применить',
                                                      command=self.apply_connection_filter)
        # btn_apply_connection_filter.place(x=145, y=85)
        self.btn_apply_connection_filter.pack(side=tk.RIGHT, pady=7, padx=7)

        btn_clear_connection_filter = ttk.Button(self.frm_conn_btn, text='Сбросить')
        # btn_clear_connection_filter.place(x=65, y=85)
        btn_clear_connection_filter.pack(side=tk.RIGHT, pady=7, padx=7)
        btn_clear_connection_filter.bind('<Button-1>', lambda event: self.app.connections.clear_connection_filter())
        btn_clear_connection_filter.bind('<Button-1>', lambda event: self.destroy(), add='+')  # вешаем доп событие

    def get_connection_filter(self):
        """ Процедура получения текущих значений фильтра и вывод на форму """
        if connections_filter_dict:
            # Получаем текущие фильтры
            id_company = connections_filter_dict.get('id_company', '')
            id_connection_type = connections_filter_dict.get('id_connection_type', '')
            connection_ip = connections_filter_dict.get('connection_ip', '')
            connection_description = connections_filter_dict.get('connection_description', '')

            # Компания по фильтру
            if id_company:
                index_company = 0
                for items in self.comps_list:
                    if items[0] == id_company:
                        break
                    index_company += 1
                self.cmb_comps_list.current(index_company)

            # Тип подключения по фильтру
            if id_connection_type:
                index_connection_type = 0
                for items in self.conn_types_list:
                    if items[0] == id_connection_type:
                        break
                    index_connection_type += 1
                self.cmb_conn_types_list.current(index_connection_type)

            if connection_ip:
                self.ent_conn_name.insert(0, connection_ip)
            if connection_description:
                self.txt_conn_description.insert(1.0, connection_description)

        # в идеале опивсание преопределить на однострочное поле

    def apply_connection_filter(self):
        """ Процедура применения фильтров """
        # получаем компанию с формы
        if (self.cmb_comps_list.current()) == -1:
            id_company = ''
        else:
            id_company = self.comps_list[self.cmb_comps_list.current()][0]
        # получаем тип подключения с формы
        if (self.cmb_conn_types_list.current()) == -1:
            id_connection_type = ''
        else:
            id_connection_type = self.conn_types_list[self.cmb_conn_types_list.current()][0]
        # получаем Ip-адрес/домен с формы
        conn_name = self.ent_conn_name.get()
        # получаем Описание с формы
        conn_description = re.sub('[\n]', '', (self.txt_conn_description.get('1.0', tk.END)))
        # сохраняем фильтр
        self.app.connections.set_connection_filter(id_company, id_connection_type, conn_name, conn_description)
        # имитация клика по кнопке закрыть
        self.btn_cancel.invoke()


class NewConnection(Connection):
    """ Класс формы ввода нового подключения """
    def __init__(self, app):  # Конструктор
        super().__init__(app)
        self.init_new_connection()
        self.app = app  # Передаем класс Main
        # self.db = db  # Передаем класс DB
        self.get_comps_list()  # Список компаний
        self.get_conn_types_list()  # Список типов подключения

    def init_new_connection(self):
        self.title('Добавить подключение')

        # Кнопка "Сохранить"
        self.btn_save = ttk.Button(self.frm_conn_btn, text='Сохранить', command=self.save_new_connection)
        # self.btn_cancel.place(x=305, y=160)
        self.btn_save.pack(side=tk.RIGHT, pady=7, padx=7)

    def save_new_connection(self):
        """ Процедура сохраненеия нового подключения """
        if self.check_empty() and self.check_exists():  # проверка на пустые поля и дубль
            # данные с формы
            id_company = self.comps_list[self.cmb_comps_list.current()][0]
            id_connection_type = self.conn_types_list[self.cmb_conn_types_list.current()][0]
            conn_name = self.ent_conn_name.get()
            conn_description = self.txt_conn_description.get('1.0', tk.END)
            self.app.db.insert_new_connection(id_company, id_connection_type, conn_name, conn_description)  # сохраняем
            self.app.connections.show_connections()  # выводим список на форму
            # mb.showinfo("Информация", 'Данные сохранены')
            self.btn_cancel.invoke()  # имитация клика по кнопке закрыть


class UpdateConnection(Connection):
    """ Класс формы обновления подключений """
    def __init__(self, app, parent, id_connection):  # Конструктор
        super().__init__(app)
        self.init_update_connection()

        self.app = app  # Передаем класс Main
        self.parent = parent  # класс ConnectionTypes
        self.id_connection = id_connection
        # self.db = db.DB()  # Передаем класс DB

        self.get_connection_for_update()

    def init_update_connection(self):
        self.title('Обновить подключение')
        # Добавляем кнопку "Обновить"
        btn_update = ttk.Button(self.frm_conn_btn, text='Обновить', command=self.update_connection)
        #btn_save.place(x=220, y=160)
        btn_update.pack(side=tk.RIGHT, pady=7, padx=7)

    def get_connection_for_update(self):
        """ Процедура получения и вывода на форму данных выделенной строки """
        data = self.app.db.get_connection_for_update_by_id(self.id_connection)
        # Выводим значения в поля формы
        self.cmb_comps_list['values'] = [data[1]]
        self.cmb_comps_list.current(0)
        self.cmb_comps_list.configure(state="disabled")  # normal, readonly и disabled
        self.cmb_conn_types_list['values'] = [data[2]]
        self.cmb_conn_types_list.current(0)
        self.cmb_conn_types_list.configure(state="disabled")  # normal, readonly и disabled
        self.ent_conn_name.insert(0, data[3])
        self.txt_conn_description.insert(1.0, data[4])

    def update_connection(self):
        """ Процедура обновления типа подключения """
        if self.check_empty():  # проверка на пустые поля
            # данные с формы
            # id_company = self.comps_list[self.cmb_comps_list.current()][0]  # Отключено
            # id_connection_type = self.conn_types_list[self.cmb_conn_types_list.current()][0]  # Отключено
            conn_name = self.ent_conn_name.get()
            conn_description = self.txt_conn_description.get('1.0', tk.END)
            self.app.db.update_connection_by_id(self.id_connection, conn_name, conn_description)  # Обновляем
            self.parent.show_connections()  # выводим список на форму
            # mb.showinfo("Информация", 'Данные сохранены')
            self.btn_cancel.invoke()  # имитация клика по кнопке закрыть

    #def update_connection_type(self):
    #    """ Процедура сохранения нового типа подключения """
    #    if self.check_empty():  # проверка на пустые поля
    #        # получаем поля с формы
    #        connection_type_name = self.ent_connection_type_name.get()
    #        connection_type_description = self.txt_connection_type_description.get('1.0', tk.END)
    #        self.app.db.update_connection_type_by_id(self.id_connection_type, connection_type_name,
    #                                                 connection_type_description)  # обновляем
    #        self.parent.show_connection_types()  # выводим на форму
    #        self.btn_cancel.invoke()  # имитация клика по "Отмена"

