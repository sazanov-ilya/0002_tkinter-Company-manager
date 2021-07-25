import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
# import tkinter.ttk as ttk
#import sqlite3

# импортируем свои модули
#import db_sqlite3 as db


# cловарь фильтров
connection_types_filter_dict = {'connection_type_name': '', 'connection_type_description': ''}


class ConnectionTypes(tk.Frame):
    '''
    Базовый класс для типов подключения, меню и список типов подключения
    '''

    def __init__(self, root, app):
        super().__init__(root)
        self.init_connection_types()
        self.app = app  # Передаем класс Main
        #self.db = db.DB(root)  # Передаем класс DB
        self.show_connection_types()  # загружаем данные на форму

    def init_connection_types(self):
        # для отображения на полное окно
        self.pack(fill=tk.BOTH, expand=True)

        # базовая рамка для модуля
        # frm_connection_types = ttk.Frame(app.frm_content_all, relief=tk.RAISED, borderwidth=3)
        frm_connection_types = ttk.Frame(self, relief=tk.RAISED, borderwidth=0)
        frm_connection_types.pack(fill=tk.BOTH, expand=True)

        # рамка toolbar для кнопок
        frm_connection_types_toolbar = ttk.Frame(frm_connection_types, relief=tk.RAISED, borderwidth=0)
        frm_connection_types_toolbar.pack(fill=tk.X)

        # кнопки
        # 1
        btn_open_connection_filter = tk.Button(frm_connection_types_toolbar, text='Фильтр',
                                               bg='#d7d8e0', bd=0, compound=tk.BOTTOM, relief=tk.GROOVE,
                                               borderwidth=5, pady=2, padx=2, command=self.open_connection_type_filter)
        btn_open_connection_filter.pack(side=tk.LEFT)
        # 2
        btn_open_connection_new = tk.Button(frm_connection_types_toolbar, text='Добавить',
                                            bg='#d7d8e0', bd=0, compound=tk.BOTTOM, relief=tk.GROOVE, borderwidth=5,
                                            pady=2, padx=2, command=self.open_new_connection_type)
        btn_open_connection_new.pack(side=tk.LEFT)
        # 3
        btn_open_connection_update = tk.Button(frm_connection_types_toolbar, text='Редактировать'
                                               , bg='#d7d8e0', bd=0, compound=tk.BOTTOM, relief=tk.GROOVE,
                                               borderwidth=5, pady=2, padx=2, command=self.open_updade_connection_type)
        btn_open_connection_update.pack(side=tk.LEFT)
        # 4
        btn_open_connection_types_delete = tk.Button(frm_connection_types_toolbar, text='Удалить',
                                                     bg='#d7d8e0', bd=0, compound=tk.BOTTOM, relief=tk.GROOVE,
                                                     borderwidth=5, pady=2, padx=2, command=self.delete_connection_types)
        btn_open_connection_types_delete.pack(side=tk.LEFT)

        # контент модуля
        frm_connection_types_content = ttk.Frame(frm_connection_types, relief=tk.RAISED, borderwidth=0)
        frm_connection_types_content.pack(fill=tk.BOTH, expand=True)

        # список Treeview
        self.connection_types_list = ttk.Treeview(frm_connection_types_content,
                                                  columns=('id_connection', 'connection_name',
                                                           'connection_description'), height=10, show='headings')
        # параметры столбцов
        self.connection_types_list.column("id_connection", width=40, anchor=tk.CENTER)
        self.connection_types_list.column("connection_name", width=150, anchor=tk.CENTER)
        self.connection_types_list.column("connection_description", width=355, anchor=tk.CENTER)
        # названия столбцов
        self.connection_types_list.heading('id_connection', text='ID')
        self.connection_types_list.heading('connection_name', text='Наименование')
        self.connection_types_list.heading('connection_description', text='Описание')
        # вывод с выравниванием по левой стороне
        self.connection_types_list.pack(fill="both", side='left', expand=True)

        # полоса прокрутки для списка
        scroll = tk.Scrollbar(frm_connection_types_content, command=self.connection_types_list.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.connection_types_list.configure(yscrollcommand=scroll.set)

        ## рамка для toolbar
        # frm_toolbar = tk.Frame(frm_connection_types, bg='#d7d8e0', bd=4, relief=tk.GROOVE)
        # frm_toolbar.pack(side=tk.TOP, fill=tk.X)

    def show_connection_types(self):
        '''
        Процедура перезаполнения списка тиов подключения согласно данных БД и фильтров
        '''
        # очистка таблицы
        [self.connection_types_list.delete(i) for i in self.connection_types_list.get_children()]
        # получаем данные согласно фильтров
        data = self.app.db.get_connection_type_list_by_filter(
            connection_types_filter_dict.get('connection_type_name', ''),
            connection_types_filter_dict.get('connection_type_description', ''))
#        [self.connection_types_list.insert('', 'end', values=row) for row in self.db.c_sqlite3.fetchall()]
        [self.connection_types_list.insert('', 'end', values=row) for row in data]

    def delete_connection_types(self):
        '''
        Процедура удаления выбранных типов подключения
        '''
        if (self.connection_types_list.focus() != ''):
            # Цикл удаление нескольких записей
#            [ids.append(row) for row in self.#            [ids.append(row) for row in self._list.selection()]_list.selection()]

            ids = []  # кортеж id выделенных элементов
            for selection_item in self.connection_types_list.selection():
                ids.append(self.connection_types_list.set(selection_item, '#1'),)
            self.app.db.delete_connection_types(ids)
            self.show_connection_types()  # перезагружаем список


#            # Запятая (self.tree.set(select, '#1'),)) - для удаление при более 10 записей
#            for selection_item in self.connection_types_list.selection():
#                self.db.c_sqlite3.execute(
#                    '''DELETE FROM connection_types WHERE id_connection=?''', (self.connection_types_list.set(selection_item, '#1'),)
#                )
#            self.db.conn_sqlite3.commit()

        else:
            mb.showwarning('Предупреждение', 'Выберите тип подключения')

    def open_new_connection_type(self):
        '''
        Открываем форму ввода нового типа подключения
        '''
        NewConnectionType(self.app)

    def save_new_connection_type(self, connection_type_name, connection_type_description):
        '''
        Процедура сохранения нового типа подключения
        :param connection_type_name: Название тпа подключения
        :param connection_type_description: Комментарий для типа подключения
        :return: none
        '''
        if (len(connection_type_name) == 0):
            mb.showwarning("Предупреждение", "Требуется ввести тип подключения")
            return 'clear'
        else:
            if (self.app.db.get_connection_type_name_by_name(connection_type_name)):  # компания есть, обновляем?
                answer = mb.askyesnocancel(title='Дубль данных',
                                           message='Тип подключения <' + connection_type_name +
                                                   '> уже существует\n\nОбновляем?')
                if (answer):  # если Да = True
                    # Обновляем данные компании и перевыводим список
                    self.app.db.update_connection_type_by_name(connection_type_name, connection_type_description)
                    self.show_connection_types()  # загружаем данные на форму
                    return 'clear'
                elif (answer == False): # если Да = False
                    return 'clear'
                elif (answer is None):  # если Отмена = None
                    return 'cancel'
            else:  # типа подключения нет, сохраняем
                self.app.db.insert_new_connection_type(connection_type_name, connection_type_description)
                self.show_connection_types()  # загружаем данные на форму
                answer = mb.askyesno(title='Данные сохранены', message='Еще новый тип подключения?')
                if (answer):  # если True
                    return 'clear'
                else:  # если False
                    return 'cancel'

    def open_updade_connection_type(self):
        '''
        Открываем окно для обновления выбранного типа подключения
        '''
        if (self.connection_types_list.focus() != ''):
            UpdateConnectionType(self.app)
        else:
            mb.showwarning('Предупреждение', 'Выберите тип подключения')

    def open_connection_type_filter(self):
        '''
        Открываем форму ввода фильтров скиска типов подключения
        :return:
        '''
        FilterConnectionTypes(self.app)

    def apply_connection_type_filter(self, connection_type_name, connection_type_description):
        '''
        Процедура фильтрации по введенным типу подключения и описанию
        :param connection_type_name: Название типа подключения
        :param connection_type_description: Описание типа подключения
        :return none
        '''
        connection_types_filter_dict['connection_type_name'] = connection_type_name  # сохраняем фильтр в словарь
        connection_types_filter_dict['connection_type_description'] = connection_type_description
        self.show_connection_types()  # перезегружаем список

    def clear_connection_type_filter(self):
        for key in connection_types_filter_dict:
            connection_types_filter_dict[key] = ''  # обнуляем ключи
            self.show_connection_types()     # перезегружаем список компаний


class ConnectionType(tk.Toplevel):
    '''
    Базовый класс формы типа подключения
    '''

    def __init__(self, app):
        super().__init__()
        self.init_connection_type()
        self.app = app  # Передаем класс Main
        # self.db = db  # Передаем класс DB
        self.clear_connection_type()

    def init_connection_type(self):
        self.geometry('415x200+400+300')
        self.resizable(False, False)

        # Добавляем функции модального, т.е прехватываем фокус не нем до закрытия
        self.grab_set()
        self.focus_set()

        # Создаем поля формы
        lbl_connection_type_name = tk.Label(self, text='Тип подключения')
        lbl_connection_type_name.place(x=50, y=20)
        self.ent_connection_type_name = ttk.Entry(self)
        self.ent_connection_type_name.place(x=200, y=20, width=180)
        self.ent_connection_type_name.focus()

        lbl_connection_type_description = tk.Label(self, text='Описание')
        lbl_connection_type_description.place(x=50, y=50)
        self.txt_connection_type_description = tk.Text(self)
        self.txt_connection_type_description.place(x=200, y=50, width=180, height=100)

        # Полоса прокрутки
        scroll = tk.Scrollbar(self, command=self.txt_connection_type_description.yview)
        # scroll.pack(side=tk.RIGHT, fill=tk.Y)
        scroll.place(x=380, y=50, height=100)
        self.txt_connection_type_description.configure(yscrollcommand=scroll.set)

        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=305, y=160)

    def clear_connection_type(self):
        self.ent_connection_type_name.delete(0, tk.END)
        self.txt_connection_type_description.delete(1.0, tk.END)


