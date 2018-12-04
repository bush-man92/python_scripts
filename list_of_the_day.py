from Tkinter import *
import sqlite3
import tkMessageBox
import datetime

class GUI1:

    def __init__(self, master):
        self.master = master
        master.title("LIST OF THE DAY")
        self.username()
        self.password()
        self.confirm()

    def username(self):
        self.USERNAME = Label(text="Username:", font="Verdana 12 bold")
        self.USERNAME.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.ENTRYNAME = Entry()
        self.ENTRYNAME.grid(row = 0, column = 1, pady = 10, padx = 10, sticky="NSEW")

    def password(self):
        self.PASSWORD = Label(text="Password:", font="Verdana 12 bold")
        self.PASSWORD.grid(row = 1, column = 0, pady = 10, padx = 10)
        self.ENTRYPASSWORD = Entry(show = "*")
        self.ENTRYPASSWORD.grid(row = 1, column = 1, pady = 10, padx = 10, sticky="NSEW")
        self.ENTRYPASSWORD.bind("<Return>", lambda event: self.get_name_password())

    def confirm(self):
        self.CONFIRM = Button(text="Confirm", command = lambda: self.get_name_password())
        self.CONFIRM.grid(row = 2, column = 1, pady = 5, padx = 10)

    def get_name_password(self):
        password = self.ENTRYPASSWORD.get()
        username = self.ENTRYNAME.get()
        user_tuple = (username, password)
        try:
            dtbs.execute("INSERT INTO USERNAME VALUES (?, ?)", user_tuple)
            self.QUESTION = tkMessageBox.askquestion("NEW USER",
            "DO YOU WANT TO CREATE A NEW USER?")
            if self.QUESTION == "yes":
                database.commit()
                self.close_window(username, password)
            elif self.QUESTION == "no":
                database.rollback()
                app = GUI1(root)
        except:
            user_tuple_list = dtbs.execute("SELECT NAME, PASSWORD FROM USERNAME")
            for tuple in user_tuple_list:
                if tuple[0] == username and tuple[1] == password:
                    self.close_window(username, password)
                elif tuple[0] == username and tuple[1] != password:
                    self.INFO = tkMessageBox.showinfo("INFO",
                    "WRONG PASSWORD OR USERNAME ALREADY EXIST.")

    def close_window(self, username, password):
        self.master.destroy()
        self.master = Tk()
        self.app = GUI2(self.master, username, password)
        self.master.mainloop()

