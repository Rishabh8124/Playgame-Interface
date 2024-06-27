from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk, Image
from Games import Space_invasion
from Games import Snake_game
from Games import Flappy_bird
import mysql.connector
import pygame
from pygame import mixer
import pyttsx3

# Snake text
snake_text = '''SNAKE GAME
The ||BROWN SQUARE|| in the screen is the snake.
It can move around in all directions. Use ||ARROW KEYS|| to move around.
The main aim is to hit the ||RED SQUARE|| which pops at random positions.
On hitting the red square you get one point and the length of the snake increases by 1
YOU GET OUT WHEN YOU TOUCH THE BOUNDARIES (OR)
WHEN THE HEAD TOUCHES THE BODY OF THE SNAKE.
The score is calculated by the number of red squares you hit.

KEY INSTRUCTIONS:
Arrow - Move the snake
Esc - Pause'''

# Space invasion text
space_text = '''SPACE INVASION GAME
The main ||SPACE SHIP|| is under your control.You can move it along the line using ||LEFT AND RIGHT ARROW KEYS||
There are aliens coming from the top. The aim is to shoot them. For shooting press the ||SPACE BAR||.
Each level has some number of aliens. You win that level if you shoot all the aliens.
YOU GET OUT IF 3 ALIENS REACH THE HEIGHT OF THE SHIP.

KEY INSTRUCTIONS:
Left and Right Arrow - Move the ship left and right
Space - Shoot
Esc - Pause'''

# Flappy bird text
bird_text = '''FLAPPY BIRD
The ||BIRD|| is under your control. It will fly if you press the ||UP ARROW|| key.
There are walls through the way. Move the bird in order to dodge the walls.
THE GAME ENDS IF THE BIRD HITS THE WALLS OR THE FLOOR.

KEY INSTRUCTIONS:
UP Arrow - Move the bird up
Esc - Pause'''

pygame.init()
mixer.music.load('Audio/bgm.mp3')

# Audio
voice_engine_main = pyttsx3.init()
rate = voice_engine_main.getProperty('rate')
voices = voice_engine_main.getProperty('voices')
voice_engine_main.setProperty('voice', voices[0].id)
voice_engine_main.setProperty('rate', 125)

