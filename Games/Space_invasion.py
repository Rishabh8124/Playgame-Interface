# Space invasion text
space_text = '''The main ||SPACE SHIP|| is under your control.You can move it along the line using ||LEFT AND RIGHT ARROW KEYS||
There are aliens coming from the top. The aim is to shoot them. For shooting press the ||SPACE BAR||.
Each level has some number of aliens. You win that level if you shoot all the aliens.
You get out if any one alien reaches the height of the space ship.

KEY INSTRUCTIONS:
Left and Right Arrow - Move the ship left and right
Esc - Pause
'''

import pygame
import random
import mysql.connector
from pygame import mixer
from tkinter import *
from tkinter import ttk

score_count = 0
level_update = 0

def escape_window(password):
    def resume_function():
        pause_screen.destroy()

    def high_scores():
        pause_screen.destroy()

        database = mysql.connector.connect(host='localhost', user='root', password=password, database='School_project')
        cursor = database.cursor()
        cursor.execute('Select * from space_invasion_scores order by score desc')
        result = cursor.fetchall()

        if not result:
            result = [('No', 'Records', 'Found!')]

        def back_function():
            scores_screen.destroy()

        scores_screen = Tk()
        scores_screen.title('SPACE INVASION SCORES')
        scores_screen.geometry('400x201+483+273')
        scores_screen.after(1, lambda: scores_screen.focus_force())
        scores_screen.resizable(False, False)

        score_frame = Frame(scores_screen)
        score_frame.grid(row=0, column=0)

        back = Button(scores_screen, text='BACK', command=back_function)
        back.grid(row=1, column=0, sticky=N + S + W + E, pady=4)

        scroll = Scrollbar(score_frame, orient=VERTICAL)
        scroll.pack(side=RIGHT, fill='y')

        high_score = ttk.Treeview(score_frame, height=7, yscrollcommand=scroll.set)
        high_score.pack()

        scroll.config(command=high_score.yview)

        high_score['columns'] = ("User_id", "Highest score", "Level")

        high_score.column("#0", width=0, stretch=NO)
        high_score.column("User_id", anchor=CENTER, width=180)
        high_score.column("Highest score", anchor=CENTER, width=100)
        high_score.column("Level", anchor=CENTER, width=100)

        high_score.heading('User_id', text='User_id', anchor=CENTER)
        high_score.heading('Highest score', text='Highest score', anchor=CENTER)
        high_score.heading('Level', text='Level', anchor=CENTER)

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
        instruction_window.title('SPACE INVASION GAME INSTRUCTIONS')
        instruction_window.geometry('1351x338+4+205')
        instruction_window.after(1, lambda: instruction_window.focus_force())
        instruction_window.resizable(False, False)

        instruction = Label(instruction_window, text=space_text, font=('TIMES NEW ROMAN', 20), bg='light pink')
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

    image_file = PhotoImage(file='Games\\Space_Invasion\\Images\\spaceship.png')
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

