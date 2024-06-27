import os
import inspect

old_path = os.getcwd()

path = inspect.getfile(os).split('\\')
index = path.index('Python') + 2
del path[index:]
path = '\\'.join(path+['Scripts'])

os.chdir(path)
module_list = ['Pillow', 'mysql.connector', 'pyttsx3', 'tkvideo', 'pygame', 'playsound', 'imageio']
l = (os.popen('pip freeze'))

for module in module_list:
    x = os.popen('pip install ' + module)
    for i in x:
        if 'Requirement' not in i:
            print(i)

os.chdir(old_path)