def game(user_id, password):
    mixer.music.play(-1)

    def game_button_1():
        game_interface.destroy()
        mixer.music.stop()

        # Instructions Window
        def start():
            instruction_window.destroy()
            Snake_game.snake_game(user_id, password)

            voice_engine_main.say('GAME OVER')
            voice_engine_main.runAndWait()

        def cancel():
            instruction_window.destroy()

        instruction_window = Tk()
        instruction_window.title('SNAKE GAME INSTRUCTIONS')
        instruction_window.geometry('936x431+215+148')
        instruction_window.after(1, lambda: instruction_window.focus_force())
        instruction_window.resizable(False, False)

        instruction = Label(instruction_window, text=snake_text,
                            font=('TIMES NEW ROMAN', 20), bg='light green')
        instruction.grid(row=0, column=0, columnspan=2)

        start_button = Button(instruction_window, text='START', command=start,
                              pady=8, font=('TIMES NEW ROMAN', 15))
        start_button.grid(row=1, column=0, sticky=W+E)

        cancel_button = Button(instruction_window, text='CANCEL', command=cancel,
                               pady=8, font=('TIMES NEW ROMAN', 15))
        cancel_button.grid(row=1, column=1, sticky=W+E)

        instruction_window.mainloop()

        mixer.music.load('Audio/bgm.mp3')
        mixer.music.play(-1)
        game(user_id, password)

    def game_button_2():
        game_interface.destroy()
        mixer.music.stop()

        # Instructions Window
        def start():
            instruction_window.destroy()
            Space_invasion.space_invasion(1, user_id, password)

            voice_engine_main.say('GAME OVER')
            voice_engine_main.runAndWait()

        def cancel():
            instruction_window.destroy()

        instruction_window = Tk()
        instruction_window.title('SPACE INVASION INSTRUCTION')
        instruction_window.geometry('1351x369+4+180')
        instruction_window.after(1, lambda: instruction_window.focus_force())
        instruction_window.resizable(False, False)

        instruction = Label(instruction_window, text=space_text,
                            font=('TIMES NEW ROMAN', 20), bg='light pink')
        instruction.grid(row=0, column=0, columnspan=2)

        start_button = Button(instruction_window, text='START', command=start,
                              pady=8, font=('TIMES NEW ROMAN', 15))
        start_button.grid(row=1, column=0, sticky=W + E)

        cancel_button = Button(instruction_window, text='CANCEL', command=cancel,
                               pady=8, font=('TIMES NEW ROMAN', 15))
        cancel_button.grid(row=1, column=1, sticky=W + E)

        instruction_window.mainloop()
        mixer.music.load('Audio/bgm.mp3')
        mixer.music.play(-1)

        game(user_id, password)

    def game_button_3():
        game_interface.destroy()
        mixer.music.stop()

        # Instructions Window
        def start():
            instruction_window.destroy()
            Flappy_bird.flappy_bird_game(password, user_id)

            voice_engine_main.say('GAME OVER')
            voice_engine_main.runAndWait()

        def cancel():
            instruction_window.destroy()

        instruction_window = Tk()
        instruction_window.title('FLAPPY BIRD INSTRUCTION')
        instruction_window.geometry('882x307+242+210')
        instruction_window.after(1, lambda: instruction_window.focus_force())
        instruction_window.resizable(False, False)

        instruction = Label(instruction_window, text=bird_text,
                            font=('TIMES NEW ROMAN', 20), bg='light blue')
        instruction.grid(row=0, column=0, columnspan=2)

        start_button = Button(instruction_window, text='START', command=start,
                              pady=8, font=('TIMES NEW ROMAN', 15))
        start_button.grid(row=1, column=0, sticky=W + E)

        cancel_button = Button(instruction_window, text='CANCEL', command=cancel,
                               pady=8, font=('TIMES NEW ROMAN', 15))
        cancel_button.grid(row=1, column=1, sticky=W + E)

        instruction_window.mainloop()
        mixer.music.load('Audio/bgm.mp3')
        mixer.music.play(-1)

        game(user_id, password)

    def exit_button():
        choice = messagebox.askyesno("EXIT", "Do you want to LOGOUT???")
        if choice:
            game_interface.destroy()
            mixer.music.stop()

    def my_scores():
        game_interface.destroy()

        def destroy():
            for children in high_score.get_children():
                high_score.delete(children)

        def alter_tree(event):
            destroy()
            combo_position = table_list.get()

            if combo_position == 'ALL':
                new_tables = tables
            else:
                new_tables = [combo_position]

            new_values = []

            for i in new_tables:
                cursor.execute('select * from {}'.format(i))
                element = cursor.fetchall()
                if cursor.rowcount != 0:
                    if len(element[0]) == 2:
                        cursor.execute(
                            'select score from {} where user_id = "{}" order by '
                            'score desc'.format(i, user_id))
                        final_result = cursor.fetchall()
                        for j1 in range(len(final_result)):
                            final_result[j1] = [i.upper(), final_result[j1][0], 'NA']

                        new_values.extend(final_result)

                    else:
                        cursor.execute('select * from {} where user_id = "{}" order'
                                       ' by level desc, score desc'.format(i, user_id))
                        final_result = cursor.fetchall()

                        for j1 in range(len(final_result)):
                            final_result[j1] = [i.upper(), final_result[j1][0],
                                                final_result[j1][1]]

                        new_values.extend(final_result)

            if len(new_values) > 0:
                for k1 in new_values:
                    high_score.insert(parent='', index=END, iid=
                    len(high_score.get_children()), text='', value=k1)

            else:
                high_score.insert(parent='', index=END, iid=len(high_score.get_children()), text='',
                                  value=['NO', 'RECORDS', 'FOUND'])

        def back_function():
            scores_screen.destroy()

        my_database = mysql.connector.connect(host='localhost', user='root',
                                              password=password,
                                              database='school_project')
        cursor = my_database.cursor()
        cursor.execute('show tables')
        result = cursor.fetchall()
        result.remove(('passwords',))
        tables = [i[0].title() for i in result]

        scores_screen = Tk()
        scores_screen.title('MY SCORES')
        scores_screen.resizable(False, False)
        scores_screen.geometry('400x185+483+281')
        scores_screen.after(1, lambda: scores_screen.focus_force())

        table_list = ttk.Combobox(scores_screen, value=['ALL'] + tables)
        table_list.current(0)
        table_list.grid(row=0, column=0, sticky=W + E, pady=4)
        table_list.bind('<<ComboboxSelected>>', alter_tree)

        score_frame = Frame(scores_screen)
        score_frame.grid(row=1, column=0, sticky=W+E, pady=4)

        back = Button(scores_screen, text='BACK', command=back_function,
                      font=('Times', 13))
        back.grid(row=2, column=0, sticky=N + S + W + E, pady=4)

        scroll = Scrollbar(score_frame, orient=VERTICAL)
        scroll.pack(side=RIGHT, fill='y')

        high_score = ttk.Treeview(score_frame, height=4, yscrollcommand=scroll.set)
        high_score.pack()

        scroll.config(command=high_score.yview)

        high_score['columns'] = ("Game", "Highest score", "Level")

        high_score.column("#0", width=0, stretch=NO)
        high_score.column("Game", anchor=CENTER, width=180)
        high_score.column("Highest score", anchor=CENTER, width=100)
        high_score.column("Level", anchor=CENTER, width=100)

        high_score.heading('Game', text='GAME', anchor=CENTER)
        high_score.heading('Highest score', text='Highest score', anchor=CENTER)
        high_score.heading('Level', text='Level', anchor=CENTER)

        values = []

        for i in tables:
            cursor.execute('select * from {}'.format(i))
            first_element = cursor.fetchall()
            if cursor.rowcount != 0:
                if len(first_element[0]) == 2:
                    cursor.execute('select score from {} where user_id = "{}" '
                                   'order by score desc'.format(i, user_id))
                    result = cursor.fetchall()
                    for j in range(len(result)):
                        result[j] = [i.upper(), result[j][0], 'NA']

                    values.extend(result)

                else:
                    cursor.execute('select score, level from {} where user_id = "{}"'
                                   ' order by level desc, score desc'.format(i, user_id))
                    result = cursor.fetchall()
                    for j in range(len(result)):
                        result[j] = [i.upper(), result[j][0], result[j][1]]

                    values.extend(result)

        if len(values) > 0:
            for k in values:
                high_score.insert(parent='', index=END, iid=
                len(high_score.get_children()), text='', value=k)

        else:
            high_score.insert(parent='', index=END, iid=
            len(high_score.get_children()), text='', value=['NO', 'RECORDS', 'FOUND'])

        scores_screen.mainloop()

        game(user_id, password)

    def high_scores():
        game_interface.destroy()

        def destroy():
            for children in high_score.get_children():
                high_score.delete(children)

        def alter_tree(event):
            destroy()
            combo_position = table_list.get()

            if combo_position != 'ALL':
                new_tables = [combo_position]
            else:
                new_tables = tables

            new_values = []

            for i in new_tables:
                cursor.execute('select * from {}'.format(i))
                element = cursor.fetchall()
                if cursor.rowcount != 0:
                    if len(element[0]) == 2:
                        cursor.execute('select * from {} order by score desc'.format(i))
                        final_result = cursor.fetchall()
                        for j1 in range(len(final_result)):
                            final_result[j1] = [i.upper(), final_result[j1][0],
                                                final_result[j1][1], 'NA']

                        new_values.extend(final_result)

                    else:
                        cursor.execute('select * from {} order by level desc, '
                                       'score desc'.format(i))
                        final_result = cursor.fetchall()
                        for j1 in range(len(final_result)):
                            final_result[j1] = [i.upper()] + list(final_result[j1])

                        new_values.extend(final_result)

            if len(new_values) > 0:
                for k1 in new_values:
                    high_score.insert(parent='', index=END, iid=
                    len(high_score.get_children()), text='', value=k1)

            else:
                high_score.insert(parent='', index=END, iid=
                len(high_score.get_children()), text='',
                                  value=['NO', 'RECORDS', 'FOUND', '!!!'])

        def back_function():
            scores_screen.destroy()

        my_database = mysql.connector.connect(host='localhost', user='root',
                                              password=password,
                                              database='school_project')
        cursor = my_database.cursor()
        cursor.execute('show tables')
        result = cursor.fetchall()
        result.remove(('passwords',))
        tables = [i[0].title() for i in result]

        scores_screen = Tk()
        scores_screen.title('HIGH SCORES')
        scores_screen.resizable(False, False)
        scores_screen.geometry('580x185+393+281')
        scores_screen.after(1, lambda: scores_screen.focus_force())

        table_list = ttk.Combobox(scores_screen, value=['ALL'] + tables)
        table_list.current(0)
        table_list.grid(row=0, column=0, sticky=W + E, pady=4)
        table_list.bind('<<ComboboxSelected>>', alter_tree)

        score_frame = Frame(scores_screen)
        score_frame.grid(row=1, column=0, sticky=W + E, pady=4)

        back = Button(scores_screen, text='BACK', command=back_function,
                      font=('Times', 13))
        back.grid(row=2, column=0, sticky=N + S + W + E, pady=4)

        scroll = Scrollbar(score_frame, orient=VERTICAL)
        scroll.pack(side=RIGHT, fill='y')

        high_score = ttk.Treeview(score_frame, height=4, yscrollcommand=scroll.set)
        high_score.pack()

        scroll.config(command=high_score.yview)

        high_score['columns'] = ("Game", "User_ID", "Highest score", "Level")

        high_score.column("#0", width=0, stretch=NO)
        high_score.column("Game", anchor=CENTER, width=180)
        high_score.column("User_ID", anchor=CENTER, width=180)
        high_score.column("Highest score", anchor=CENTER, width=100)
        high_score.column("Level", anchor=CENTER, width=100)

        high_score.heading('Game', text='GAME', anchor=CENTER)
        high_score.heading("User_ID", text="User_ID", anchor=CENTER)
        high_score.heading('Highest score', text='Highest score', anchor=CENTER)
        high_score.heading('Level', text='Level', anchor=CENTER)

        values = []

        for i in tables:
            cursor.execute('select * from {}'.format(i))
            first_element = cursor.fetchall()
            if cursor.rowcount != 0:
                if len(first_element[0]) == 2:
                    cursor.execute('select * from {} order by score desc'.format(i))
                    result = cursor.fetchall()
                    for j in range(len(result)):
                        result[j] = [i.upper(), result[j][0], result[j][1], 'NA']

                    values.extend(result)

                else:
                    cursor.execute('select * from {} order by level desc, '
                                   'score desc'.format(i))
                    result = cursor.fetchall()
                    for j in range(len(result)):
                        result[j] = [i.upper()] + list(result[j])

                    values.extend(result)

        if len(values) > 0:
            for k in values:
                high_score.insert(parent='', index=END, iid=
                len(high_score.get_children()), text='', value=k)

        else:
            high_score.insert(parent='', index=END, iid=len(high_score.get_children()),
                              text='', value=['NO', 'RECORDS', 'FOUND', '!!!'])

        scores_screen.mainloop()

        game(user_id, password)

    def change_password():
        game_interface.destroy()

        def change_user_password():
            password_1 = new_password_entry_1.get()
            password_2 = new_password_entry_2.get()

            if password_1 != password_2:
                messagebox.showwarning('WARNING', 'Passwords do not match')

            else:
                my_database = mysql.connector.connect(host='localhost', user='root',
                                                      password=password,
                                                      database='school_project')
                cursor = my_database.cursor()
                cursor.execute('update passwords set password = "{}" where '
                               'user_id = "{}"'.format(password_1, user_id))
                my_database.commit()

                new_password_window.destroy()

        def back_function():
            new_password_window.destroy()

        new_password_window = Tk()
        new_password_window.title('CHANGE PASSWORD')
        new_password_window.resizable(False, False)
        new_password_window.geometry('348x68+509+340')
        new_password_window.focus_force()

        image_file = PhotoImage(file='Images\\user.png')
        image = Label(new_password_window, image=image_file)
        image.grid(row=0, column=0, rowspan=3)

        password_info = Label(new_password_window, text='NEW PASSWORD: ')
        password_info.grid(row=0, column=1)

        new_password_entry_1 = Entry(new_password_window, show='*')
        new_password_entry_1.grid(row=0, column=2)
        new_password_entry_1.focus_set()

        re_enter_password_info = Label(new_password_window,
                                       text='RE ENTER NEW PASSWORD: ')
        re_enter_password_info.grid(row=1, column=1)

        new_password_entry_2 = Entry(new_password_window, show='*')
        new_password_entry_2.grid(row=1, column=2)

        confirm_button = Button(new_password_window, text='CHANGE',
                                command=change_user_password)
        confirm_button.grid(row=2, column=1, sticky=W+E)

        cancel_button = Button(new_password_window, text='CANCEL',
                               command=back_function)
        cancel_button.grid(row=2, column=2, sticky=W+E)

        new_password_window.mainloop()

        game(user_id, password)

    game_interface = Tk()
    game_interface.config(bg='purple')
    game_interface.iconbitmap('Video transitions/Logo.ico')
    game_interface.title('GAME LIST')
    game_interface.resizable(False, False)
    game_interface.geometry('520x461+423+143')
    game_interface.after(1, lambda: game_interface.focus_force())

    bg = ImageTk.PhotoImage(Image.open('Images/bg.jpg'))
    bg_placement = Label(game_interface, image=bg)
    bg_placement.place(x=0, y=0)

    user_frame = LabelFrame(game_interface, padx=7, pady=7, bg='dark gray')
    user_frame.grid(row=0, column=0, columnspan=3, sticky=W+E+N+S, padx=10, pady=10)
    user = Label(user_frame, text='Welcome ' + user_id.lower(),
                 font=('Helvetica', 28), pady=4)
    user.pack(anchor=CENTER)

    snake_image = ImageTk.PhotoImage(Image.open('Images/snake.png'))
    game_1_frame = LabelFrame(game_interface, padx=7, pady=7, bg='white')
    game_1_frame.grid(row=1, column=0, sticky=W+E+N+S, padx=10, pady=10)
    game_1 = Button(game_1_frame, image=snake_image, command=game_button_1)
    game_1.grid(row=0, column=0, sticky=W+E+N+S)
    game_1_text = Label(game_1_frame, text='SNAKE GAME',
                        font=('TIMES NEW ROMAN', 13))
    game_1_text.grid(row=1, column=0, sticky=W+E+N+S)

    space_image = ImageTk.PhotoImage(Image.open('Images/spaceship.png'))
    game_2_frame = LabelFrame(game_interface, padx=7, pady=7, bg='white')
    game_2_frame.grid(row=1, column=1, sticky=W+E+N+S, padx=10, pady=10)
    game_2 = Button(game_2_frame, image=space_image, command=game_button_2)
    game_2.grid(row=0, column=0, sticky=W+E+N+S)
    game_2_text = Label(game_2_frame, text='SPACE INVASION',
                        font=('TIMES NEW ROMAN', 13))
    game_2_text.grid(row=1, column=0, sticky=W + E + N + S)

    bird_image = ImageTk.PhotoImage(Image.open('Images/robin.png'))
    game_3_frame = LabelFrame(game_interface, padx=7, pady=7, bg='white')
    game_3_frame.grid(row=1, column=2, sticky=W+E+N+S, padx=10, pady=10)
    game_3 = Button(game_3_frame, image=bird_image, command=game_button_3)
    game_3.grid(row=0, column=0, sticky=W+E+N+S)
    game_3_text = Label(game_3_frame, text='FLAPPY BIRD', font=('TIMES NEW ROMAN', 13))
    game_3_text.grid(row=1, column=0, sticky=W + E + N + S)

    info_frame = LabelFrame(game_interface, padx=12, pady=7, bg='gray')
    info_frame.grid(row=2, column=0, columnspan=3, sticky=W+E+N+S, padx=10, pady=10)

    but_1 = Button(info_frame, text='MY SCORES', command=my_scores, pady=8,
                   font=('TIMES NEW ROMAN', 13))
    but_1.grid(row=0, column=0, sticky=W+E+N+S, pady=10, padx=10)

    but_2 = Button(info_frame, text='HIGHEST SCORES', padx=25, command=high_scores,
                   pady=8, font=('TIMES NEW ROMAN', 13))
    but_2.grid(row=0, column=1, sticky=W+E+N+S, pady=10, padx=10)

    but_3 = Button(info_frame, text='CHANGE PASSWORD', padx=25, command=change_password,
                   pady=8, font=('TIMES NEW ROMAN', 13))
    but_3.grid(row=1, column=0, sticky=W + E + N + S, pady=10, padx=10)

    but_4 = Button(info_frame, text='LOGOUT', command=exit_button, pady=8,
                   font=('TIMES NEW ROMAN', 13))
    but_4.grid(row=1, column=1, sticky=W+E+N+S, pady=10, padx=10)

    game_interface.protocol('WM_DELETE_WINDOW', exit_button)

    game_interface.mainloop()
