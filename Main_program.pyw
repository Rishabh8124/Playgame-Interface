"""
DESCRIPTION
Each user can register and login using user id and password (tkinter)
Userid, password, scores in each game will be saved in database (mysql.connector)
Text to speech conversion (pyttsx3)
Audio effects (playsound)
Game interface (pygame)

LIST OF GAMES:
-> Snake game
-> Space invasion
-> Flappy bird

FEATURES
-> Multiple Games
-> Login passwords(Database)
-> Compiled scores
"""

# Modules setup
import Modules_setup

# SQL setup
import SQL_setup
from SQL_setup import pass_input

# Video
# import Video

# User Ids from database
import mysql.connector

user_records = mysql.connector.connect(host='localhost', user='root', password=pass_input, database='school_project')
records = user_records.cursor()

# Audio
import pyttsx3

voice_engine_main = pyttsx3.init()
rate = voice_engine_main.getProperty('rate')
voices = voice_engine_main.getProperty('voices')
voice_engine_main.setProperty('voice', voices[0].id)
voice_engine_main.setProperty('rate', 175)

# Login
from Register_and_Login import login_using_user

# Interface
from Games_Interface import game

def gaming():
    playing = True

    while playing:
        # Login Interface
        user_id, login_status = login_using_user(pass_input)

        if login_status:
            voice_engine_main.setProperty('voice', voices[0].id)
            voice_engine_main.say('Successfully logged in')
            voice_engine_main.runAndWait()

            # Games Interface
            game(user_id, pass_input)

        else:
            playing = False

            voice_engine_main.setProperty('voice', voices[0].id)
            voice_engine_main.say('THANK YOU FOR PLAYING')
            voice_engine_main.runAndWait()


gaming()
