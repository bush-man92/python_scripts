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
        self.ENTRYPASSWORD = Entry()
        self.ENTRYPASSWORD.grid(row = 1, column = 1, pady = 10, padx = 10, sticky="NSEW")

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
            else:
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
        self.user_menu(name, password)

    def user_menu(self, name, password):
        self.DEL_USER = Button(text="Delete User", command = lambda: self.delete_user(name))
        self.DEL_USER.grid(row = 0, column = 0, pady = 5, padx = 5, sticky="NSEW")
        self.CHANGE_PASSWORD = Button(text="Change Password",
        command = lambda: self.change_password(name, password))
        self.CHANGE_PASSWORD.grid(row = 0, column = 1, pady = 5, padx = 5, sticky="NSEW")
        self.CREATE_LIST = Button(text="Create List")
        self.CREATE_LIST.grid(row = 0, column = 2, pady = 5, padx = 5, sticky="NSEW")
        self.SAVE = Button(text="Save")
        self.SAVE.grid(row = 0, column = 3, pady = 5, padx = 5, sticky="NSEW")
        self.QUIT = Button(text="Exit", command = lambda: self.master.destroy())
        self.QUIT.grid(row = 0, column = 4, pady = 5, padx = 5, sticky="NSEW")

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
