import telebot
from difflib import SequenceMatcher
from random import*
import openai
import os
import wave
from vosk import Model, KaldiRecognizer
import json
import requests
import webbrowser
import subprocess
from datetime import datetime
import pyttsx3
from telebot import types
import time


# Set up telegram bot
bot = telebot.TeleBot('7113066147:AAFZQ9D6Y67ltV9y7-03QSpK2UCs2JEdiKk')

# Set up openai api (key.txt file must be in the same directory as this python script)
f = open('key.txt', 'r')
API_KEY=f.read()
f.close()
os.environ['OPENAI_API_KEY'] =API_KEY
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set up vosk voice recognition model
model = Model('vosk-model-small-ru-0.22')
rec = KaldiRecognizer(model, 16000)

# Set up open weather api key
api_key = '0999965ff4552c8cc2263f8b29acbbe2'
location = 'Almaty'

# Set up bot voice engine
engine = pyttsx3.init()
engine.setProperty('voice', engine.getProperty('voices')[2].id)



def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def say_and_save(text, filename="out.mp3"):
    engine.save_to_file(text, filename)
    engine.runAndWait()


chat_link = None
text_mode = True
def say(text):
    global text_mode
    global chat_link
    if text_mode:
        bot.send_message(chat_link, text)
    else:
        say_and_save(text, 'out.mp3')
        audio_file = open('out.mp3', 'rb')
        bot.send_audio(chat_link, audio_file)



# Yes no command
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == 'yes':
        global waiting_for_rpc
        waiting_for_rpc = False
        recognize_command("камень ножницы бумага")
    elif call.data == 'no':
        bot.send_message(call.message.chat.id, "Это печально")
    bot.answer_callback_query(call.id)


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
        if current_command == option:
            result = option+'... Вы проиграли'
            print("Bot:",option,'Вы проиграли')
            say(result)
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton("да", callback_data='yes')
            button2 = types.InlineKeyboardButton("нет", callback_data='no')
            markup.row(button1, button2)
            bot.send_message(chat_link, 'Хотите сыграть ещё раз?', reply_markup=markup)
        elif (current_command == 'камень' and option == 'ножницы') or (current_command == 'ножницы' and option == 'бумага') or (current_command == 'бумага' and option == 'камень'):
            result = option+'... Вы проиграли'
            print("Bot:",option,'Вы проиграли')
            say(result)
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton("да", callback_data='yes')
            button2 = types.InlineKeyboardButton("нет", callback_data='no')
            markup.row(button1, button2)
            bot.send_message(chat_link, 'Хотите сыграть ещё раз?', reply_markup=markup)
        else:
            result = option+'... Вы проиграли'
            print("Bot:",option,'Вы проиграли')
            say(result)
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton("да", callback_data='yes')
            button2 = types.InlineKeyboardButton("нет", callback_data='no')
            markup.row(button1, button2)
            bot.send_message(chat_link, 'Хотите сыграть ещё раз?', reply_markup=markup)
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
    url = "https://github.com/wabys32/goofy-ahh-voice-assistant"
    webbrowser.open(url)
def switch_to_voice_mode():
    global text_mode
    if text_mode:
        text_mode = False
        print("Bot: переключено: режим речи")
        say("переключено: режим речи")
    else:
        print("Bot: уже в режиме речи")
        say("уже в режиме речи")
def switch_to_text_mode():
    global text_mode
    if not text_mode:
        text_mode = True
        print("Bot: переключено в текстовый режим")
        say("переключено в текстовый режим")
    else:
        print("Bot: уже в текстовом режиме")
        say("уже в текстовом режиме")



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
    'открой гид хаб': open_github,
    'переключись на текстовый режим': switch_to_text_mode,
    'переключись на голосовой режим': switch_to_voice_mode
}

def recognize_command(command):
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


# Default commands ============================
@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}, I\'m goofy ahh bot. \nHow can I assist you today?', parse_mode='html')




import librosa
import soundfile as sf
import json
@bot.message_handler(content_types=['voice'])
def handle_voice_message(message):
    global downloaded_file
    global transcribed_text_list
    file_id = message.voice.file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open('aud.wav', 'wb') as f:
        f.write(downloaded_file)
    command = recognise_sound()
    global chat_link 
    chat_link = message.chat.id
    recognize_command(command)
    #bot.send_message(message.chat.id, command)

    

def recognise_sound() -> str:
    x,_ = librosa.load('./aud.wav', sr=16000)
    sf.write('tmp.wav', x, 16000)
    wf = wave.open("tmp.wav", "rb")
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        rec.AcceptWaveform(data)
    result = rec.FinalResult()
    result_dict = json.loads(result)
    wf.close()
    os.remove('aud.wav')
    os.remove('tmp.wav')
    return result_dict['text']
    
        


# Messages ====================================
@bot.message_handler()
def main(message):
    global chat_link 
    chat_link = message.chat.id
    msg = message.text.lower()
    recognize_command(msg)

    


print('Bot is ready!')
bot.polling(none_stop=True)
