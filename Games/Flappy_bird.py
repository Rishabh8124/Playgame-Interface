# Flappy bird text
bird_text = '''The ||BIRD|| is under your control. It will fly if you press the ||UP ARROW|| key.
There are walls through the way. Move the bird in order to dodge the walls.
The game ends if the bird hits the walls or the floor.

KEY INSTRUCTIONS:
UP Arrow - Move the bird up
Esc - Pause
'''

import pygame
import random
import mysql.connector
from tkinter import *
from tkinter import ttk
from pygame import mixer

def escape_window(password):
    def resume_function():
        pause_screen.destroy()

    def high_scores():
        pause_screen.destroy()

        database = mysql.connector.connect(host='localhost', user='root', password=password, database='School_project')
        cursor = database.cursor()
        cursor.execute('select * from flappy_bird_scores order by score desc')
        result = cursor.fetchall()

        if not result:
            result = [('No', 'Records')]

        def back_function():
            scores_screen.destroy()

        scores_screen = Tk()
        scores_screen.title('FLAPPY BIRD SCORES')
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
        instruction_window.title('FLAPPY BIRD GAME INSTRUCTIONS')
        instruction_window.geometry('882x307+242+220')
        instruction_window.after(1, lambda: instruction_window.focus_force())
        instruction_window.resizable(False, False)

        instruction = Label(instruction_window, text=bird_text, font=('TIMES NEW ROMAN', 20), bg='light pink')
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

    image_file = PhotoImage(file='Games\\Flappy bird\\Images\\robin.png')
    image = Label(pause_screen, image=image_file)
    image.grid(row=0, column=0, columnspan=2)

    resume = Button(pause_screen, padx=25, text='RESUME', command=resume_function, font=('Times New Roman', 13))
    resume.grid(row=1, column=0, sticky=W + E)

    scores = Button(pause_screen, text='SCORES', padx=25, command=high_scores, font=('Times New Roman', 13))
    scores.grid(row=1, column=1, sticky=W + E)

    instruction_button = Button(pause_screen, text='GAME INSTRUCTIONS', padx=25, command=instruction_button_display,
                                font=('Times New Roman', 13))
    instruction_button.grid(row=2, column=0, columnspan=2, sticky=W + E)

    pause_screen.mainloop()

def flappy_bird_game(password, user_id):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    game_state = True
    background = pygame.image.load('Games\\Flappy bird\\Images\\bg.jpeg')

    blocks = []
    j = 400
    while j < 800:
        x = random.randint(5, 45) * 10
        blocks.append([j, x, 150 + x])
        j += 240

    bird_image = pygame.image.load('Games\\Flappy bird\\Images\\bird.png')
    bird_x = 200
    bird_y = 300
    y_change = 0
    yy_change = 0
    blocks_change = 0

    q = 1

    clock = pygame.time.Clock()
    score = 0
    font = pygame.font.Font('freesansbold.ttf', 32)
    start_message = True
    exit_state = False

    database = mysql.connector.connect(host='localhost', user='root', password=password, database='School_project')
    cursor = database.cursor()
    cursor.execute('select * from flappy_bird_scores order by score desc')
    result = cursor.fetchall()

    scores = [int(i[1]) for i in result]
    rank = len(scores) + 1

    # BGM
    mixer.music.load('Games\\Flappy bird\\Audio\\bgm.mp3')
    mixer.music.play(-1)

    while game_state:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                die_sound = mixer.Sound('Games\\Flappy bird\\Audio\\die.mp3')
                die_sound.play()
                game_state = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    blocks_change = 10
                    y_change = -20
                    yy_change = 5
                    start_message = False

                    wing_sound = mixer.Sound('Games\\Flappy bird\\Audio\\wing.mp3')
                    wing_sound.play()

                if event.key == pygame.K_ESCAPE:
                    mixer.music.pause()
                    escape_window(password)
                    mixer.music.unpause()
                    pygame.event.get()
                    break

        if blocks[0][0] < -45:
            del blocks[0]
            score += 1
            score_sound = mixer.Sound('Games\\Flappy bird\\Audio\\point.mp3')
            score_sound.set_volume(10)
            score_sound.play()

            scores_new = scores + [score]
            scores_new.sort(reverse=True)

            rank = scores_new.index(score)

        if blocks[-1][0] < 660:
            x = random.randint(5, 45) * 10
            blocks.append([blocks[-1][0] + 240, x, 150 + x])

        bird_y += y_change
        y_change += yy_change

        if bird_y < 600:
            screen.fill((255, 255, 255))
            screen.blit(background, (0, 0))

            for i in range(len(blocks)):
                image1 = pygame.image.load('Games\\Flappy bird\\Images\\pipe1.png')
                screen.blit(image1, (blocks[i][0], blocks[i][1] - 517))
                image2 = pygame.image.load('Games\\Flappy bird\\Images\\pipe.png')
                screen.blit(image2, (blocks[i][0], blocks[i][2]))
                blocks[i][0] -= blocks_change
                if blocks[i][0] <= bird_x <= blocks[i][0] + 30 and (blocks[i][1] >= bird_y or bird_y >= blocks[i][2]):
                    game_state = False
                    die_sound = mixer.Sound('Games\\Flappy bird\\Audio\\die.mp3')
                    die_sound.play()
                    break
            screen.blit(bird_image, (bird_x, bird_y))

        else:
            die_sound = mixer.Sound('Games\\Flappy bird\\Audio\\die.mp3')
            die_sound.play()
            game_state = False
            break

        pygame.draw.rect(screen, (255, 255, 255), [0, 0, 175, 110])
        score_count = font.render('Score : ' + str(score), True, (0, 0, 0))
        screen.blit(score_count, (15, 10))
        rank_display = font.render('Rank : ' + str(rank), True, (0, 0, 0))
        screen.blit(rank_display, (15, 65))

        if start_message:
            start_display_1 = font.render('PRESS UP ARROW TO', True, (0, 0, 0))
            start_display_2 = font.render('MOVE THE BIRD', True, (0, 0, 0))
            screen.blit(start_display_1, (23, 205))
            screen.blit(start_display_2, (55, 245))

        pygame.display.update()
        clock.tick(15 + score//10)

    my_db = mysql.connector.connect(host='localhost', user='root', password=password, database='School_project')
    cursor = my_db.cursor()
    cursor.execute('insert into flappy_bird_scores values("{}", {})'.format(user_id, score))
    my_db.commit()
    mixer.music.stop()

    while not exit_state:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                die_sound = mixer.Sound('Games\\Flappy bird\\Audio\\life.mp3')
                die_sound.play()
                pygame.display.quit()
                exit_state = True

            elif event.type == pygame.KEYDOWN:
                die_sound = mixer.Sound('Games\\Flappy bird\\Audio\\life.mp3')
                die_sound.play()
                pygame.display.quit()
                exit_state = True

        if not exit_state:
            key_display = font.render('PRESS ANY KEY TO EXIT', True, (255, 255, 255))
            score_display = font.render('SCORE :'+str(score), True, (255, 255, 255))
            out_display = font.render('YOU ARE OUT! GAME OVER', True, (255, 255, 255))
            rank_display = font.render('Rank : ' + str(rank), True, (255, 255, 255))
            screen.blit(key_display, (215, 185))
            screen.blit(out_display, (195, 245))
            screen.blit(score_display, (315, 295))
            screen.blit(rank_display, (320, 345))

            pygame.display.update()