class NewConnectionType(ConnectionType):
    '''
    Класс формы добавления подключения
    '''
    def __init__(self, app):  # Конструктор
        super().__init__(app)
        self.init_new_connection_type()
        self.app = app  # Передаем класс Main
        # self.db = db  # Передаем класс DB
        # self.connection_types = connection_types

    def init_new_connection_type(self):
        self.title('Добавить подключение')

        btn_save = ttk.Button(self, text='Сохранить', command=self.save_new_connection_type_action)
        btn_save.place(x=220, y=160)
        #btn_save.bind('<Button-1>', lambda event: self.main.save_new_connection_type(
        #    self.ent_connection_type_name.get(), self.txt_connection_types_description.get('1.0', tk.END)
        # ))

    def save_new_connection_type_action(self):
        action = self.app.connection_types.save_new_connection_type(
            self.ent_connection_type_name.get(), self.txt_connection_type_description.get('1.0', tk.END)
        )
        if action == 'clear':
            self.clear_connection_type()  # чистим
            self.ent_connection_type_name.focus()  # фокус на имя
        elif action == 'cancel':
            # Имитация клика по btn_cancel
            self.btn_cancel.invoke()
        else:
            self.btn_cancel.invoke()


class UpdateConnectionType(ConnectionType):
    '''
    Класс формы обновления подключений
    '''

    def __init__(self, app):  # Конструктор
        super().__init__(app)
        self.init_update_connection_type()
        self.app = app  # Передаем класс Main
        #self.db = db.DB()  # Передаем класс DB
        self.get_connection_type_for_update()
        # self.connection_types = connection_types


    def init_update_connection_type(self):
        self.title('Обновить подключение')
        btn_save = ttk.Button(self, text='Обновить')
        btn_save.place(x=220, y=160)
        # передаем все поля и id как первый элемент из списка выделенных и порядковый номер столбца
        btn_save.bind('<Button-1>', lambda event: self.app.db.update_connection_type_by_id(
            self.app.connection_types.connection_types_list.set
            (self.app.connection_types.connection_types_list.selection()[0], '#1'), self.ent_connection_type_name.get(),
            self.txt_connection_type_description.get('1.0', tk.END)
         ))
        btn_save.bind('<Button-1>', lambda event: self.app.connection_types.show_connection_types(),
                      add='+')  # вешаем доп событие на кнопку
        btn_save.bind('<Button-1>', lambda event: self.destroy(), add='+')  # вешаем доп событие на кнопку

    def get_connection_type_for_update(self):
        ''' Процедура получения и вывода на форму данных выделенной строки '''
        data = self.app.db.get_connection_type_by_id(self.app.connection_types.connection_types_list.set(
            self.app.connection_types.connection_types_list.selection()[0], '#1'),)
        # Выводим значения в поля формы
        self.ent_connection_type_name.insert(0, data[1])
        self.txt_connection_type_description.insert(1.0, data[2])


