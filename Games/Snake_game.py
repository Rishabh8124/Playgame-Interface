# Snake text
snake_text = '''The ||BROWN SQUARE|| in the screen is the snake.
It can move around in all directions. Use ||ARROW KEYS|| to move around.
The main aim is to hit the ||RED SQUARE|| which pops at random positions.
On hitting the red square you get one point and the length of the snake increases by 1
You get out when you touch the boundaries or when the head touches the body of the snake.
The score is calculated by the number of red squares you hit.

KEY INSTRUCTIONS:
Arrow - Move the snake
Esc - Pause
'''

import pygame
import random
import mysql.connector
from tkinter import *
from tkinter import ttk
from pygame import mixer

def escape_window(password):
    database = mysql.connector.connect(host='localhost', user='root', password=password, database='School_project')
    cursor = database.cursor()
    cursor.execute('select * from snake_scores order by score desc')
    result1 = cursor.fetchall()

    def resume_function():
        pause_screen.destroy()

    def high_scores():
        pause_screen.destroy()

        result = result1

        if not result:
            result = [('No', 'Records')]

        def back_function():
            scores_screen.destroy()

        scores_screen = Tk()
        scores_screen.title('SNAKE GAME SCORES')
        scores_screen.geometry('300x141+533+303')
        scores_screen.after(1, lambda: scores_screen.focus_force())
        scores_screen.resizable(False, False)

        score_frame = Frame(scores_screen)
        score_frame.grid(row=0, column=0)

        back = Button(scores_screen, text='BACK', command=back_function)
        back.grid(row=1, column=0, sticky=N + S + W + E, pady=4)

        scroll = Scrollbar(score_frame, orient=VERTICAL)
        scroll.pack(side=RIGHT, fill='y')

        high_score = ttk.Treeview(score_frame, height=4, yscrollcommand=scroll.set)
        high_score.pack()

        scroll.config(command=high_score.yview)

        high_score['columns'] = ("User_id", "Highest score")

        high_score.column("#0", width=0, stretch=NO)
        high_score.column("User_id", anchor=CENTER, width=180)
        high_score.column("Highest score", anchor=CENTER, width=100)

        high_score.heading('User_id', text='User_id', anchor=CENTER)
        high_score.heading('Highest score', text='Highest score', anchor=CENTER)

        for position in range(len(result)):
            result[position] = list(result[position])
            result[position][0] = result[position][0].title()
            high_score.insert(parent='', index=END, iid=position, text='', value=result[position])

        scores_screen.mainloop()

        escape_window(password)

    def instruction_button_display():
        pause_screen.destroy()

        # Instructions Window
        def back():
            instruction_window.destroy()

        instruction_window = Tk()
        instruction_window.title('SNAKE GAME INSTRUCTIONS')
        instruction_window.geometry('1021x400+172+174')
        instruction_window.after(1, lambda: instruction_window.focus_force())
        instruction_window.resizable(False, False)

        instruction = Label(instruction_window, text=snake_text, font=('TIMES NEW ROMAN', 20), bg='light green')
        instruction.grid(row=0, column=0)

        start_button = Button(instruction_window, text='BACK', command=back, pady=8, font=('TIMES NEW ROMAN', 15))
        start_button.grid(row=1, column=0, sticky=W + E)

        instruction_window.mainloop()
        escape_window(password)

    pause_screen = Tk()
    pause_screen.title('PAUSE')
    pause_screen.geometry('253x262+556+238')
    pause_screen.after(1, lambda: pause_screen.focus_force())
    pause_screen.resizable(False, False)

    image_file = PhotoImage(file='Games\\Snake game\\Images\\Pause.png')
    image = Label(pause_screen, image=image_file)
    image.grid(row=0, column=0, columnspan=2)

    resume = Button(pause_screen, padx=25, text='RESUME', command=resume_function, font=('Times New Roman', 13))
    resume.grid(row=1, column=0, sticky=W + E)

    scores = Button(pause_screen, text='SCORES', padx=25, command=high_scores, font=('Times New Roman', 13))
    scores.grid(row=1, column=1, sticky=W + E)

    instruction_button = Button(pause_screen, text='GAME INSTRUCTIONS', padx=25, command=instruction_button_display, font=('Times New Roman', 13))
    instruction_button.grid(row=2, column=0, columnspan=2, sticky=W + E)

    pause_screen.mainloop()