class GUI2:

    def __init__(self, master, name, password):
        self.master = master
        self.name = name
        self.password = password
        master.title(name.upper() + "'S LIST")
        today = datetime.datetime.today().strftime('%A %d. %m. %y.')
        yesterday = datetime.datetime.strptime(today, '%A %d. %m. %y.') + datetime.timedelta(days=-1)
        tomorrow = datetime.datetime.strptime(today, '%A %d. %m. %y.') + datetime.timedelta(days=1)
        day_before_yesterday = datetime.datetime.strptime(today, '%A %d. %m. %y.') + datetime.timedelta(days=-2)
        day_after_tomorrow = datetime.datetime.strptime(today, '%A %d. %m. %y.') + datetime.timedelta(days=2)
        time_tuple = (day_before_yesterday, yesterday, today, tomorrow, day_after_tomorrow)
        self.user_menu(name, password, time_tuple)
        self.save_to_database(name, time_tuple)
        self.load_lists(name)

    def user_menu(self, name, password, time_tuple):

        CheckVar1 = IntVar()
        CheckVar2 = IntVar()
        CheckVar3 = IntVar()

        self.DEL_USER = Button(text="Delete User", command = lambda: self.delete_user(name))
        self.DEL_USER.grid(row = 0, column = 0, pady = 5, padx = 5, sticky="NSEW")
        self.CHANGE_PASSWORD = Button(text="Change Password",
        command = lambda: self.change_password(name, password))
        self.CHANGE_PASSWORD.grid(row = 0, column = 1, pady = 5, padx = 5, sticky="NSEW")
        self.SAVE = Button(text="Save", command = lambda: self.save_question(name, time_tuple))
        self.SAVE.grid(row = 0, column = 2, pady = 5, padx = 5, sticky="NSEW")
        self.QUIT = Button(text="Exit", command = lambda: self.master.destroy())
        self.QUIT.grid(row = 0, column = 3, pady = 5, padx = 5, sticky="NSEW")
        self.ENTRYLABEL = Label(text="Star your list here:", font = "Verdana 8")
        self.ENTRYLABEL.grid(row = 1, column = 0, padx = 5, pady = 5, sticky="NSEW")
        self.ENTRYLIST = Entry()
        self.ENTRYLIST.grid(row = 1, column = 1, pady = 5, padx = 5, sticky="NSEW")
        self.ENTRYLIST.bind("<Return>", lambda event: self.enter_to_lists(name, CheckVar1,
        CheckVar2, CheckVar3))
        self.FIRSTNAME = Label(text = time_tuple[0].strftime('%A %d. %m. %y.'),
        font="Verdana 8")
        self.FIRSTNAME.grid(row = 2, column = 0, pady = 5, padx = 5, sticky="NSEW")
        self.SECOND = Label(text = time_tuple[1].strftime('%A %d. %m. %y.'),
        font="Verdana 8")
        self.SECOND.grid(row = 2, column = 1, pady = 5, padx = 5, sticky="NSEW")
        self.THIRD = Checkbutton(text = time_tuple[2], font="Verdana 8", variable = CheckVar1,
        onvalue = 1, offvalue = 0)
        self.THIRD.grid(row = 2, column = 2, pady = 5, padx = 5, sticky="NSEW")
        self.FOURTH = Checkbutton(text = time_tuple[3].strftime('%A %d. %m. %y.'),
        font="Verdana 8", variable = CheckVar2, onvalue = 1, offvalue = 0)
        self.FOURTH.grid(row = 2, column = 3, pady = 5, padx = 5, sticky="NSEW")
        self.FIFTH = Checkbutton(text = time_tuple[4].strftime('%A %d. %m. %y.'),
        font="Verdana 8", variable = CheckVar3, onvalue = 1, offvalue = 0)
        self.FIFTH.grid(row = 2, column = 4, pady = 5, padx = 5, sticky="NSEW")
        self.FIRSTLIST = Listbox()
        self.FIRSTLIST.grid(row = 3, column = 0, pady = 5, padx = 5, sticky="NSEW")
        self.SECONDLIST = Listbox()
        self.SECONDLIST.grid(row = 3, column = 1, pady = 5, padx = 5, sticky="NSEW")
        self.THIRDLIST = Listbox()
        self.THIRDLIST.grid(row = 3, column = 2, pady = 5, padx = 5, sticky="NSEW")
        self.FOURTHLIST = Listbox()
        self.FOURTHLIST.grid(row = 3, column = 3, pady = 5, padx = 5, sticky="NSEW")
        self.FIFTHLIST = Listbox()
        self.FIFTHLIST.grid(row = 3, column = 4, pady = 5, padx = 5, sticky="NSEW")

    def enter_to_lists(self, name, one, two, three):
        entry = self.ENTRYLIST.get()
        self.ENTRYLIST.delete(0, END)
        if one.get() == 1:
            self.THIRDLIST.insert(END, entry)
        if two.get() == 1:
            self.FOURTHLIST.insert(END, entry)
        if three.get() == 1:
            self.FIFTHLIST.insert(END, entry)

    def save_question(self, name, time_tuple):
        self.SAVEQUESTION = tkMessageBox.askquestion("SAVE", "ARE YOU SURE YOU WANT TO SAVE YOUR LISTS?")
        if self.SAVEQUESTION == "yes":
            self.save_to_database(name, time_tuple)
        else:
            pass

    def save_to_database(self, name, time_tuple):
        try:
            dtbs.execute("""CREATE TABLE before_yesterday_table
            (TASK       TEXT PRIMARY KEY        NOT NULL,
            USER        TEXT        NOT NULL,
            TMSTAMP        TEXT        NOT NULL)""")
        except:
            pass
        try:
            dtbs.execute("""CREATE TABLE yesterday_table
            (TASK       TEXT PRIMARY KEY        NOT NULL,
            USER        TEXT        NOT NULL,
            TMSTAMP     TEXT        NOT NULL)""")
        except:
            pass
        try:
            dtbs.execute("""CREATE TABLE today_table
            (TASK   TEXT PRIMARY KEY    NOT NULL,
            USER    TEXT    NOT NULL,
            TMSTAMP     TEXT        NOT NULL);""")
        except:
            third_list = self.THIRDLIST.get(0, END)
            list11 = dtbs.execute("SELECT TASK FROM today_table WHERE USER = ?", (name,))
            search_list1 = []
            for tuple in list11:
                search_list1.append(tuple[0])
            if len(third_list) > len(search_list1):
                for n in range (len(search_list1), len(third_list)):
                    tuple1 = (third_list[n], name, time_tuple[2])
                    dtbs.execute("INSERT INTO today_table VALUES (?, ?, ?)", tuple1)
                database.commit()
        try:
            dtbs.execute("""CREATE TABLE tomorrow_table
            (TASK       TEXT PRIMARY KEY        NOT NULL,
            USER        TEXT        NOT NULL,
            TMSTAMP     TEXT        NOT NULL)""")
        except:
            fourth_list = self.FOURTHLIST.get(0, END)
            list12 = dtbs.execute("SELECT TASK FROM tomorrow_table WHERE USER = ?", (name,))
            search_list2 = []
            for tuple in list12:
                search_list2.append(tuple[0])
            if len(fourth_list) > len(search_list2):
                for n in range (len(search_list2), len(fourth_list)):
                    tuple2 = (fourth_list[n], name, time_tuple[3])
                    dtbs.execute("INSERT INTO tomorrow_table VALUES (?, ?, ?)", tuple2)
                database.commit()
        try:
            dtbs.execute("""CREATE TABLE after_tomorrow_table
            (TASK       TEXT PRIMARY KEY        NOT NULL,
            USER        TEXT        NOT NULL,
            TMSTAMP     TEXT        NOT NULL)""")
        except:
            fifth_list = self.FIFTHLIST.get(0, END)
            list13 = dtbs.execute("SELECT TASK FROM after_tomorrow_table WHERE USER = ?", (name,))
            search_list3 = []
            for tuple in list13:
                search_list3.append(tuple[0])
            if len(fifth_list) > len(search_list3):
                for n in range (len(search_list3), len(fifth_list)):
                    tuple3 = (fifth_list[n], name, time_tuple[4])
                    dtbs.execute("INSERT INTO after_tomorrow_table VALUES (?, ?, ?)", tuple3)
                database.commit()

    def delete_user(self, name):
        self.QUESTION2 = tkMessageBox.askquestion("DELETING USERNAME",
        "ARE YOU SURE YOU WANT TO DELETE USERNAME: " + name)
        if self.QUESTION2 == "yes":
            dtbs.execute("DELETE FROM USERNAME WHERE NAME = (?)", (name,))
            database.commit()
            self.master.destroy()
            self.master = Tk()
            self.app = GUI1(self.master)
            self.master.mainloop()
        else:
            pass

    def change_password(self, name, password):
        self.master.destroy()
        self.master = Tk()
        self.app = GUI3(self.master, name, password)
        self.master.mainloop()

    def load_lists(self, name):
        list1 = dtbs.execute("SELECT TASK, USER FROM before_yesterday_table")
        for tuple in list1:
            if tuple[1] == name:
                self.FIRSTLIST.insert(END, tuple[0])
        list2 = dtbs.execute("SELECT TASK, USER FROM yesterday_table")
        for tuple in list2:
            if tuple[1] == name:
                self.SECONDLIST.insert(END, tuple[0])
        list3 = dtbs.execute("SELECT TASK, USER, TMSTAMP FROM today_table")
        for tuple in list3:
            if tuple[1] == name:
                self.THIRDLIST.insert(END, tuple[0])
        list4 = dtbs.execute("SELECT TASK, USER, TMSTAMP FROM tomorrow_table")
        for tuple in list4:
            if tuple[1] == name:
                self.FOURTHLIST.insert(END, tuple[0])
        list5 = dtbs.execute("SELECT TASK, USER, TMSTAMP FROM after_tomorrow_table")
        for tuple in list5:
            if tuple[1] == name:
                self.FIFTHLIST.insert(END, tuple[0])

