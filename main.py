import os
import tkinter as tk
from tkinter import ttk
import sqlite3

script_directory = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_directory, 'static', 'media')


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file=os.path.join(image_path, 'add.gif'))
        btn_open_dialog = tk.Button(
            toolbar,
            text='Добавить позицию',
            command=self.open_dialog,
            bg='#d7d8e0',
            bd=0,
            compound=tk.TOP,
            image=self.add_img,
        )
        btn_open_dialog.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(
            file=os.path.join(image_path, 'update.gif')
        )
        btn_edit_dialog = tk.Button(
            toolbar,
            text='Редактировать',
            bg='#d7d8e0',
            bd=0,
            image=self.update_img,
            compound=tk.TOP,
            command=self.open_update_dialog,
        )
        btn_edit_dialog.pack(side=tk.LEFT)

        self.search_img = tk.PhotoImage(
            file=os.path.join(image_path, 'search.gif')
        )
        btn_search = tk.Button(
            toolbar,
            text='Поиск',
            bg='#d7d8e0',
            bd=0,
            image=self.search_img,
            compound=tk.TOP,
            command=self.open_search_dialog,
        )
        btn_search.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(
            file=os.path.join(image_path, 'delete.gif')
        )
        btn_delete = tk.Button(
            toolbar,
            text='Удалить позицию',
            bg='#d7d8e0',
            bd=0,
            image=self.delete_img,
            compound=tk.TOP,
            command=self.delete_records,
        )
        btn_delete.pack(side=tk.LEFT)

        self.refresh_img = tk.PhotoImage(
            file=os.path.join(image_path, 'refresh.gif')
        )
        btn_refresh = tk.Button(
            toolbar,
            text='Обновить',
            bg='#d7d8e0',
            bd=0,
            image=self.refresh_img,
            compound=tk.TOP,
            command=self.view_records,
        )
        btn_refresh.pack(side=tk.LEFT)

        self.exit_img = tk.PhotoImage(
            file=os.path.join(image_path, 'exit.gif')
        )
        btn_exit = tk.Button(
            toolbar,
            text='Выход',
            bg='#d7d8e0',
            bd=0,
            image=self.exit_img,
            compound=tk.TOP,
            command=self.quit,
        )
        btn_exit.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(
            self,
            columns=('ID', 'description', 'costs', 'total'),
            height=15,
            show='headings',
        )

        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('description', width=365, anchor=tk.CENTER)
        self.tree.column('costs', width=150, anchor=tk.CENTER)
        self.tree.column('total', width=100, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('description', text='Наименование')
        self.tree.heading('costs', text='Статья дохода/расхода')
        self.tree.heading('total', text='Сумма')

        self.tree.pack(side=tk.LEFT)

        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    def records(self, description, costs, total):
        self.db.insert_data(description, costs, total)
        self.view_records()

    def update_record(self, description, costs, total):
        self.db.c.execute(
            '''UPDATE finance SET description=?, costs=?, total=? WHERE ID=?''',
            (
                description,
                costs,
                total,
                self.tree.set(self.tree.selection()[0], '#1'),
            ),
        )
        self.db.conn.commit()
        self.view_records()

    def view_records(self):
        self.db.c.execute('''SELECT * FROM finance''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [
            self.tree.insert('', 'end', values=row)
            for row in self.db.c.fetchall()
        ]

    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute(
                '''DELETE FROM finance WHERE id=?''',
                (self.tree.set(selection_item, '#1'),),
            )
        self.db.conn.commit()
        self.view_records()

    def search_records(self, description):
        description = ('%' + description + '%',)
        self.db.c.execute(
            '''SELECT * FROM finance WHERE description LIKE ?''', description
        )
        [self.tree.delete(i) for i in self.tree.get_children()]
        [
            self.tree.insert('', 'end', values=row)
            for row in self.db.c.fetchall()
        ]

    def open_dialog(self):
        Child()

    def open_update_dialog(self):
        Update()

    def open_search_dialog(self):
        Search()


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавить доходы/расходы')
        self.geometry('400x220+400+300')
        self.wm_attributes('-alpha', 0.9)
        root.iconbitmap(os.path.join(image_path, 'add.ico'))
        self.resizable(False, False)

        label_description = tk.Label(self, text='Наименование:')
        label_description.place(x=50, y=50)
        label_select = tk.Label(self, text='Статья дохода/расхода:')
        label_select.place(x=50, y=80)
        label_sum = tk.Label(self, text='Сумма:')
        label_sum.place(x=50, y=110)

        self.entry_description = ttk.Entry(self)
        self.entry_description.place(x=200, y=50)

        self.entry_money = ttk.Entry(self)
        self.entry_money.place(x=200, y=110)

        self.combobox = ttk.Combobox(self, values=[u'Доход', u'Расход'])
        self.combobox.current(0)
        self.combobox.place(x=200, y=80)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=170)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=170)
        self.btn_ok.bind(
            '<Button-1>',
            lambda event: self.view.records(
                self.entry_description.get(),
                self.combobox.get(),
                self.entry_money.get(),
            ),
        )

        self.grab_set()
        self.focus_set()


class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title('Редактировать позицию')
        root.iconbitmap(os.path.join(image_path, 'update.ico'))
        self.wm_attributes('-alpha', 0.9)
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=170)
        btn_edit.bind(
            '<Button-1>',
            lambda event: self.view.update_record(
                self.entry_description.get(),
                self.combobox.get(),
                self.entry_money.get(),
            ),
        )

        self.btn_ok.destroy()

    def default_data(self):
        self.db.c.execute(
            '''SELECT * FROM finance WHERE id=?''',
            (self.view.tree.set(self.view.tree.selection()[0], '#1'),),
        )
        row = self.db.c.fetchone()
        self.entry_description.insert(0, row[1])
        if row[2] != 'Доход':
            self.combobox.current(1)
        self.entry_money.insert(0, row[3])


class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск')
        self.geometry('330x100+450+350')
        root.iconbitmap(os.path.join(image_path, 'search.ico'))
        self.wm_attributes('-alpha', 0.9)

        self.resizable(False, False)

        label_search = tk.Label(self, text='Поиск   ')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=180)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=105, y=50)
        btn_search.bind(
            '<Button-1>',
            lambda event: self.view.search_records(self.entry_search.get()),
        )
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('finance.db')
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS finance (id integer primary key, description text, costs text, total real)'''
        )
        self.conn.commit()

    def insert_data(self, description, costs, total):
        self.c.execute(
            '''INSERT INTO finance(description, costs, total) VALUES (?, ?, ?)''',
            (description, costs, total),
        )
        self.conn.commit()


if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Home finance")
    root.geometry("680x400+300+200")
    root.resizable(False, False)
    root.iconbitmap(os.path.join(image_path, 'icon.ico'))
    root.mainloop()