def snake_game(user_id, password):
    pygame.init()

    screen = pygame.display.set_mode((800, 650))

    # Snake
    snake_positions = []
    length = 1
    x_change = 0
    y_change = 0
    shead_x = 400
    shead_y = 350

    # Apple
    apple_x = random.randint(1, 79) * 10
    apple_y = random.randint(6, 64) * 10

    # Score
    score = 0
    font = pygame.font.Font('freesansbold.ttf', 32)

    # BGM
    mixer.music.load('Games\\Snake game\\Audio\\bgm.mp3')
    mixer.music.play(-1)

    clock = pygame.time.Clock()

    database = mysql.connector.connect(host='localhost', user='root', password=password, database='School_project')
    cursor = database.cursor()
    cursor.execute('select * from snake_scores order by score desc')
    result1 = cursor.fetchall()
    scores = [int(i[1]) for i in result1]

    game_state = True
    exit_state = False
    start_message = True

    rank = len(scores) + 1

    while game_state:
        screen.fill((0, 0, 0))
        key_state = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                die_sound = mixer.Sound('Games\\Snake game\\Audio\\die.mp3')
                die_sound.play()
                game_state = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not x_change and key_state:
                    x_change = -10
                    y_change = 0
                    key_state = False
                    start_message = False

                elif event.key == pygame.K_RIGHT and not x_change and key_state:
                    x_change = 10
                    y_change = 0
                    key_state = False
                    start_message = False

                elif event.key == pygame.K_UP and not y_change and key_state:
                    y_change = -10
                    x_change = 0
                    key_state = False
                    start_message = False

                elif event.key == pygame.K_DOWN and not y_change and key_state:
                    y_change = +10
                    x_change = 0
                    key_state = False
                    start_message = False

                elif event.key == pygame.K_ESCAPE:
                    mixer.music.pause()
                    escape_window(password)
                    mixer.music.unpause()
                    pygame.event.get()
                    break

        shead_x += x_change
        shead_y += y_change
        if 790 <= shead_x or shead_x < 10 or shead_y < 60 or shead_y >= 640:
            die_sound = mixer.Sound('Games\\Snake game\\Audio\\die.mp3')
            die_sound.play()
            game_state = False

        if (shead_x, shead_y) in snake_positions and length > 1:
            die_sound = mixer.Sound('Games\\Snake game\\Audio\\die.mp3')
            die_sound.play()
            game_state = False

        snake_positions.append((shead_x, shead_y))

        if len(snake_positions) > length:
            del snake_positions[0]

        if (apple_x, apple_y) == (shead_x, shead_y):
            length += 1
            apple_sound = mixer.Sound('Games\\Snake game\\Audio\\apple.mp3')
            apple_sound.play()
            score += 1

            scores_new = scores + [score]
            scores_new.sort(reverse=True)

            rank = scores_new.index(score)

            while (apple_x, apple_y) in snake_positions:
                apple_x = random.randint(1, 78) * 10
                apple_y = random.randint(6, 63) * 10

        grass_x = 0
        grass_y = 50

        while grass_x <= 800:
            grass_y = 50
            while grass_y <= 650:
                if (((grass_y-50)//10) % 2 and (grass_x//10) % 2) or not (((grass_y-50)//10) % 2 or (grass_x//10) % 2):
                    pygame.draw.rect(screen, (0, 200, 0), [grass_x, grass_y, 10, 10])
                else:
                    pygame.draw.rect(screen, (0, 175, 0), [grass_x, grass_y, 10, 10])
                grass_y += 10
            grass_x += 10

        for i in range(len(snake_positions)):
            pygame.draw.rect(screen, (100, 0, 0), [snake_positions[i][0], snake_positions[i][1], 10, 10])

        pygame.draw.rect(screen, (227, 132, 0), [0, 0, 800, 50])
        pygame.draw.rect(screen, (0, 0, 0), [0, 0, 800, 2])
        pygame.draw.rect(screen, (0, 0, 0), [0, 0, 2, 50])
        pygame.draw.rect(screen, (0, 0, 0), [0, 48, 800, 2])
        pygame.draw.rect(screen, (0, 0, 0), [798, 0, 2, 50])
        pygame.draw.rect(screen, (250, 200, 0), [0, 50, 800, 10])
        pygame.draw.rect(screen, (250, 200, 0), [0, 640, 800, 10])
        pygame.draw.rect(screen, (250, 200, 0), [0, 50, 10, 650])
        pygame.draw.rect(screen, (250, 200, 0), [790, 50, 10, 650])

        score_count = font.render('Score : ' + str(score), True, (0, 0, 0))
        screen.blit(score_count, (15, 10))

        rank_display = font.render('Rank : ' + str(rank), True, (0, 0, 0))
        screen.blit(rank_display, (645, 10))

        pygame.draw.rect(screen, (255, 0, 0), [apple_x, apple_y, 10, 10])

        if start_message:
            start_display = font.render('PRESS ANY ARROW KEY TO MOVE THE SNAKE', True, (255, 255, 255))
            screen.blit(start_display, (25, 105))

        pygame.display.update()
        clock.tick(15)

    my_db = mysql.connector.connect(host='localhost', user='root', password=password, database='School_project')
    cursor = my_db.cursor()
    cursor.execute('insert into snake_scores values("{}", {})'.format(user_id, score))
    my_db.commit()

    mixer.music.stop()

    while not exit_state:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                die_sound = mixer.Sound('Games\\Snake game\\Audio\\life.mp3')
                die_sound.play()
                pygame.display.quit()
                exit_state = True

            elif event.type == pygame.KEYDOWN:
                die_sound = mixer.Sound('Games\\Snake game\\Audio\\life.mp3')
                die_sound.play()
                pygame.display.quit()
                exit_state = True

        if not exit_state:
            key_display = font.render('PRESS ANY KEY TO EXIT', True, (255, 255, 255))
            score_display = font.render('SCORE :'+str(score), True, (255, 255, 255))
            out_display = font.render('YOU ARE OUT! GAME OVER', True, (255, 255, 255))
            rank_display = font.render('Rank : ' + str(rank), True, (255, 255, 255))
            screen.blit(key_display, (215, 255))
            screen.blit(out_display, (195, 315))
            screen.blit(score_display, (315, 365))
            screen.blit(rank_display, (320, 415))

            pygame.display.update()
