import customtkinter
from tkinter import *
import threading

# Window settings
window = Tk()
window.geometry("400x350")
window.title("Goofy ahh bot 2.0 | microphone: inactive")
window.iconbitmap("Images/icon.ico")
window.resizable(False, False)
window.configure(bg='white')
image = PhotoImage(file="Images/mic.png").subsample(5)
image2 = PhotoImage(file="Images/mic2.png").subsample(5)

# Center the window
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_width = 400
window_height = 350
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
window.geometry(f"{window_width}x{window_height}+{x}+{y}")


# Function for mic button
def button_function():
    global listening
    if listening == False:
        listening = True
        print("Listening...")
        window.title("Virtual assistant | microphone: active")
        button.configure(image=image)
        window.iconbitmap("Images/icon2.ico")
    else:
        listening = False
        print("Listening is over")
        window.title("Virtual assistant | microphone: inactive")
        button.configure(image=image2)
        window.iconbitmap("Images/icon.ico")
button = customtkinter.CTkButton(master=window, corner_radius=25, command=button_function, width=70, height=70, image=image2, text='', fg_color='#000000', hover_color='#303030')
button.place(relx=0.5, rely=0.8, anchor=CENTER)



# Bot voice vizualisation
frameCount = 22
frames = [PhotoImage(file='Images/voice1.gif',format = 'gif -index %i' %(i)).subsample(3) for i in range(frameCount)]
def update(ind):
    global animate
    if animate == True:
        frame = frames[ind]
        ind += 1
        if ind == frameCount:
            ind = 0
        label.configure(image=frame)
        window.after(50, update, ind)
label = Label(window)
label.pack()
label.configure(bg='white')
label.place(relx=0.5, rely=0.35, anchor=CENTER)
animate = True
update(0)
#window.after(0, update, 0)
animate = False

import json, pyaudio
from vosk import Model, KaldiRecognizer
import pyttsx3
from difflib import SequenceMatcher
import subprocess
from datetime import datetime
from random import randint
import openai
import os
import requests
import webbrowser

# Set up voice recognition model
model = Model('vosk-model-small-ru-0.22')
rec = KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

# Set up openai api (key.txt file must be in the same directory as this python script)
f = open('key.txt', 'r')
API_KEY=f.read()
f.close()
os.environ['OPENAI_API_KEY'] =API_KEY
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set up open weather api key
api_key = '0999965ff4552c8cc2263f8b29acbbe2'
location = 'Almaty'

# Set up voice engine
engine = pyttsx3.init()
engine.setProperty('voice', engine.getProperty('voices')[0].id)
current_command = ''

# Bot voice
def say(text):
    global animate
    animate = True
    window.after(0, update, 0)
    engine.say(text)
    engine.runAndWait()
    update(0)
    animate = False
    window.after(0, update, 0)


# Text similarity
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

# Various functions
def open_chrome():
    print("Bot: ", end='')
    replies = ['Открываю!', 'Момент', 'Секунду']
    res = replies[randint(0, len(replies) - 1)]
    print(res)
    say(res)
    subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe')
def greeting():
    print("Bot: ", end='')
    list_of_greetings = ['Дарова!', 'Привет!', 'Здравствуй!', 'Салют!', 'Приветствую!', 'Здравия желаю!', 'Ты где пропадал?', 'Гутэн моргэн!']
    word_to_say = list_of_greetings[randint(0, len(list_of_greetings)-1)]
    print(word_to_say)
    say(word_to_say)
def goodbye():
    print("Bot: ", end='')
    list_of_greetings = ['Всего хорошего!', 'Бай бай!', 'Адьос!', 'Удачи!']
    word_to_say = list_of_greetings[randint(0, len(list_of_greetings) - 1)]
    print(word_to_say)
    say(word_to_say)
    window.quit()
def say_time():
    print("Bot: ", end='')
    now = datetime.now()
    h = now.hour
    chas = [1,21]
    chasa = [2,3,4,22,23,24]
    if h in chas:
        word_to_say = 'Сейчас ' + now.strftime('%H час %M минут')
    elif h in chasa:
        word_to_say = 'Сейчас ' + now.strftime('%H часа %M минут')
    else:
        word_to_say = 'Сейчас ' + now.strftime('%H часов %M минут')
    print(word_to_say)
    say(word_to_say)
waiting_for_rpc = False
def rock_paper_scissors():
    global waiting_for_rpc
    if waiting_for_rpc == False:
        print("Bot: Давай, вы ходите первыми")
        say('Давай, вы ходите первыми')
        waiting_for_rpc = True
    else:
        options = ['камень','ножницы','бумага']
        option = options[randint(0, len(options)-1)]
        print("Bot:",option)
        say(option)
        if current_command == option:
            say('Ничья')
        elif (current_command == 'камень' and option == 'ножницы') or (current_command == 'ножницы' and option == 'бумага') or (current_command == 'бумага' and option == 'камень'):
            say('Вы проиграли')
        else:
            say('Вы проиграли')