def space_invasion(level, user_id, password):
    global score_count, level_update

    life = 3
    exit_state = False

    while level:
        pygame.init()

        # Screen
        screen = pygame.display.set_mode((800, 650))
        pygame.display.set_caption('!!SPACE INVASION!!')

        # Background
        background = pygame.image.load('Games\\Space_Invasion\\Images\\photo.jpg')

        # Player
        player_image = pygame.image.load('Games\\Space_Invasion\\Images\\ship.png')
        player_x = 370
        player_y = 520
        player_change = 0

        # Enemies
        enemy = []
        enemy_change = 0.05 + level/250
        enemy_image = pygame.image.load('Games\\Space_Invasion\\Images\\enemy.png')
        for i in range(level + 2):
            enemy_x = random.randint(0, 735)
            enemy_y = 50
            enemy.append([enemy_image, [enemy_x, enemy_y], 0])

        # Bullets
        bullets = []
        bullet_change = 3
        bullet_image = pygame.image.load('Games\\Space_Invasion\\Images\\bullet.png')

        # Score
        score_count = 0
        font = pygame.font.Font('freesansbold.ttf', 32)

        # BGM
        mixer.music.load('Games\\Space_Invasion\\Audio\\bgm.mp3')
        mixer.music.play(-1)

        start = True
        game_state = True
        win_state = False

        while start:
            screen.fill((100, 100, 100))

            font_1 = pygame.font.Font('freesansbold.ttf', 72)
            level_render = font_1.render('LEVEL ' + str(level), True, (255, 250, 155))
            entry_statement = font.render('PRESS SPACE TO START', True, (255, 250, 155))
            aliens_statement = font.render('NO OF ALIENS: ' + str(level * (level+2)), True, (255, 250, 155))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_state = False
                    level_update = level
                    level = 0
                    start = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        start = False

                    elif event.key == pygame.K_ESCAPE:
                        mixer.music.pause()
                        escape_window(password)
                        mixer.music.unpause()
                        pygame.event.get()
                        break

            if start:
                screen.blit(level_render, (275, 200))
                screen.blit(entry_statement, (225, 300))
                screen.blit(aliens_statement, (275, 350))
                pygame.display.update()

        while game_state:

            # Screen altering
            screen.fill((100, 100, 100))
            screen.blit(background, (0, 50))

            # Checking keys
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    game_state = False
                    level_update = level
                    level = 0

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player_change = -0.25
                    elif event.key == pygame.K_RIGHT:
                        player_change = +0.25

                    elif event.key == pygame.K_SPACE:
                        bullet_sound = mixer.Sound('Games\\Space_Invasion\\Audio\\laser.mp3')
                        bullet_sound.play()

                        bullet_x = player_x + 20
                        bullet_y = player_y + 10
                        bullets.append([bullet_image, [bullet_x, bullet_y]])

                    elif event.key == pygame.K_ESCAPE:
                        mixer.music.pause()
                        escape_window(password)
                        mixer.music.unpause()
                        pygame.event.get()
                        break

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        player_change = 0

            if game_state:
                # Altering positions
                if 0 <= player_x + player_change <= 736:
                    player_x += player_change
                screen.blit(player_image, (player_x, player_y))

                for i in enemy:
                    i[1][1] += enemy_change

                j = 0
                while j < len(bullets):
                    bullets[j][1][1] -= bullet_change
                    if bullets[j][1][1] <= 50:
                        del bullets[j]
                    else:
                        j += 1

                i = j = 0
                while i < len(bullets):
                    while j < len(enemy):
                        if (enemy[j][1][1] - 10 <= bullets[i][1][1] <= enemy[j][1][1] + 50) and (enemy[j][1][0] - 10 <= bullets[i][1][0] <= enemy[j][1][0] + 50):
                            del bullets[i]
                            score_count += 1
                            hit_sound = mixer.Sound('Games\\Space_Invasion\\Audio\\die.mp3')
                            hit_sound.play()

                            if enemy[j][2] < level-1:
                                enemy[j][2] += 1
                                enemy[j][1][0] = random.randint(0, 735)
                                enemy[j][1][1] = 50
                            else:
                                del enemy[j]
                            break
                        else:
                            j += 1
                    i += 1

                for i in range(len(enemy)):
                    if enemy[i][1][1] >= 450:
                        life -= 1
                        if not life:
                            del enemy[:]
                            die_sound = mixer.Sound('Games\\Space_Invasion\\Audio\\life.mp3')
                            die_sound.play()
                            game_state = False
                            break

                        else:
                            life_sound = mixer.Sound('Games\\Space_Invasion\\Audio\\life.mp3')
                            life_sound.play()
                            if enemy[i][2] < level-1:
                                enemy[i][2] += 1
                                enemy[i][1][0] = random.randint(0, 735)
                                enemy[i][1][1] = 50
                            else:
                                del enemy[i]
                            break

                    screen.blit(enemy[i][0], (enemy[i][1][0], enemy[i][1][1]))

                for i in bullets:
                    screen.blit(i[0], (i[1][0], i[1][1]))

                score = font.render('Score : ' + str(score_count), True, (255, 255, 255))
                level_render = font.render('Level : ' + str(level), True, (255, 255, 255))
                life_render = font.render('Life : ' + str(life), True, (255, 255, 255))
                pygame.draw.rect(screen, (0, 0, 0), [0, 0, 800, 50])
                screen.blit(score, (23, 10))
                screen.blit(level_render, (645, 10))
                screen.blit(life_render, (340, 10))

                # Updating
                pygame.display.update()

                # Ending
                if not game_state:
                    game_state = False
                    level_update = level
                    level = 0

                if not enemy and game_state:
                    level += 1
                    game_state = False

            else:
                level_update = level
                level = 0

        level_sound = mixer.Sound('Games\\Space_Invasion\\Audio\\level.mp3')
        level_sound.play()
        while not game_state and level and not win_state:
            screen.fill((100, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    win_state = True
                    game_state = False
                    level_sound = mixer.Sound('Games\\Space_Invasion\\Audio\\level.mp3')
                    level_sound.play()

                elif event.type == pygame.KEYDOWN:
                    win_state = True
                    level_sound = mixer.Sound('Games\\Space_Invasion\\Audio\\level.mp3')
                    level_sound.play()

            if not win_state:
                key_display = font.render('PRESS ANY KEY', True, (255, 255, 255))
                score_display = font.render('SCORE :' + str(score_count), True, (255, 255, 255))
                out_display = font.render('YOU WIN! LEVEL COMPLETED', True, (255, 255, 255))
                screen.blit(key_display, (295, 255))
                screen.blit(out_display, (185, 315))
                screen.blit(score_display, (335, 365))

                pygame.display.update()

    mixer.music.stop()
    my_db = mysql.connector.connect(host='localhost', user='root', password=password, database='School_project')
    cursor = my_db.cursor()
    cursor.execute('insert into space_invasion_scores values("{}", {}, {})'.format(user_id, score_count, level_update))
    my_db.commit()

    cursor.execute('select * from space_invasion_scores')
    scores = cursor.fetchall()
    rank = scores.index((user_id, score_count, level_update))

    while not exit_state and not level:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                die_sound = mixer.Sound('Games\\Space_Invasion\\Audio\\die.mp3')
                die_sound.play()
                pygame.display.quit()
                exit_state = True

            elif event.type == pygame.KEYDOWN:
                die_sound = mixer.Sound('Games\\Space_Invasion\\Audio\\die.mp3')
                die_sound.play()
                pygame.display.quit()
                exit_state = True

        if not exit_state:
            key_display = font.render('PRESS ANY KEY TO EXIT', True, (255, 255, 255))
            score_display = font.render('SCORE :' + str(score_count), True, (255, 255, 255))
            level_display = font.render('LEVEL :' + str(level_update), True, (255, 255, 255))
            out_display = font.render('YOU ARE OUT! GAME OVER', True, (255, 255, 255))
            rank_display = font.render('Rank : ' + str(rank), True, (255, 255, 255))
            screen.blit(key_display, (215, 225))
            screen.blit(out_display, (195, 285))
            screen.blit(score_display, (235, 335))
            screen.blit(level_display, (425, 335))
            screen.blit(rank_display, (320, 385))

            pygame.display.update()
