import mysql.connector
from tkinter import *
from tkinter import messagebox

pass_input = None
connection = None

def get_password():
    global pass_input
    pass_input = password_entry.get()
    try:
        my_db = mysql.connector.connect(host='localhost', user='root',
                                        password=pass_input)
        password_screen.destroy()
    except:
        messagebox.showerror('ERROR', 'Password entered is wrong')

def exit_button():
    choice = messagebox.askyesno("EXIT", "Do you want to exit???")
    if choice:
        password_screen.destroy()
        exit()

password_screen = Tk()
password_screen.title('SQL PASSWORD')
password_screen.geometry('450x325+458+211')
password_screen.resizable(False, False)
password_screen.after(1, lambda: password_screen.focus_force())

image_file = PhotoImage(file='Images\\login_bg.png')
image = Label(password_screen, image=image_file)
image.place(x=0, y=0)

password_message = Label(password_screen, text='ENTER SQL PASSWORD: ',
                         bg='white', font=('Times New Roman', 13))
password_message.place(x=20, y=128)
password_entry = Entry(password_screen, show='*', font=('Times New Roman', 14))
password_entry.place(x=222, y=128)
password_entry.focus_set()

password_button = Button(password_screen, text='SUBMIT', command=get_password,
                         padx=62, font=('Times New Roman', 13))
password_button.place(x=20, y=160)

password_cancel_button = Button(password_screen, text='CANCEL', command=exit_button,
                                padx=55, font=('Times New Roman', 13))
password_cancel_button.place(x=222, y=160)

password_screen.protocol('WM_DELETE_WINDOW', exit_button)
password_screen.mainloop()

try:
    connection = mysql.connector.connect(host='localhost', user='root',
                                         password=pass_input)

except:
    exit()

my_cursor = connection.cursor()

my_cursor.execute('create database if not exists school_project')
my_cursor.execute('use school_project')

my_cursor.execute('create table if not exists passwords(user_id varchar(20)'
                  ' Primary key, password varchar(20))')
my_cursor.execute('create table if not exists snake_scores(user_id varchar(20),'
                  ' score int)')
my_cursor.execute('create table if not exists space_invasion_scores'
                  '(user_id varchar(20), score int, level int)')
my_cursor.execute('create table if not exists flappy_bird_scores'
                  '(user_id varchar(20), score int)')

my_cursor.execute('alter table snake_scores add foreign key(user_id) references '
                  'passwords(user_id) on delete cascade')
my_cursor.execute('alter table space_invasion_scores add foreign key(user_id)'
                  ' references passwords(user_id) on delete cascade')
my_cursor.execute('alter table flappy_bird_scores add foreign key(user_id) '
                  'references passwords(user_id) on delete cascade')