def weather():
    url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&units=metric&lang=ru&appid={api_key}'
    result = requests.get(url)

    if result.status_code == 200:
        data = result.json()
        temperature = data['main']['temp']
        description = data['weather'][0]['description']
        print(f"Bot: В Алмате,{description},температура {temperature} °C" )
        say(f"В Алмате,{description},температура {temperature} градусов цельсия" )
    else:
        print("Bot: Не удалось получить данные о погоде.")
        say("Bot: Не удалось получить данные о погоде.")
def tell_quote():
    replies = ['Если заблудился в лесу, иди домой',
               'Чем богаче дача, джими джими ача ача',
               'Не суди, да не судимым будишь, не будии, да небуди дабудай',
               'Не круто пить, не круто врать, круто маме помогать',
               'Мотоцикл это транспорт, . . . дальше не придумал пока',
               'Хороший асфальт на дороге не валяется',
               'Принять мужчину таким каким он есть может только, военкомат']
    res = replies[randint(0, len(replies) - 1)]
    print("Bot: ", res)
    say(res)
def tell_joke():
    replies = ['У всех машин есть дворники, но не у всех дворников есть машины',
               'Как то раз один городской тип купил посёлок, теперь это посёлок городского типа',
               'Если на ногах ногти, то на руках рукти',
               'Не стоит расчитывать на таксистов, они могут нас подвести',
               'Если сделать греческий салат на 31 декабря, то на следующий день он станет, древнегреческим']
    res = replies[randint(0, len(replies) - 1)]
    print("Bot: ", res)
    say(res)
def open_youtube():
    print("Bot: ", end='')
    replies = ['Открываю!', 'Момент', 'Секунду']
    res = replies[randint(0, len(replies) - 1)]
    print(res)
    say(res)
    url = "https://www.youtube.com"
    webbrowser.open(url)
def open_spotify():
    print("Bot: ", end='')
    replies = ['Открываю!', 'Момент', 'Секунду']
    res = replies[randint(0, len(replies) - 1)]
    print(res)
    say(res)
    url = "https://open.spotify.com/"
    webbrowser.open(url)
def open_openai():
    print("Bot: ", end='')
    replies = ['Открываю!', 'Момент', 'Секунду']
    res = replies[randint(0, len(replies) - 1)]
    print(res)
    say(res)
    url = "https://chat.openai.com/"
    webbrowser.open(url)
def open_github():
    print("Bot: ", end='')
    replies = ['Открываю!', 'Момент', 'Секунду']
    res = replies[randint(0, len(replies) - 1)]
    print(res)
    say(res)
    url = "https://github.com/"
    webbrowser.open(url)


# Default commands list
commands = {
    'открой хром': open_chrome,
    'привет': greeting,
    'здравствуй': greeting,
    'сколько время': say_time,
    'камень ножницы бумага': rock_paper_scissors,
    'ножницы': rock_paper_scissors,
    'камень': rock_paper_scissors,
    'бумага': rock_paper_scissors,
    'погода': weather,
    'шутку': tell_joke,
    'цитату': tell_quote,
    'открой ютуб': open_youtube,
    'открой чат джепяти': open_openai,
    'открой спотифай': open_spotify,
    'выключись': goodbye,
    'открой гид хаб': open_github
}

# Function for command recognition
def recognize_command(command):
    if listening == True:
        print("You:", command)
        global current_command
        current_command = command
        similarities = [0]*len(commands)
        similarities_c = ['']*len(commands)
        i=0
        c=''
        for key, value in commands.items():
            similarities[i] = similar(command.lower(), key.lower())
            similarities_c[i] = key
            i+=1
        if max(similarities) >= 0.55:
            index = similarities.index(max(similarities))
            commands[similarities_c[index]]()
            return
        #If not recognized
        completion = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": command}
            ]
        )
        res = completion.choices[0].message.content
        print("Bot:",res)
        say(res)
    else:
        print("Вы пытаетесь говорить? Включите микрофон")


# Listening function
def listen():
    while True:
        data = stream.read(8000, exception_on_overflow=False)
        if (rec.AcceptWaveform(data)) and (len(data) > 0):
            answer = json.loads(rec.Result())
            if answer['text']:
                yield answer['text']


# When model loaded, it is output
print('Model loaded!')
listening = False
# When voice command received, the function recognize_command() starts
def start_voice_recognition():
    for text in listen():
        recognize_command(text)


# Multi processes
voice_thread = threading.Thread(target=start_voice_recognition)
voice_thread.daemon = True
voice_thread.start()

window.mainloop()
