# Video
import tkinter as tk
import threading
import playsound
import pygame
import imageio
from PIL import Image, ImageTk
from pygame import mixer

def play_video():
    pygame.init()

    video_name = 'Video transitions\\Title to Logo with audio.mp4'
    video = imageio.get_reader(video_name)

    def exit_function_video():
        root.attributes('-fullscreen', False)
        root.destroy()
        mixer.music.stop()

    def stream(label):
        global my_label

        mixer.music.load('Video transitions\\Audio.mp3')
        mixer.music.play(1)

        for image in video.iter_data():
            frame_image = ImageTk.PhotoImage(Image.fromarray(image))
            label.config(image=frame_image)
            label.image = frame_image

        root.after(100, exit_function_video)

    root = tk.Tk()
    root.attributes('-fullscreen', True)
    my_label = tk.Label(root)
    my_label.pack()
    thread = threading.Thread(target=stream, args=(my_label,))
    thread.daemon = 1
    thread.start()
    root.mainloop()


play_video()