class FilterConnectionTypes(tk.Toplevel):
    '''
    Класс формы фильльтра для отображения списка подключений
    '''

    def __init__(self, app):
        super().__init__()

        self.init_filter_connection_type()
        self.app = app  # Передаем класс Main
        #self.db = db.DB()  # Передаем класс DB
        #self.connection_types = connection_types

    def init_filter_connection_type(self):
        self.title('Фильтр типов доступа')
        self.geometry('350x125+400+300')
        self.resizable(False, False)

        # Добавляем функции модального, прехватываем фокус на нем до закрытия
        self.grab_set()
        self.focus_set()

        lbl_connection_type_name = tk.Label(self, text='Тип подключения')
        lbl_connection_type_name.place(x=50, y=20)
        self.ent_connection_type_name = ttk.Entry(self)
        self.ent_connection_type_name.place(x=120, y=20, width=180)
        self.ent_connection_type_name.insert(0, connection_types_filter_dict.get('connection_type_name', ''))  # имя
        self.ent_connection_type_name.focus()

        lbl_connection_type_description = tk.Label(self, text='Описание')
        lbl_connection_type_description.place(x=50, y=50)
        self.ent_connection_type_description = ttk.Entry(self)
        self.ent_connection_type_description.place(x=120, y=50, width=180)
        self.ent_connection_type_description.insert(0, connection_types_filter_dict.get('connection_type_description', '')
                                                    )  # описание

        btn_clear_connection_type_filter = ttk.Button(self, text='Сбросить')
        btn_clear_connection_type_filter.place(x=65, y=85)
        btn_clear_connection_type_filter.bind('<Button-1>', lambda event:
        self.app.connection_types.clear_connection_type_filter())
        btn_clear_connection_type_filter.bind('<Button-1>', lambda event:
        self.destroy(), add='+')  # вешаем второе событие

        btn_apply_connection_type_filter = ttk.Button(self, text='Применить')
        btn_apply_connection_type_filter.place(x=145, y=85)
        btn_apply_connection_type_filter.bind('<Button-1>', lambda event:
        self.app.connection_types.apply_connection_type_filter(
            self.ent_connection_type_name.get(), self.ent_connection_type_description.get()))
        btn_apply_connection_type_filter.bind('<Button-1>', lambda event: self.destroy(), add='+') # вешаем доп событие

        btn_closed_connection_type_filter = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_closed_connection_type_filter.place(x=225, y=85)