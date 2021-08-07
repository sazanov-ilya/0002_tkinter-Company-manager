import sqlite3
import tkinter.messagebox as mb

class DB:
    """ Класс подвлючения к БД sqlite3 """
    def __init__(self):
        # self.root = root  # Передаем класс Main
        self.conn_sqlite3 = sqlite3.connect('company_manager.db')
        self.c_sqlite3 = self.conn_sqlite3.cursor()
        # Для каскадного удаления
        self.c_sqlite3.execute("PRAGMA foreign_keys=ON")

        #####################
        # Таблица companies #
        #####################
        try:
            self.c_sqlite3.execute(
                '''CREATE TABLE IF NOT EXISTS companies (id_company integer primary key autoincrement not null,
                company_name text, company_description text)'''
            )
            self.conn_sqlite3.commit()
        except sqlite3.Error as err:
            print('Ошибка: ' + err.__str__())
            # self.root.destroy()
            # sys.exit()
            # raise SystemExit
            # exit()
            # ??? self.master.title("Оставить отзыв")
            #self.master.destroy()

        ############################
        # Таблица connection_types #
        ############################
        try:
            self.c_sqlite3.execute(
                '''CREATE TABLE IF NOT EXISTS connection_types 
                (id_connection_type integer primary key autoincrement not null, connection_type_name text,
                connection_type_description text)'''
            )
            self.conn_sqlite3.commit()
        except sqlite3.Error as err:
            mb.showerror("ОШИБКА!", err.__str__())
            # self.root.destroy()

        #######################
        # Таблица connections #
        #######################
        try:
            self.c_sqlite3.execute(
                '''CREATE TABLE IF NOT EXISTS connections (id_connection integer primary key autoincrement not null,
                id_company integer,id_connection_type integer, connection_ip text, connection_description text,
                FOREIGN KEY(id_company) REFERENCES companies(id_company) ON DELETE CASCADE,
                FOREIGN KEY(id_connection_type) REFERENCES connection_types(id_connection_type) ON DELETE CASCADE)'''
            )
            self.conn_sqlite3.commit()
        except sqlite3.Error as err:
            mb.showerror("ОШИБКА!", err.__str__())
            #self.root.destroy()

        ##################
        # Таблица logins #
        ##################
        try:
            self.c_sqlite3.execute(
                '''CREATE TABLE IF NOT EXISTS logins (id_login integer primary key autoincrement not null,
                id_connection integer, login_name text, login_password text, login_description text,
                FOREIGN KEY(id_connection) REFERENCES connections(id_connection) ON DELETE CASCADE)'''
            )
            self.conn_sqlite3.commit()
        except sqlite3.Error as err:
            mb.showerror("ОШИБКА!", err.__str__())
            # self.root.destroy()

    #####################
    # Таблица companies #
    #####################
    def get_company_by_id(self, id_company):
        """ Процедура возврата данных компании по переданному id
        :param id_company:
        :return: No
        """
        try:
            self.c_sqlite3.execute(
                '''SELECT id_company, company_name, company_description FROM companies WHERE id_company=?''',
                [id_company]
            )
        except sqlite3.Error as err:
            mb.showerror("ОШИБКА!", err.__str__())
            # self.root.destroy()
        data = self.c_sqlite3.fetchone()  # возвращает только одну запись
        return data

    def get_company_name_by_name(self, company_name):
        """ Процедура проверки наличия компании по ее имени
        :param company_name: Название компании
        :return: company_name/None
        """
        company_name = (company_name.lower(),)
        try:
            self.c_sqlite3.execute(
                '''SELECT company_name FROM companies WHERE LOWER(company_name) = ?''', company_name
            )
        except sqlite3.Error as err:
            mb.showerror("ОШИБКА!", err.__str__())
            # self.root.destroy()
        data = self.c_sqlite3.fetchone()
        if data is not None:
            return data[0]
        else:
            return None

    def get_company_list_by_filter(self, company_name, company_description):
        """ Процедура возврата результата списка компаний согласно фильтров
        :param company_name: Фильтр по названию компании
        :param company_description: Фильтр по описанию для компании
        :return: набор кортежей со списком компаний согласно фильтров
        """
        if (company_name and company_description):  # проверяем фильтр
            company_filter_name = ('%' + company_name.lower() + '%')
            company_filter_description = ('%' + company_description.lower() + '%')
            try:
                self.c_sqlite3.execute(
                    '''SELECT id_company, company_name, company_description FROM companies WHERE company_name LIKE ?
                    AND company_description LIKE ?''',
                    [company_filter_name, company_filter_description]
                )
            except sqlite3.Error as err:
                mb.showerror("ОШИБКА!", err.__str__())
                # self.root.destroy()
        elif (company_name):  # Проверяем фильтр
            company_filter_name = ('%' + company_name.lower() + '%')
            # company_filter_description = ('%' + company_filter_description.lower() + '%',)

            # рабочий
            # company_filter_name = ('%' + company_filter_name.lower() + '%',)
            # self.db.c_sqlite3.execute(
            #    '''SELECT id_company, company_name, company_description FROM companies WHERE company_name LIKE ?''',
            #    (company_filter_name)
            # )

            try:
                self.c_sqlite3.execute(
                    '''SELECT id_company, company_name, company_description FROM companies WHERE company_name LIKE ?''',
                    [company_filter_name]
                )
            except sqlite3.Error as err:
                mb.showerror("ОШИБКА!", err.__str__())
                # self.root.destroy()
        elif (company_description):  # Проверяем фильтр
            # company_filter_name = ('%' + company_filter_name.lower() + '%',)
            company_filter_description = ('%' + company_description.lower() + '%')
            try:
                self.c_sqlite3.execute(
                    '''SELECT id_company, company_name, company_description FROM companies 
                    WHERE company_description LIKE ?''',[company_filter_description]
                )
            except sqlite3.Error as err:
                mb.showerror("ОШИБКА!", err.__str__())
                # self.root.destroy()
        else:
            try:
                self.c_sqlite3.execute(
                    '''SELECT id_company, company_name, company_description FROM companies'''
                )
            except sqlite3.Error as err:
                mb.showerror("ОШИБКА!", err.__str__())
                # self.root.destroy()
        data = []  # запрос возвращает набор кортежей
        [data.append(row) for row in self.c_sqlite3.fetchall()]