class GUI3:

    def __init__(self, master, name, password):
        self.master = master
        self.name = name
        self.password = password
        master.title("CHANGE PASSWORD")
        self.change(name, password)

    def change(self, name, password):
        self.change_password = Label(text="Your password is " + password, font="Verdana 8")
        self.change_password.grid(row = 0, column = 0, pady = 10, padx = 10, sticky="NSEW")
        self.change_password2 = Label(text="Enter your new password below:", font="Verdana 8")
        self.change_password2.grid(row = 1, column = 0, pady = 10, padx = 10, sticky="NSEW")
        self.change_password3 = Entry()
        self.change_password3.grid(row = 2, column = 0, pady = 10, padx = 10, sticky="NSEW")
        self.change_password4 = Button(text="Confirm",
        command = lambda: self.confirm_change(name, password))
        self.change_password4.grid(row = 3, column = 0, pady = 10, padx = 10, sticky="NSEW")
        self.change_password5 = Button(text="Cancel", command = lambda: self.cancel(name, password))
        self.change_password5.grid(row = 3, column = 1, pady = 10, padx = 10, sticky="NSEW")

    def confirm_change(self, name, password):
        new_password = self.change_password3.get()
        user_tuple2 = (new_password, name)
        dtbs.execute("UPDATE USERNAME SET PASSWORD = ? WHERE NAME = ?", user_tuple2)
        self.QUESTION3 = tkMessageBox.askquestion("CHANGE PASSWORD",
        "ARE YOU SURE YOU WANT TO CHANGE YOUR PASSWORD TO " + new_password + "?")
        if self.QUESTION3 == "yes":
            database.commit()
            self.master.destroy()
            self.master = Tk()
            self.app = GUI2(self.master, name, new_password)
            self.master.mainloop()
        else:
            app = GUI3(self.master, name, password)

    def cancel(self, name, password):
        self.master.destroy()
        self.master = Tk()
        self.app = GUI2(self.master, name, password)
        self.master.mainloop()

try:
    database = sqlite3.connect('database.db')
    dtbs = database.cursor()
    dtbs.execute("""CREATE TABLE USERNAME
    (NAME    TEXT PRIMARY KEY    NOT NULL,
    PASSWORD     TEXT    NOT NULL);""")
except:
    pass

root = Tk()
app = GUI1(root)
root.mainloop()
