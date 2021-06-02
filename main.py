import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
# import tkinter.ttk as ttk
import sqlite3


# Класс основной формы
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        # Передаем класс DB
        self.db = db

    def init_main(self):
        # Стили
        self.style = ttk.Style()
        self.style.theme_use("default")

        # Главная рамка
        # Поле для ввода данных растянуто горизонтально с параметрами fill и expand
        self.pack(fill=tk.BOTH, expand=True)

        # Рамка для toolbar
        frm_main_toolbar = ttk.Frame(self, relief=tk.RAISED, borderwidth=3)  # GROOVE
        frm_main_toolbar.pack(fill=tk.X)

        # Кнопки меню с картинками
        self.new_company_img = tk.PhotoImage(file='new_company.gif')
        btn_open_new_company = tk.Button(frm_main_toolbar, text='Добавить компанию', bg='#d7d8e0', bd=0
                                         , compound=tk.BOTTOM, image=self.new_company_img
                                         , command=self.open_new_company)
        btn_open_new_company.pack(side=tk.LEFT)

        self.company_img = tk.PhotoImage(file='new_company.gif')
        btn_open_test = tk.Button(frm_main_toolbar, text='Компании', bg='#d7d8e0', bd=0, compound=tk.BOTTOM,
                                  image=self.company_img, command=self.open_companies)
        btn_open_test.pack(side=tk.LEFT)

        self.frm_content_all_clear_img = tk.PhotoImage(file='new_company.gif')
        btn_content_all_clear = tk.Button(frm_main_toolbar, text='Тест удаления', bg='#d7d8e0', bd=0,
                                          compound=tk.BOTTOM,
                                          image=self.frm_content_all_clear_img, command=self.clear_frm_content_all)
        btn_content_all_clear.pack(side=tk.LEFT)

        # Рамка сожержимого
        ##self.master = root
        self.frm_content_all = ttk.Frame(self, relief=tk.RAISED, borderwidth=3)
        self.frm_content_all.pack(fill=tk.BOTH, anchor=tk.N, expand=True)

        # lbl2 = ttk.Label(frm_content_all, text="frm_content_all", width=10)
        # lbl2.pack(fill=tk.X, padx=5, expand=True)

    ## Работает 1
    # def content_all_clear(self):
    #    self.frm_content_all.pack_forget()

    # Работает 2
    def clear_frm_content_all(self):
        for widget in self.frm_content_all.winfo_children():
            # widget.pack_forget()
            widget.destroy()

    # def content_all_clear(frm_companies):
    #    widgets = root.grid_slaves()
    #    for widget in widgets:
    #        if widget.winfo_name() == 'frm_companies':
    #            widget.destroy()
    #            #widget.pack_forget()

    def open_companies(self):
        # self.pack(fill=tk.BOTH, expand=True)

        self.clear_frm_content_all()
        Companies()

    def open_new_company(self):
        CompanyNew()