#        [self.companies_list.insert('', 'end', values=row) for row in self.db.c_sqlite3.fetchall()]
        return data

    def get_company_for_list(self):
        """ Процедура возвращает список компаний для выпадающего списка
        :return: набор кортежей id и company_name
        """
        try:
            self.c_sqlite3.execute(
                '''SELECT id_company, company_name FROM companies'''
            )
        except sqlite3.Error as err:
            mb.showerror("ОШИБКА!", err.__str__())
            # self.root.destroy()

        data = []  # запрос возвращает набор кортежей
        [data.append(row) for row in self.c_sqlite3.fetchall()]
        return data

    def insert_new_company(self, company_name, company_description):
        """ Процедура сохранения данных новой компании
        :param company_name: Название компании
        :param company_description: Описание для компании
        :return: No
        """
        try:
            self.c_sqlite3.execute(
                '''INSERT INTO companies(company_name, company_description) VALUES(?, ?)''',
                (company_name.lower(), company_description)
            )
            self.conn_sqlite3.commit()
        except sqlite3.Error as err:
            mb.showerror("ОШИБКА!", err.__str__())
            # self.root.destroy()

    def update_company_by_name(self, company_name, company_description):
        """ Процедура обновления данных компании по ее имени
        :param company_name: Название компании
        :param company_description: Комментарий для компании
        :return: No
        """
        try:
            self.c_sqlite3.execute(
                '''UPDATE companies SET company_name=?, company_description=? WHERE LOWER(company_name) = ?''',
                (company_name.lower(), company_description, company_name.lower())
            )
            self.conn_sqlite3.commit()
        except sqlite3.Error as err:
            mb.showerror("ОШИБКА!", err.__str__())
            # self.root.destroy()

    def update_company_by_id(self, id_company, company_name, company_description):
        """ Процедура обновления данных компании по ее id
        :param id_company: Id компании
        :param company_name: Название компании
        :param company_description: Комментарий для компании
        :return No
        """
        try:
            self.c_sqlite3.execute(
                '''UPDATE companies SET company_name=?, company_description=? WHERE id_company=?''',
                (company_name, company_description, id_company)
            )
            self.conn_sqlite3.commit()
        except sqlite3.Error as err:
            mb.showerror("ОШИБКА!", err.__str__())
            # self.root.destroy()

    def delete_companies(self, ids):
        """ Процедура удаления выбранных в списке компаний
        :param ids: Список id компаний
        :return: No
        """
        try:
            for id in ids:
                self.c_sqlite3.execute(
                    '''DELETE FROM companies WHERE id_company=?''', [id]
                    )
                self.conn_sqlite3.commit()
        except sqlite3.Error as err:
            mb.showerror("ОШИБКА!", err.__str__())
            # self.root.destroy()

    ############################
    # Таблица connection_types #
    ############################
    def get_connection_type_by_id(self, id_connection_type):
        """ Процедура возврата данных типа подключения по переданному id
        :param id_connection_type: id типа подключения
        :return: возвращает только одну запись по id
        """
        try:
            self.c_sqlite3.execute(
                '''SELECT id_connection_type, connection_type_name, connection_type_description
                FROM connection_types WHERE id_connection_type=?''', [id_connection_type]
            )
        except sqlite3.Error as err:
            mb.showerror("ОШИБКА!", err.__str__())
            # self.root.destroy()
        data = self.c_sqlite3.fetchone()  # возвращает только одну запись
        return data

    def get_connection_type_name_by_name(self, connection_type_name):
        """ Процедура проверки наличия типа подключения по его имени
        :param connection_type_name: Название типа подключения
        :return: connection_type_name/None
        """
        connection_type_name = (connection_type_name.lower(),)
        try:
            self.c_sqlite3.execute(
                '''SELECT connection_type_name FROM connection_types WHERE LOWER(connection_type_name) = ?''',
                connection_type_name
            )
        except sqlite3.Error as err:
            mb.showerror("ОШИБКА!", err.__str__())
        # self.root.destroy()
        data = self.c_sqlite3.fetchone()
        if data is not None:
            return data[0]
        else:
            return None

    def get_connection_type_list_by_filter(self, connection_type_name, connection_type_description):
        """ Процедура возврата результата списка типов подключения согласно переданных фильтров
        :param connection_type_name: Фильтр по названию типа подключения
        :param connection_type_description: Фильтр по описанию для типа подключения
        :return: набор кортежей со списком компаний согласно фильтров
        """
        if (connection_type_name and connection_type_description):  # проверяем фильтр
            connection_type_filter_name = ('%' + connection_type_name.lower() + '%')
            connection_type_filter_description = ('%' + connection_type_description.lower() + '%')
            try:
                self.c_sqlite3.execute(
                    '''SELECT id_connection_type, connection_type_name, connection_type_description
                    FROM connection_types WHERE connection_type_name LIKE ?
                    AND connection_type_description LIKE ?''',
                    [connection_type_filter_name, connection_type_filter_description]
                )
            except sqlite3.Error as err:
                mb.showerror("ОШИБКА!", err.__str__())
                # self.root.destroy()
        elif (connection_type_name):  # Проверяем фильтр
            connection_type_filter_name = ('%' + connection_type_name.lower() + '%')
            # connection_type_filter_description = ('%' + connection_type_filter_description.lower() + '%',)

            # рабочий
            # connection_type_filter_name = ('%' + connection_type_filter_name.lower() + '%',)
            # self.db.c_sqlite3.execute(
            #    '''SELECT id_connection_type, connection_name, connection_type_description
            #    FROM connection_types WHERE connection_type_name LIKE ?''',
            #    (connection_type_filter_name)
            # )

            try:
                self.c_sqlite3.execute(
                    '''SELECT id_connection_type, connection_type_name, connection_type_description
                    FROM connection_types WHERE connection_type_name LIKE ?''',
                    [connection_type_filter_name]
                )
            except sqlite3.Error as err:
                mb.showerror("ОШИБКА!", err.__str__())
                # self.root.destroy()
        elif (connection_type_description):  # Проверяем фильтр
            # connection_type_filter_name = ('%' + connection_type_filter_name.lower() + '%',)
            connection_type_filter_description = ('%' + connection_type_description.lower() + '%')
            try:
                self.c_sqlite3.execute(
                    '''SELECT id_connection_type, connection_type_name, connection_type_description
                    FROM connection_types WHERE connection_type_description LIKE ?''',
                    [connection_type_filter_description]
                )
            except sqlite3.Error as err:
                mb.showerror("ОШИБКА!", err.__str__())
                # self.root.destroy()
        else:
            try:
                self.c_sqlite3.execute(
                    '''SELECT id_connection_type, connection_type_name, connection_type_description 
                    FROM connection_types'''
                )
            except sqlite3.Error as err:
                mb.showerror("ОШИБКА!", err.__str__())
                # self.root.destroy()

        data = []  # запрос возвращает набор кортежей
        [data.append(row) for row in self.c_sqlite3.fetchall()]
        # [self.connection_types_list.insert('', 'end', values=row) for row in self.db.c_sqlite3.fetchall()]
        return data

    def get_connection_type_for_list(self):
        """ Процедура возвращает список типов подключений
        :return: набор кортежей id и connection_type_name
        """
        try:
            self.c_sqlite3.execute(
                '''SELECT id_connection_type, connection_type_name FROM connection_types'''
            )
        except sqlite3.Error as err:
            mb.showerror("ОШИБКА!", err.__str__())
            # self.root.destroy()

        data = []  # запрос возвращает набор кортежей
        [data.append(row) for row in self.c_sqlite3.fetchall()]
        return data

    def insert_new_connection_type(self, connection_type_name, connection_type_description):
        """ Процедура сохранения нового типа подключения
        :param connection_type_name:
        :param connection_type_description:
        :return: No
        """
        try:
            self.c_sqlite3.execute(
                '''INSERT INTO connection_types(connection_type_name, connection_type_description) VALUES(?, ?)''',
                (connection_type_name.lower(), connection_type_description)
            )
            self.conn_sqlite3.commit()
        except sqlite3.Error as err:
            mb.showerror("ОШИБКА!", err.__str__())

    def update_connection_type_by_name(self, connection_type_name, connection_type_description):
        """ Процедура обновления данных типа подключения по его имени
        :param connection_type_name: Название типа подключения
        :param connection_type_description: Комментарий для типа подключения
        :return: No
        """
        try:
            self.c_sqlite3.execute(
                '''UPDATE connection_types SET connection_type_name=?, connection_type_description=? 
                WHERE LOWER(connection_type_name) = ?''',
                (connection_type_name.lower(), connection_type_description, connection_type_name.lower())
            )
            self.conn_sqlite3.commit()
        except sqlite3.Error as err:
            mb.showerror("ОШИБКА!", err.__str__())

    def update_connection_type_by_id(self, id_connection_type, connection_type_name, connection_type_description):
        """ Процедура обновления данных первого выделенного в списке типа подключения
        :param connection_type_name: Название типа подключения
        :param connection_type_description: Комментарий для типа подключения
        :return No
        """
        try:
            self.c_sqlite3.execute(
                '''UPDATE connection_types SET connection_type_name=?, connection_type_description=?
                WHERE id_connection_type=?''',
                (connection_type_name, connection_type_description, id_connection_type)
            )
            self.conn_sqlite3.commit()
        except sqlite3.Error as err:
            mb.showerror("ОШИБКА!", err.__str__())

    def delete_connection_types(self, ids):
        """ Процедура удаления выбранных типов подключения
        :param ids: Список id типов подключения
        :return: No
        """
        try:
            for id in ids:
                self.c_sqlite3.execute(
                    '''DELETE FROM connection_types WHERE id_connection_type=?''', [id]
                )
                self.conn_sqlite3.commit()
        except sqlite3.Error as err:
            mb.showerror("ОШИБКА!", err.__str__())

    #######################
    # Таблица connections #
    #######################
    def get_connection_by_id(self, id_connection):
        """ Процедура возврата данных подключения по переданному id_connection
        :param id_connection: id подключения
        :return: возвращает только одну запись по id
        """
        try:
            self.c_sqlite3.execute(
                '''SELECT id_connection, id_company, id_connection_type, connection_ip, connection_description
                FROM connections WHERE id_connection=?''', [id_connection]
            )
        except sqlite3.Error as err:
            mb.showerror("ОШИБКА!", err.__str__())
            # self.root.destroy()
        data = self.c_sqlite3.fetchone()  # возвращает только одну запись
        return data

    def get_company_connection_type_by_id_connection(self, id_connection):
        """ Процедура возвращает названия компании и типа подключения по id_connection
        :param id_connection:
        :return: названия компании и тип подклюжчения
        """
        try:
            self.c_sqlite3.execute(
                '''SELECT connections.id_connection, companies.company_name, connection_types.connection_type_name
                FROM connections, companies, connection_types
                WHERE  connections.id_company=companies.id_company
                AND connections.id_connection_type = connection_types.id_connection_type
                AND connections.id_connection = ?''', [id_connection]
            )
        except sqlite3.Error as err:
            mb.showerror("ОШИБКА!", err.__str__())
            # self.root.destroy()
        data = self.c_sqlite3.fetchone()  # возвращает только одну запись
        return data

    def get_connection_for_update_by_id(self, id_connection):
        """ Процедура возвращает данные подключения для формы обновления по id_connection
        :param id_connection:
        :return: названия компании и тип подклюжчения
        """
        try:
            self.c_sqlite3.execute(
                '''SELECT connections.id_connection, companies.company_name, connection_types.connection_type_name,
                connections.connection_ip, connections.connection_description
                FROM connections, companies, connection_types
                WHERE  connections.id_company=companies.id_company
                AND connections.id_connection_type = connection_types.id_connection_type
                AND connections.id_connection = ?''', [id_connection]
            )
        except sqlite3.Error as err:
            mb.showerror("ОШИБКА!", err.__str__())
            # self.root.destroy()
        data = self.c_sqlite3.fetchone()  # возвращает только одну запись
        return data

    def get_connections_by_filter(self, id_company, id_connection_type, connection_ip, connection_description):
        """ Процедура возврата списка подключений согласно фильтра
        :param id_company: Фильтр по id_company
        :param id_connection_type: Фильтр по id_connection_type
        :param connection_ip: Фильтр по Ip-адрес/домен через LIKE
        :param connection_description: Фильтр по Описанию через LIKE
        :return: набор кортежей со списком подключений согласно фильтров
        """
        if (id_company and id_connection_type):  # компания и тип
            #company_filter_name = ('%' + company_name.lower() + '%')
            #company_filter_description = ('%' + company_description.lower() + '%')
            try:
                self.c_sqlite3.execute(
                    '''SELECT connections.id_connection, companies.company_name, connection_types.connection_type_name,
                    connections.connection_ip, connections.connection_description
                    FROM connections, companies, connection_types
                    WHERE connections.id_company = companies.id_company and 
                    connections.id_connection_type = connection_types.id_connection_type and
                    connections.id_company = ? and connections.id_connection_type = ?''',
                    [id_company, id_connection_type]
                )
            except sqlite3.Error as err:
                mb.showerror("ОШИБКА!", err.__str__())
                # self.root.destroy()
        elif (id_company):  # только компания
            # company_filter_name = ('%' + company_name.lower() + '%')
            # company_filter_description = ('%' + company_filter_description.lower() + '%',)
            try:
                self.c_sqlite3.execute(
                    '''SELECT connections.id_connection, companies.company_name, connection_types.connection_type_name,
                    connections.connection_ip, connections.connection_description
                    FROM connections, companies, connection_types
                    WHERE connections.id_company = companies.id_company and 
                    connections.id_connection_type = connection_types.id_connection_type and
                    connections.id_company = ? ''',
                    [id_company]
                )
            except sqlite3.Error as err:
                mb.showerror("ОШИБКА!", err.__str__())
                # self.root.destroy()
        elif (id_connection_type):  # только тип
            # company_filter_name = ('%' + company_filter_name.lower() + '%',)
            # company_filter_description = ('%' + company_description.lower() + '%')
            try:
                self.c_sqlite3.execute(
                    '''SELECT connections.id_connection, companies.company_name, connection_types.connection_type_name,
                    connections.connection_ip, connections.connection_description
                    FROM connections, companies, connection_types
                    WHERE connections.id_company = companies.id_company and 
                    connections.id_connection_type = connection_types.id_connection_type and
                    connections.id_connection_type = ?''',
                    [id_connection_type]
                )
            except sqlite3.Error as err:
                mb.showerror("ОШИБКА!", err.__str__())
                # self.root.destroy()
        else:
            try:
                self.c_sqlite3.execute(
                    '''SELECT connections.id_connection, companies.company_name, connection_types.connection_type_name,
                    connections.connection_ip, connections.connection_description
                    FROM connections, companies, connection_types
                    WHERE connections.id_company = companies.id_company and 
                    connections.id_connection_type = connection_types.id_connection_type'''
                )
            except sqlite3.Error as err:
                mb.showerror("ОШИБКА!", err.__str__())
                # self.root.destroy()
        data = []  # запрос возвращает набор кортежей
        [data.append(row) for row in self.c_sqlite3.fetchall()]
        return data

    def get_connection_ip_for_check_exists(self, id_company, id_connection_type, connection_ip):
        """ Процедура проверки наличия подключения по компании, типу подключения и ip/домену (проверка на дубль)
        :param id_company:
        :param id_connection_type:
        :param connection_ip:
        :return: connection_ip/None
        """
        try:
            self.c_sqlite3.execute(
                '''SELECT connection_ip FROM connections WHERE id_company = ? and
                id_connection_type = ? and connection_ip = ?''',
                [id_company, id_connection_type, connection_ip.lower()]
            )
        except sqlite3.Error as err:
            mb.showerror("ОШИБКА!", err.__str__())
            # self.root.destroy()
        data = self.c_sqlite3.fetchone()
        if data is not None:
            return data[0]
        else:
            return None

    def insert_new_connection(self, id_company, id_connection_type, connection_ip, connection_description):
        """ Процедура сохранения нового подключения
        :param id_company:
        :param id_connection_type:
        :param connection_ip:
        :param connection_description:
        :return: No
        """
        try:
            self.c_sqlite3.execute(
                '''INSERT INTO connections(id_company, id_connection_type, connection_ip, connection_description) 
                VALUES(?, ?, ?, ?)''',
                (id_company, id_connection_type, connection_ip.lower(), connection_description)
            )
            self.conn_sqlite3.commit()
        except sqlite3.Error as err:
            mb.showerror("ОШИБКА!", err.__str__())

    def update_connection_by_id(self, id_connection, connection_ip, connection_description):
        """ Процедура обновления подключения по id_connection
        :param id_connection:
        :param connection_ip:
        :param connection_description:
        :return: No
        """
        try:
            self.c_sqlite3.execute(
                '''UPDATE connections SET connection_ip=?, connection_description=?
                WHERE id_connection=?''',
                (connection_ip, connection_description, id_connection)
            )
            self.conn_sqlite3.commit()
        except sqlite3.Error as err:
            mb.showerror("ОШИБКА!", err.__str__())

    # curs.execute("SELECT weight FROM Equipment WHERE name = :name AND price = :price",
    #         {name: 'lead', price: 24})



    def delete_connections(self, ids):
        """ Процедура удаления подключений
        :param ids: Список id подключений
        :return: No
        """
        try:
            for id in ids:
                self.c_sqlite3.execute(
                    '''DELETE FROM connections WHERE id_connection=?''', [id]
                )
                self.conn_sqlite3.commit()
        except sqlite3.Error as err:
            mb.showerror("ОШИБКА!", err.__str__())

    ##################
    # Таблица logins #
    ##################
    def get_login_by_id(self, id_login):
        """ Процедура возврата данных логина по переданному id_login
        :param id_login:
        :return: Кортеж значений
        """
        try:
            self.c_sqlite3.execute(
                '''SELECT id_login, login_name, login_password, login_description 
                FROM logins WHERE id_login=?''', [id_login]
            )
        except sqlite3.Error as err:
            mb.showerror("ОШИБКА!", err.__str__())
            # self.root.destroy()
        data = self.c_sqlite3.fetchone()  # возвращает только одну запись
        return data

    def get_logins_list_by_id_connection(self, id_connection):
        """ Процедура возврата списка логинов по id_connection (вывод на форму)
        :param id_connection:
        :return: Набор кортежей со списком логинов согласно фильтров
        """
        try:
            self.c_sqlite3.execute(
                '''SELECT id_login, login_name, login_password, login_description
                FROM logins WHERE id_connection = ?''',
                [id_connection]
            )
        except sqlite3.Error as err:
            mb.showerror("ОШИБКА!", err.__str__())
            # self.root.destroy()
        data = []  # запрос возвращает набор кортежей
        [data.append(row) for row in self.c_sqlite3.fetchall()]
        return data

    def get_login_name_for_check_exists(self, id_connection, login_name):
        """ Процедура проверки наличия логина по id_connection и login_name (проверка на дубль)
        :param id_connection:
        :param login_name:
        :return: login_name/None
        """
        try:
            self.c_sqlite3.execute(
                '''SELECT login_name FROM logins WHERE id_connection = ? and LOWER(login_name) = ?''',
                [id_connection, login_name.lower()]
            )
        except sqlite3.Error as err:
            mb.showerror("ОШИБКА!", err.__str__())
            # self.root.destroy()
        data = self.c_sqlite3.fetchone()
        if data is not None:
            return data[0]
        else:
            return None

    def insert_new_login(self, id_connection, login_name, login_password, login_description):
        """ Процедура сохранения нового логина для подключения через id_connection
        :param id_connection:
        :param login_name:
        :param login_password:
        :param login_description:
        :return: No
        """
        try:
            self.c_sqlite3.execute(
                '''INSERT INTO logins(id_connection, login_name, login_password, login_description)
                VALUES(?, ?, ?, ?)''', (id_connection, login_name, login_password, login_description)
            )
            self.conn_sqlite3.commit()
        except sqlite3.Error as err:
            mb.showerror("ОШИБКА!", err.__str__())
            # self.root.destroy()

    def update_login_by_id(self, id_login, login_name, login_password, login_description):
        """ Процедура обновления логина по id_login
        :param id_login:
        :param login_name:
        :param login_password:
        :param login_description:
        :return: No
        """
        try:
            self.c_sqlite3.execute(
                '''UPDATE logins SET login_name=?, login_password=?, login_description=?
                WHERE id_login=?''',
                (login_name, login_password, login_description, id_login)
            )
            self.conn_sqlite3.commit()
        except sqlite3.Error as err:
            mb.showerror("ОШИБКА!", err.__str__())

    def delete_logins(self, ids):
        """ Процедура удаления логинов
        :param ids: Список id логинов
        :return:
        """
        try:
            for id in ids:
                self.c_sqlite3.execute(
                    '''DELETE FROM logins WHERE id_login=?''', [id]
                )
                self.conn_sqlite3.commit()
        except sqlite3.Error as err:
            mb.showerror("ОШИБКА!", err.__str__())


    # стиль qmark
    #curs.execute("SELECT weight FROM Equipment WHERE name = ? AND price = ?",
    #             ['lead', 24])

    # названный стиль
    #curs.execute("SELECT weight FROM Equipment WHERE name = :name AND price = :price",
    #         {name: 'lead', price: 24})

    # Именованные параметры
    # sql = "SELECT column FROM table WHERE col1=%s AND col2=%s"
    # params = (col1_value, col2_value)
    # cursor.execute(sql, params)


#    # пример 1
#    try:
#        cursor.execute("INSERT INTO ...", params)
#    except sqlite3.Error as err:
#        logger.error(err.message)

#    # пример 2
#    import sqlite3 as lite
#
#    con = lite.connect('test.db')
#
#    with con:
#        cur = con.cursor()
#        cur.execute("CREATE TABLE Persons(Id INT, Name TEXT)")
#        cur.execute("INSERT INTO Persons VALUES(1,'Joe')")
#        cur.execute("INSERT INTO Persons VALUES(1,'Jenny')")
#
#        try:
#            cur.execute("INSERT INTO Persons VALUES(1,'Jenny', 'Error')")
#            self.con.commit()
#
#        except lite.Error as er:
#            print
#            'er:', er.message
#
#        # Retrieve data
#        cur.execute("SELECT * FROM Persons")
#        rows = cur.fetchall()
#        for row in rows:
#            print
#            row