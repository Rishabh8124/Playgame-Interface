from tkinter import *
from tkinter import messagebox
import mysql.connector
import pyttsx3

status = False
r_status = False
register_state = True
register_state_1 = True
user_id = ''
warn = 0
time_count = 500

def login_using_user(password):
    global user_id, status, register_state_1

    register_state_1 = True
    status = False

    # Creating and executing the login interface
    def login_interface():
        global register_state_1
        register_state_1 = False

        # Deleting the login or register screen
        try:
            screen.destroy()
        except:
            pass

        # Function for checking the password
        def get_password():
            global status, user_id, warn

            # Getting the user id and password
            user_id = user_entry.get().lower()
            password = password_entry.get()
            warning_count = warn

            # Checking the user id and password
            if user_id not in records:

                if warning_count in (0, 1):

                    warning_count += 1
                    warn = warning_count
                    available = 3 - warning_count
                    user_entry.delete(0, END)
                    password_entry.delete(0, END)
                    messagebox.showwarning('WARNING', 'USER not found')
                    voice_engine.say(str(available) + 'attempts left')
                    voice_engine.runAndWait()

                    user_entry.focus_set()

                elif warning_count == 2:

                    # Displaying and ending the login screen
                    warning_count = 3
                    warn = warning_count
                    messagebox.showerror('ERROR', '3 WRONG ATTEMPTS')
                    root.destroy()
                    voice_engine.say('LOGIN FAILED')
                    voice_engine.runAndWait()
                    status = False

            elif records[user_id] != password:

                if warning_count in (0, 1):
                    # Clearing the entry field
                    user_entry.delete(0, END)
                    password_entry.delete(0, END)

                    # Displaying the error
                    warning_count += 1
                    warn = warning_count
                    available = 3 - warning_count
                    messagebox.showwarning('WARNING', 'PASSWORD does not match')
                    voice_engine.say(str(available)+'attempts left')
                    voice_engine.runAndWait()

                    user_entry.focus_set()

                elif warning_count == 2:

                    # Displaying and ending the login screen
                    warning_count = 3
                    warn = warning_count
                    messagebox.showerror('ERROR', '3 WRONG ATTEMPTS')
                    root.destroy()
                    voice_engine.say('LOGIN FAILED')
                    voice_engine.runAndWait()
                    status = False

            else:
                user_entry.delete(0, END)
                password_entry.delete(0, END)

                # Displaying the message and ending the screen
                messagebox.showinfo('SUCCESS', 'SUCCESSFULLY LOGGED IN')
                root.destroy()

                status = True

        def cancel():
            root.destroy()

        # Initializing the screen
        root = Tk()
        root.title('LOGIN')
        root.iconbitmap('Video transitions/Logo.ico')
        root.geometry('479x83+443+322')
        root.resizable(False, False)
        root.after(1, lambda: root.focus_force())

        # Getting the records
        database = mysql.connector.connect(host='localhost', user='root',
                                           password=password, database='school_project')
        cursor = database.cursor()
        cursor.execute('select * from passwords;')
        result = cursor.fetchall()
        records = {}
        for i in result:
            records.update({i[0]: i[1]})

        # Image
        image_file = PhotoImage(file='Images\\user.png')
        image = Label(root, image=image_file)
        image.grid(row=0, column=0, rowspan=3)

        # Labels and buttons
        u_label = Label(root, text='User', padx=50, font=('Times', 13))
        u_label.grid(row=0, column=1)

        user_entry = Entry(root, width=30, font=('Times', 13))
        user_entry.grid(row=0, column=2)
        user_entry.focus_set()

        p_label = Label(root, text='Password', padx=10, font=('Times', 13))
        p_label.grid(row=1, column=1)

        password_entry = Entry(root, show='*', width=30, font=('Times', 13))
        password_entry.grid(row=1, column=2)

        login = Button(root, text='LOGIN', command=get_password, padx=10, font=('Times', 13))
        login.grid(row=2, column=1, sticky=W+E)

        cancel = Button(root, text='CANCEL', command=cancel, font=('Times', 13))
        cancel.grid(row=2, column=2, sticky=W+E)

        # Initiating the loop
        root.mainloop()

        if not status and warn < 3:
            login_using_user(password)

    # Creating and executing the register interface
    def register_interface():
        global register_state_1
        register_state_1 = False

        # Destroying the existing login or register screen
        screen.destroy()

        # Defining a function to register a record and add it to the database
        def insert_records():
            global user_id, status, r_status

            # Getting the user id and password
            user_id = user_entry.get().lower()
            password = password_entry.get()

            # Checking the existing records
            if password == '' or user_id == '':
                user_entry.delete(0, END)
                password_entry.delete(0, END)
                messagebox.showwarning('WARNING', 'USER or PASSWORD cannot be empty')
                user_entry.focus_set()

            elif user_id not in records:
                records[user_id] = password
                r_status = True

                # Adding the user to the database
                cursor.execute('Insert into passwords values(\'%s\',\'%s\')' % (user_id, password))
                database.commit()

                # Showing the success message and proceeding to log in to interface
                messagebox.showinfo("SUCCESS", "SUCCESSFULLY REGISTERED")
                root.destroy()
                voice_engine.say('Please re-enter your detail to login')
                voice_engine.runAndWait()

                login_interface()

            # Displaying error and getting a valid user and password
            else:
                user_entry.delete(0, END)
                password_entry.delete(0, END)
                messagebox.showwarning('WARNING', 'USER already exists')
                voice_engine.say('Try a different user name')
                voice_engine.runAndWait()
                user_entry.focus_set()

        def cancel():
            root.destroy()

        # Register interface
        root = Tk()
        root.title('REGISTER')
        root.iconbitmap('Video transitions/Logo.ico')
        root.geometry('479x83+443+322')
        root.resizable(False, False)
        root.after(1, lambda: root.focus_force())

        # Getting the records
        database = mysql.connector.connect(host='localhost', user='root',
                                           password=password, database='school_project')
        cursor = database.cursor()
        cursor.execute('select * from passwords;')
        result = cursor.fetchall()
        records = {}
        for i in result:
            records.update({i[0]: i[1]})

        # Image
        image_file = PhotoImage(file='Images\\user.png')
        image = Label(root, image=image_file)
        image.grid(row=0, column=0, rowspan=3)

        # Labels and buttons
        u_label = Label(root, text='User', padx=50, font=('Times', 13))
        u_label.grid(row=0, column=1)

        user_entry = Entry(root, width=30, font=('Times', 13))
        user_entry.grid(row=0, column=2)
        user_entry.focus_set()

        p_label = Label(root, text='Password', padx=10, font=('Times', 13))
        p_label.grid(row=1, column=1)

        password_entry = Entry(root, show='*', width=30, font=('Times', 13))
        password_entry.grid(row=1, column=2)

        login = Button(root, text='REGISTER', command=insert_records, padx=10, font=('Times', 13))
        login.grid(row=2, column=1, sticky=W + E)

        cancel = Button(root, text='CANCEL', command=cancel, font=('Times', 13))
        cancel.grid(row=2, column=2, sticky=W + E)

        root.mainloop()

        if not r_status:
            login_using_user(password)

    def exit_button():
        choice = messagebox.askyesno("EXIT", "Do you want to exit???")
        if choice:
            screen.destroy()

    def register_pop_up():

        try:
            global register_state, time_count

            if register_state:
                register_message.config(fg='white')
                register_state = False
                time_count = 600

            else:
                register_message.config(fg='dark blue')
                register_state = True
                time_count = 600

            register_pop_up_1()

        except:
            pass

    def register_pop_up_1():
        try:
            if register_state_1:
                screen.after(time_count, register_pop_up)

        except:
            pass
    # Database
    new_database = mysql.connector.connect(host='localhost', user='root', password=password)
    new_cursor = new_database.cursor()
    new_cursor.execute('create database if not exists school_project')
    new_cursor.execute('use school_project')
    new_cursor.execute('create table if not exists passwords(user_id varchar(20)'
                       ', password varchar(20))')

    # Voice
    voice_engine = pyttsx3.init()
    rate = voice_engine.getProperty('rate')
    voices = voice_engine.getProperty('voices')
    voice_engine.setProperty('voice', voices[1].id)
    voice_engine.setProperty('rate', 175)

    # Login or Register screen
    screen = Tk()
    screen.title('REGISTER AND LOGIN')
    screen.geometry('788x606+289+50')
    screen.iconbitmap('Video transitions/Logo.ico')
    screen.resizable(False, False)
    screen.after(1, lambda: screen.focus_force())

    image_file = PhotoImage(file='Images/Login_page_pic.png')
    image = Label(screen, image=image_file)
    image.place(x=0, y=0)

    login_button = Button(screen, text='LOGIN', padx=97, pady=4, command=login_interface,
                          state=NORMAL, font=('Times', 32))
    login_button.place(x=216, y=181)

    register_message = Label(screen, text='REGISTER IF YOU ARE A NEW USER',
                             font=('Times', 12), fg='dark blue', bg='white')
    register_message.place(x=216, y=280)

    register_button = Button(screen, text='REGISTER', padx=61, pady=4, command=register_interface,
                             state=NORMAL, font=('Times', 32))
    register_button.place(x=216, y=312)

    exit_button_display = Button(screen, text='EXIT', padx=30, pady=6, command=exit_button)
    exit_button_display.place(x=486, y=276)

    screen.after(time_count, register_pop_up)

    screen.protocol('WM_DELETE_WINDOW', exit_button)

    screen.mainloop()

    return user_id, status