class Companies(tk.Frame):
    def __init__(self):
        super().__init__(root)
        self.init_companies()
        self.main = app  # Передаем класс Main
        self.db = db  # Передаем класс DB
        self.companies_show()  # Загружаем данные на форму

    def init_companies(self):
        # self.pack(fill=tk.BOTH, expand=True)
        # Базовая рамка для модуля
        frm_companies = ttk.Frame(app.frm_content_all, relief=tk.RAISED, borderwidth=3)
        frm_companies.pack(fill=tk.BOTH, expand=True)

        # Рамка toolbar модуля
        frm_companies_toolbar = ttk.Frame(frm_companies, relief=tk.RAISED, borderwidth=0)
        frm_companies_toolbar.pack(fill=tk.X)

        # Кнопки
        btn_open_company_new = tk.Button(frm_companies_toolbar, text='Добавить компанию', bg='#d7d8e0',
                                         bd=0, compound=tk.BOTTOM, relief=tk.GROOVE, borderwidth=5,
                                         pady=2, padx=2, command=self.open_new_company)
        btn_open_company_new.pack(side=tk.LEFT)

        btn_open_company_update = tk.Button(frm_companies_toolbar, text='Обновить компанию', bg='#d7d8e0',
                                            bd=0, compound=tk.BOTTOM, relief=tk.GROOVE, borderwidth=5,
                                            pady=2, padx=2)
        btn_open_company_update.pack(side=tk.LEFT)

        # Рамка контента модуля
        frm_companies_content = ttk.Frame(frm_companies, relief=tk.RAISED, borderwidth=3)
        frm_companies_content.pack(fill=tk.BOTH, expand=True)

        # Treeview для списка
        self.tree = ttk.Treeview(frm_companies_content, columns=('id_company', 'company_name', 'company_description'),
                                 height=10, show='headings')
        # Параметры к колонкам
        self.tree.column("id_company", width=40, anchor=tk.CENTER)
        self.tree.column("company_name", width=150, anchor=tk.CENTER)
        self.tree.column("company_description", width=355, anchor=tk.CENTER)
        # Названия колонкам
        self.tree.heading('id_company', text='ID')
        self.tree.heading('company_name', text='Наименование')
        self.tree.heading('company_description', text='Описание')
        # Вывод в главное окно с выравниванием по левой стороне
        self.tree.pack(fill=tk.BOTH, anchor=tk.N, expand=True)

        ## Рамка для toolbar
        # frm_toolbar = tk.Frame(frm_companies, bg='#d7d8e0', bd=4, relief=tk.GROOVE)
        # frm_toolbar.pack(side=tk.TOP, fill=tk.X)

    # Функция вывода списка компаний форму
    def companies_show(self):
        self.db.c.execute(
            '''SELECT id_company, company_name, company_description FROM companies'''
        )
        # Очистка таблицы
        [self.tree.delete(i) for i in self.tree.get_children()]
        # Перезагргузка таблицы
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def open_new_company(self):
        #CompanyNew()
        #Company()
        CompanyNew()


# Базовый класс формы компании
class Company(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_company()
        #self.main = app  # Передаем класс Main
        self.db = db  # Передаем класс DB
        #self.company_clear()

    def init_company(self):
        self.title('Добавить компанию')
        self.geometry('415x200+400+300')
        self.resizable(False, False)

        # Создаем поля формы
        # self.entery_new_company = tk.Entry(self, width=40, bg="white", fg="black")
        # self.entery_new_company.place(x=200, y=20, width=180)

        lbl_company_name = tk.Label(self, text='Название компании')
        lbl_company_name.place(x=50, y=20)
        self.ent_company_name = ttk.Entry(self)
        self.ent_company_name.place(x=200, y=20, width=180)

        lbl_company_description = tk.Label(self, text='Описание')
        lbl_company_description.place(x=50, y=50)
        self.txt_company_description = tk.Text(self)
        self.txt_company_description.place(x=200, y=50, width=180, height=100)

        # Полоса прокрутки
        scroll = tk.Scrollbar(self, command=self.txt_company_description.yview)
        # scroll.pack(side=tk.RIGHT, fill=tk.Y)
        scroll.place(x=380, y=50, height=100)
        self.txt_company_description.configure(yscrollcommand=scroll.set)

        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=305, y=160)

        #btn_save = ttk.Button(self, text='Сохранить')
        #btn_save.place(x=220, y=160)
        #btn_save.bind('<Button-1>', lambda event: self.company_save(
        #    self.ent_company_name.get(), self.txt_company_description.get('1.0', tk.END)
        #))
        self.grab_set()
        self.focus_set()

    def company_clear(self):
        self.ent_company_name.delete(0, tk.END)
        self.txt_company_description.delete(1.0, tk.END)


# Класс формы добавления компании
class CompanyNew(Company):
    def __init__(self): # Конструктор
        super().__init__()
        self.init_edit()
        #self.main = app  # Передаем класс Main
        self.db = db  # Передаем класс DB
        #self.companies = companies
        #self.company = company

    def init_edit(self):
        self.title('Добавить компанию')

        btn_save = ttk.Button(self, text='Сохранить')
        btn_save.place(x=220, y=160)
        btn_save.bind('<Button-1>', lambda event: self.company_save(
            self.ent_company_name.get(), self.txt_company_description.get('1.0', tk.END)
         ))

    def company_save(self, company_name, company_description):
        if (len(company_name) == 0):
            mb.showwarning("Предупреждение", "Требуется ввести название компании")
        else:
            if (self.company_get_by_name(self.ent_company_name.get())):  # Компания уже есть
                #  mb.showwarning("Предупреждение", 'Компания найдена:  ' +
                #               self.get_company_by_name(self.ent_company_name.get()))
                answer = mb.askyesnocancel(title='Найдена компания - ' +
                                                 self.company_get_by_name(self.ent_company_name.get()),
                                           message="Обновить?")
                if (answer):  # Если True
                    self.company_update_by_name(company_name, company_description)
                    #self.company_clear()
                    #self.companies.companies_show()
                elif (answer is None):  # Если None
                    # Имитация клмка по btn_cancel
                    self.btn_cancel.invoke()
            else:  # Компании нет, сохраняем
                self.company_insert(company_name, company_description)
                answer = mb.askyesno(title='Данные сохранены', message='Еще новый клиент?')
                if (answer):  # Если True
                    self.company_clear()
                else:  # Если False
                    # Имитация клмка по btn_cancel
                    self.btn_cancel.invoke()

    def company_get_by_name(self, company_name):
        company_name = (company_name.lower(),)
        self.db.c.execute(
            '''SELECT company_name FROM companies WHERE LOWER(company_name) = ?''', company_name
        )
        row = self.db.c.fetchone()
        if row is not None:
            return row[0]
        else:
            return None

    def company_update_by_name(self, company_name, company_description):
        self.db.c.execute(
            '''UPDATE companies SET company_name=?, company_description=? WHERE LOWER(company_name) = ?''',
            (company_name.lower(), company_description, company_name.lower())
        )
        self.db.conn.commit()

    def company_insert(self, company_name, company_description):
        self.db.c.execute(
            '''INSERT INTO companies(company_name, company_description) VALUES(?, ?)''',
            (company_name.lower(), company_description)
        )
        self.db.conn.commit()
        #self.companies.companies_show()


## Класс формы добавления новой компании
#class CompanyNew(tk.Toplevel):
#    def __init__(self):
#        super().__init__(root)
#        self.init_company_new()
#        self.main = app  # Передаем класс Main
#        self.db = db  # Передаем класс DB
#
#    def init_company_new(self):
#        self.title('Добавить компанию')
#        self.geometry('415x200+400+300')
#        self.resizable(False, False)
#
#        # Создаем поля формы
#        # self.entery_new_company = tk.Entry(self, width=40, bg="white", fg="black")
#        # self.entery_new_company.place(x=200, y=20, width=180)
#
#        lbl_company_name = tk.Label(self, text='Название компании')
#        lbl_company_name.place(x=50, y=20)
#        self.ent_company_name = ttk.Entry(self)
#        self.ent_company_name.place(x=200, y=20, width=180)
#
#        lbl_company_description = tk.Label(self, text='Описание')
#        lbl_company_description.place(x=50, y=50)
#        self.txt_company_description = tk.Text(self)
#        self.txt_company_description.place(x=200, y=50, width=180, height=100)
#
#        # Полоса прокрутки
#        scroll = tk.Scrollbar(self, command=self.txt_company_description.yview)
#        # scroll.pack(side=tk.RIGHT, fill=tk.Y)
#        scroll.place(x=380, y=50, height=100)
#        self.txt_company_description.configure(yscrollcommand=scroll.set)
#
#        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
#        self.btn_cancel.place(x=305, y=160)
#
#        btn_save = ttk.Button(self, text='Сохранить', command=self.company_save(
#            self.ent_company_name.get(), self.txt_company_description.get('1.0', tk.END)))
#        btn_save.place(x=220, y=160)
#        #btn_save.bind('<Button-1>', lambda event: self.company_save(
#        #    self.ent_company_name.get(), self.txt_company_description.get('1.0', tk.END)
#        #))
#        self.grab_set()
#        self.focus_set()
#
#    def company_clear(self):
#        self.ent_company_name.delete(0, tk.END)
#        self.txt_company_description.delete(1.0, tk.END)
#
#    def company_save(self, company_name, company_description):
#        if (len(company_name) == 0):
#            mb.showwarning("Предупреждение", "Требуется ввести название компании")
#        else:
#            if (self.company_get_by_name(self.ent_company_name.get())):  # Компания уже есть
#                #  mb.showwarning("Предупреждение", 'Компания найдена:  ' +
#                #               self.get_company_by_name(self.ent_company_name.get()))
#                answer = mb.askyesnocancel(title='Найдена компания - ' +
#                                                 self.company_get_by_name(self.ent_company_name.get()),
#                                           message="Обновить?")
#                if (answer):  # Если True
#                    self.company_update_by_name(company_name, company_description)
#                    self.company_clear()
#                elif (answer is None):  # Если None
#                    # Имитация клмка по btn_cancel
#                    self.btn_cancel.invoke()
#            else:  # Компании нет, сохраняем
#                self.company_insert(company_name, company_description)
#                answer = mb.askyesno(title='Данные сохранены', message='Еще новый клиент?')
#                if (answer):  # Если True
#                    self.company_clear()
#                else:  # Если False
#                    # Имитация клмка по btn_cancel
#                    self.btn_cancel.invoke()
#
#    def company_get_by_name(self, company_name):
#        company_name = (company_name.lower(),)
#        self.db.c.execute(
#            '''SELECT company_name FROM companies WHERE LOWER(company_name) = ?''', company_name
#        )
#        row = self.db.c.fetchone()
#        if row is not None:
#            return row[0]
#        else:
#            return None
#
#    def company_insert(self, company_name, company_description):
#        self.db.c.execute(
#            '''INSERT INTO companies(company_name, company_description) VALUES(?, ?)''',
#            (company_name.lower(), company_description)
#        )
#        self.db.conn.commit()
#
#    def company_update_by_name(self, company_name, company_description):
#        self.db.c.execute(
#            '''UPDATE companies SET company_name=?, company_description=? WHERE LOWER(company_name) = ?''',
#            (company_name.lower(), company_description, company_name.lower())
#        )
#        self.db.conn.commit()


# Класс подвлюжчения к БД
class DB:
    def __init__(self):
        self.conn = sqlite3.connect('сompleted_work.db')
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS companies (id_company integer primary key,
             company_name text, company_description text)'''
        )
        self.conn.commit()

    # def insert_company(self, company_name, company_description):
    #    self.c.execute(
    #        '''INSERT INTO companies(company_name, company_description) VALUES(?, ?)''',
    #        (company_name, company_description)
    #    )
    #    self.conn.commit()

    # def get_company_name(self):

    # Именованные параметры
    # sql = "SELECT column FROM table WHERE col1=%s AND col2=%s"
    # params = (col1_value, col2_value)
    # cursor.execute(sql, params)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    root = tk.Tk()
    db = DB()  # Добавляем класс DB возможности добавления в другие классы
    app = Main(root)  # Добавляем класс Main ...
    #companies = Companies()
    #company = Company()
    app.pack()
    root.title("Что сделано")
    root.geometry("650x450+300+200")
    # root.resizable(False, False)
    root.mainloop()
