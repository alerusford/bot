import config
from modules import stt # преобразуем голос в текст
from modules import tts # преобразуем текст в голос
from num2words import num2words
import webbrowser
import requests
import openai
import telebot
from telebot import types
import json
import traceback
import time
import os
# from datetime import datetime
from threading import Thread
# from io import BytesIO
# from PIL import Image
# from fuzzywuzzy import fuzz
# import random
import subprocess
import threading
import platform
import psutil
import speedtest
from bs4 import BeautifulSoup




thisFile = os.path.abspath(__file__)
openai.api_key = config.openai_apikey
bot = telebot.TeleBot(config.telegram_apikey)

print(' - this is ', thisFile)

def va_respond(voice: str):
    print(' - вопрос: ', voice)

    # if voice.startswith(config.VA_ALIAS):
    #     # cmd = recognize_cmd(filter_cmd(voice))
    #     cmd = filter_cmd(voice)
    #     print(' - va_respond cmd: ', cmd)
    #     cmd_split = cmd.split()
    #
    #     if cmd == 'тест':
    #         print(' - ТЕСТ! - ')
    #
    #     elif 'найди' in cmd_split:
    #         print(' - cmd_split: ', cmd_split)
    #         print(' - запускаем чат бот!')
    #
    #     for k, v in config.VA_CMD_LIST.items():
    #         if cmd in v:
    #             print(' - find! key: ', k)
    #             execute_cmd(k)
    #             break
    #         else:
    #             time_start = datetime.now()
    #
    #             response = openai.Completion.create(
    #                 model='text-davinci-003',
    #                 prompt=cmd,
    #                 temperature=0.5,
    #                 max_tokens=2000,
    #                 top_p=1.0,
    #                 frequency_penalty=0.5,
    #                 presence_penalty=0.0,
    #             )
    #
    #             answer_chatgpt = response['choices'][0]['text']
    #             print(' - вопрос: ', cmd)
    #             print(' - ответ: ', answer_chatgpt)
    #             print(' - ответ длина: ', len(answer_chatgpt))
    #
    #             time_end = datetime.now()
    #             time_request = time_end - time_start
    #             print(' - время запроса:', time_request)
    #             # tts.va_speak(answer_chatgpt)
    #             # bot.send_message(chat_id=message.from_user.id, text=f"{response['choices'][0]['text']}")
    #     # else:
    #     #     print(' - Что?')
    #     #     tts.va_speak("Что?")


# def filter_cmd(raw_voice: str):
#     cmd = raw_voice
#     for x in config.VA_ALIAS:
#         cmd = cmd.replace(x, "").strip()
#     for x in config.VA_TBR:
#         cmd = cmd.replace(x, "").strip()
#     print(' - filter_cmd: ', cmd)
#     return cmd


# def recognize_cmd(cmd: str):
#     print(' - recognize_cmd: ', cmd)
#     rc = {'cmd': '', 'percent': 0}
#     for c, v in config.VA_CMD_LIST.items():
#         for x in v:
#             # vrt = fuzz.ratio(cmd, x)
#             vrt = cmd, x
#             print(' - vrt:', vrt)
#             if vrt > rc['percent']:
#                 rc['cmd'] = c
#                 rc['percent'] = vrt
#     print(' - rc: ', rc)
#     return rc
#     print(cmd)
#     return cmd

# команды
# def execute_cmd(cmd: str):
#     if cmd == 'help':
#         print(' - execute_cmd help: ', cmd)
#         # help
#         text = "Я умею: ..."
#         text += "произносить время ..."
#         text += "узнавать погоду ..."
#         text += "и открывать браузер"
#         tts.va_speak(text)
#         pass
#
#     elif cmd == 'ctime':
#         print(' - execute_cmd ctime: ', cmd)
#         # current time
#         now_hours = num2words(datetime.now().hour, lang='ru')
#         now_minutes = num2words(datetime.now().minute, lang='ru')
#         text = "Сейчас " + now_hours + ' ' + now_minutes
#         print(' - ответ: ', text)
#         tts.va_speak(text)
#
#     elif cmd == 'open_browser':
#         webbrowser.open("http://python.org")
#
#     elif cmd == 'weather':
#             params = {'q': 'Kolomna', 'units': 'metric', 'lang': 'ru', 'appid': config.weather_apikey}
#             response = requests.get(f'https://api.openweathermap.org/data/2.5/weather', params=params)
#             w = response.json()
#             gradus_text = num2words(round(w['main']['temp']), lang='ru')
#             gradus_int = int(round(w['main']['temp']))
#             print(f"На улице {w['weather'][0]['description']} {gradus_text}")
#             if gradus_int == 1 or gradus_int == -1 or gradus_int == 21 or gradus_int == -21:
#                 tts.va_speak(f"На улице, {w['weather'][0]['description']}, {gradus_text} градус.")
#             elif gradus_int in [2, 3, 4] or gradus_int in [-2, -3, -4]:
#                 tts.va_speak(f"На улице, {w['weather'][0]['description']}, {gradus_text} градуса.")
#             elif gradus_int >= 5 or gradus_int >= -5:
#                 if gradus_int in [22, 23, 24, 32, 33, 34] or gradus_int in [-22, -23, -24, -32, -33, -34]:
#                     tts.va_speak(f"На улице, {w['weather'][0]['description']}, {gradus_text} градуса.")
#                 else:
#                     tts.va_speak(f"На улице, {w['weather'][0]['description']}, {gradus_text} градусов.")


def sleep_timer(timer):
    time.sleep(timer)
    subprocess.run(['systemctl', 'suspend'])

@bot.message_handler(commands=['start'])
def start(message):
    print(message.from_user)
    if message.from_user.username == config.users or config.admins:
        # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="тыг") # изменить сообщение
        # bot.answer_callback_query(message.chat.id, text=output_tg) # всплывающее
        # bot.send_message(chat_id=message.chat.id, text=output_tg)  # просто сообщение
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("👋 Поздороваться")
        btn2 = types.KeyboardButton("❓ Задать вопрос")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, f'Привет {message.from_user.id}! Я - бот.', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, f'у {message.from_user.id} | {message.from_user.username} нет доступа!')

@bot.message_handler(commands=['list'])
def handle_text(message):
    if message.from_user.username in config.admins:
        for i in range(threading.active_count()):
            bot.send_message(message.chat.id, f'{threading.enumerate()[i].name}')
    else:
        bot.send_message(message.chat.id, f'у {message.from_user.id} | {message.from_user.username} нет доступа!')


# о системе
@bot.message_handler(commands=['top'])
def system_info(message):
    if message.from_user.username in config.admins:

        my_system = platform.uname()
        virtual_memory = psutil.virtual_memory()
        disk_usage = psutil.disk_usage('/')
        io_stats = psutil.net_io_counters()
        cpu_percent = psutil.cpu_percent(interval=0.1)
        battery_info = psutil.sensors_battery()

        # todo протестируй и выведи параметры LA и CPU fan в /top под Linux
        # if my_system.system == 'Linux':
        #     # temp = psutil.sensors_temperatures()
        #     print('LA: ', round(psutil.getloadavg()[0], 2), '|', round(psutil.getloadavg()[1], 2), '|',
        #           round(psutil.getloadavg()[2], 2))
        #     fans = psutil.sensors_fans()
        #     for fan in fans.values():
        #         for x in fan:
        #             print('CPU fan: ', x.current)
        # else:
        #     pass
        #     # print('Нет условия для системы ', my_system.system)

        # print()
        # print("Sent data: " + f"{round(io_stats.bytes_sent / (1024 * 1024 * 1024), 3)} GB")
        # print("Received: " + f"{round(io_stats.bytes_recv / (1024 * 1024 * 1024), 3)} GB")
        # print()
        # print("Battery Percent : " + f"{battery_info.percent} %")

        result_tg = f"System: {my_system.system}\n" \
                    f"Host name: {my_system.node}\n\n" \
                    f"RAM: {round(virtual_memory.total / (1024 * 1024 * 1024), 2)} GB | Free {round(virtual_memory.available / (1024 * 1024 * 1024), 2)} GB\n" \
                    f"ROM: {round(disk_usage.total / (1024 * 1024 * 1024), 2)} GB | Free {round(disk_usage.free / (1024 * 1024 * 1024), 2)} GB\n\n" \
                    f"CPU: {cpu_percent} %\n\n"\
                    f"Sent data: {round(io_stats.bytes_sent / (1024 * 1024 * 1024), 3)} GB\n"\
                    f"Received: " + f"{round(io_stats.bytes_recv / (1024 * 1024 * 1024), 3)} GB\n\n"\
                    f"Battery Percent: {battery_info.percent} %\n"

        if battery_info.secsleft > 0:
            result_tg += f"Time Left {round(battery_info.secsleft / 60, 2)} minutes / {round(battery_info.secsleft / 3600, 2)} hrs\n"
        else:
            result_tg += f"Status : " + "Battery is charging!\n"

        if my_system.system == 'Windows':
            temp_battery = psutil.sensors_battery()
            result_tg += f'Temperature: {temp_battery.percent}\n'

        bot.send_message(message.chat.id, result_tg)

    else:
        bot.send_message(message.chat.id, f'у {message.from_user.id} | {message.from_user.username} нет доступа!')

# проверка скорости интернета
@bot.message_handler(commands=['speed_test'])
def speed_test(message):
    if message.from_user.username in config.admins:
        speedTester = speedtest.Speedtest()
        speedTester.get_servers()
        best = speedTester.get_best_server()
        result_tg_one = f"Host: {best['host']}\n"\
                        f"Network Sponsor: {best['sponsor']}\n"\
                        f"Location: {best['name']} , {best['country']}\n" \
                        f"Country Code: {best['cc']}\n" \
                        f"Co-Ordinates: Lat : {best['lat']} , Lon: {best['lon']}\n\n"

        result_tg_two = f"Performing Download Speed Test...\n"\
                        f"Performing Upload Speed Test...\n"
        msg = bot.send_message(message.chat.id, f"{result_tg_one}{result_tg_two}")
        downloadSpeed = speedTester.download()
        uplaodSpeed = speedTester.upload()
        ping = speedTester.results.ping
        result_speed = f"Download Speed : {round(downloadSpeed / 1024 / 1024, 2)} Mbit/s\n"\
                       f"Upload Speed : {round(uplaodSpeed / 1024 / 1024, 2)} Mbit/s\n"\
                       f"Ping : {ping} ms"
        bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text=f'{result_tg_one}\n{result_speed}')
    else:
        bot.send_message(message.chat.id, f'у {message.from_user.id} | {message.from_user.username} нет доступа!')



@bot.message_handler(commands=['sleep'])
def sleep(message):
    if message.from_user.username in config.admins:
        timer = 0
        threading.Thread(target=sleep_timer, name='sleep_timer_60', args=[timer]).start()
    else:
        bot.send_message(message.chat.id, f'у {message.from_user.id} | {message.from_user.username} нет доступа!')

@bot.message_handler(commands=['sleep_60'])
def sleep_60(message):
    if message.from_user.username in config.admins:
        timer = 10 # 3600
        threading.Thread(target=sleep_timer, name='sleep_timer_60', args=[timer]).start()
    else:
        bot.send_message(message.chat.id, f'у {message.from_user.id} | {message.from_user.username} нет доступа!')

@bot.message_handler(commands=['sleep_120'])
def sleep_120(message):
    if message.from_user.username in config.admins:
        timer = 7200
        threading.Thread(target=sleep_timer, name='sleep_timer_120', args=[timer]).start()
    else:
        bot.send_message(message.chat.id, f'у {message.from_user.id} | {message.from_user.username} нет доступа!')

@bot.message_handler(commands=['sleep_180'])
def sleep_120(message):
    if message.from_user.username in config.admins:
        timer = 10800
        threading.Thread(target=sleep_timer, name='sleep_timer_180', args=[timer]).start()
    else:
        bot.send_message(message.chat.id, f'у {message.from_user.id} | {message.from_user.username} нет доступа!')


@bot.message_handler(func=lambda _: True)
# @bot.message_handler(content_types=['text'])
def handle_message(message):

    if message.text == "👋 Поздороваться":
        bot.send_message(message.chat.id, text="Привет)")
    elif message.text == "❓ Задать вопрос":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Как меня зовут?")
        btn2 = types.KeyboardButton("Что я могу?")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, text="Задай мне вопрос", reply_markup=markup)

    elif 'check_username' in message.text:
        username = message.text.split()[1]
        print(' - input: ', username)

        def username_check():
            _headers = {
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
                'Content-Type': 'application/json; charset=utf-8',
                'server': 'nginx/1.0.4',
                'x-runtime': '148ms',
                'etag': '"e1ca502697e5c9317743dc078f67693f"',
                'Access-Control-Allow-Credentials': 'true',
            }

            session = requests.session()
            website_list = {
                # CODEFORCES
                'codeforces': f'https://codeforces.com/profile/{username}',
                # GITHUB
                'github': f'https://www.github.com/{username}',
                # REPL.IT
                'repl_it': f'https://replit.com/@{username}',
                # HACKER EARTH
                'hacker_earth': f'https://www.hackerearth.com/{username}',
                # LEETCODE
                'leetcode': f'https://leetcode.com/{username}',
                # LinkedIn
                'linkedin': f'https://www.linkedin.com/in/{username}',
                # INSTAGRAM
                'instagram': f'https://www.instagram.com/{username}/',
                # SNAPCHAT
                'snapchat': f'https://www.snapchat.com/add/{username}',
                # FACEBOOK
                'facebook': f'https://www.facebook.com/{username}',
                # TWITTER
                'twitter': f'https://www.twitter.com/{username}',
                # YOUTUBE
                'youtube': f'https://www.youtube.com/{username}',
                # BLOGGER
                'blogger': f'https://{username}.blogspot.com',
                # GOOGLE+
                'google_plus': f'https://plus.google.com/s/{username}/top',
                # REDDIT
                'reddit': f'https://www.reddit.com/user/{username}',
                # WORDPRESS
                'wordpress': f'https://{username}.wordpress.com',
                # PINTEREST
                'pinterest': f'https://www.pinterest.com/{username}',
                # TUMBLR
                'tumblr': f'https://{username}.tumblr.com',
                # FLICKR
                'flickr': f'https://www.flickr.com/people/{username}',
                # STEAM
                'steam': f'https://steamcommunity.com/id/{username}',
                # VIMEO
                'vimeo': f'https://vimeo.com/{username}',
                # SOUNDCLOUD
                'soundcloud': f'https://soundcloud.com/{username}',
                # DISQUS
                'disqus': f'https://disqus.com/by/{username}',
                # MEDIUM
                'medium': f'https://medium.com/@{username}',
                # DEVIANTART
                'deviantart': f'https://{username}.deviantart.com',
                # VK
                'vk': f'https://vk.com/{username}',
                # ABOUT.ME
                'aboutme': f'https://about.me/{username}',
                # IMGUR
                'imgur': f'https://imgur.com/user/{username}',
                # FLIPBOARD
                'flipboard': f'https://flipboard.com/@{username}',
                # SLIDESHARE
                'slideshare': f'https://slideshare.net/{username}',
                # FOTOLOG
                'fotolog': f'https://fotolog.com/{username}',
                # SPOTIFY
                'spotify': f'https://open.spotify.com/user/{username}',
                # MIXCLOUD
                'mixcloud': f'https://www.mixcloud.com/{username}',
                # SCRIBD
                'scribd': f'https://www.scribd.com/{username}',
                # BADOO
                'badoo': f'https://www.badoo.com/en/{username}',
                # PATREON
                'patreon': f'https://www.patreon.com/{username}',
                # BITBUCKET
                'bitbucket': f'https://bitbucket.org/{username}',
                # DAILYMOTION
                'dailymotion': f'https://www.dailymotion.com/{username}',
                # ETSY
                'etsy': f'https://www.etsy.com/shop/{username}',
                # CASHME
                'cashme': f'https://cash.me/{username}',
                # BEHANCE
                'behance': f'https://www.behance.net/{username}',
                # GOODREADS
                'goodreads': f'https://www.goodreads.com/{username}',
                # INSTRUCTABLES
                'instructables': f'https://www.instructables.com/member/{username}',
                # KEYBASE
                'keybase': f'https://keybase.io/{username}',
                # KONGREGATE
                'kongregate': f'https://kongregate.com/accounts/{username}',
                # LIVEJOURNAL
                'livejournal': f'https://{username}.livejournal.com',
                # ANGELLIST
                'angellist': f'https://angel.co/{username}',
                # LAST.FM
                'last_fm': f'https://last.fm/user/{username}',
                # DRIBBBLE
                'dribbble': f'https://dribbble.com/{username}',
                # CODECADEMY
                'codecademy': f'https://www.codecademy.com/{username}',
                # GRAVATAR
                'gravatar': f'https://en.gravatar.com/{username}',
                # PASTEBIN
                'pastebin': f'https://pastebin.com/u/{username}',
                # FOURSQUARE
                'foursquare': f'https://foursquare.com/{username}',
                # ROBLOX
                'roblox': f'https://www.roblox.com/user.aspx?username={username}',
                # GUMROAD
                'gumroad': f'https://www.gumroad.com/{username}',
                # NEWSGROUND
                'newsground': f'https://{username}.newgrounds.com',
                # WATTPAD
                'wattpad': f'https://www.wattpad.com/user/{username}',
                # CANVA
                'canva': f'https://www.canva.com/{username}',
                # CREATIVEMARKET
                'creative_market': f'https://creativemarket.com/{username}',
                # TRAKT
                'trakt': f'https://www.trakt.tv/users/{username}',
                # 500PX
                'five_hundred_px': f'https://500px.com/{username}',
                # BUZZFEED
                'buzzfeed': f'https://buzzfeed.com/{username}',
                # TRIPADVISOR
                'tripadvisor': f'https://tripadvisor.com/members/{username}',
                # HUBPAGES
                'hubpages': f'https://{username}.hubpages.com',
                # CONTENTLY
                'contently': f'https://{username}.contently.com',
                # HOUZZ
                'houzz': f'https://houzz.com/user/{username}',
                # WIKIPEDIA
                'wikipedia': f'https://www.wikipedia.org/wiki/User:{username}',
                # HACKERNEWS
                'hackernews': f'https://news.ycombinator.com/user?id={username}',
                # CODEMENTOR
                'codementor': f'https://www.codementor.io/{username}',
                # REVERBNATION
                'reverb_nation': f'https://www.reverbnation.com/{username}',
                # BANDCAMP
                'bandcamp': f'https://www.bandcamp.com/{username}',
                # COLOURLOVERS
                'colourlovers': f'https://www.colourlovers.com/love/{username}',
                # IFTTT
                'ifttt': f'https://www.ifttt.com/p/{username}',
                # EBAY
                'ebay': f'https://www.ebay.com/usr/{username}',
                # SLACK
                'slack': f'https://{username}.slack.com',
                # OKCUPID
                'okcupid': f'https://www.okcupid.com/profile/{username}',
                # TRIP
                'trip': f'https://www.trip.skyscanner.com/user/{username}',
                # ELLO
                'ello': f'https://ello.co/{username}',
                # TRACKY
                'tracky': f'https://tracky.com/user/~{username}',
                # BASECAMP
                'basecamp': f'https://{username}.basecamphq.com/login'
            }
            found_list = []
            notincluded = ["sorry", "doesn't exist", "doesn't", "Try", "error", "nobody", "not"]
            msg = bot.send_message(message.chat.id, f" --->>> {username} <<<--- \n")
            result_tg = '--->>> {username} <<<--- \n'

            for individual_website in website_list:
                URL = website_list[individual_website]

                try:
                    response = session.get(URL, timeout=7, headers=_headers)
                    soup = BeautifulSoup(response.text, 'lxml')

                    if response.status_code == 200:
                        flagCount = 0
                        data = " ".join(soup.text.strip().split())
                        for each in notincluded:
                            if (each in data):
                                flagCount += 1
                        if flagCount < 2 and (username in data or individual_website):
                            result_tg += f'[+] {individual_website} - найден {username}!\n'
                            bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id,
                                                  text=f'{result_tg}\n')
                        elif (flagCount >= 2 and username in data):
                            result_tg += f'[!] {individual_website} - что-то найдено ...\n'
                            bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id,
                                                  text=f'{result_tg}\n')
                        else:
                            result_tg += f'[-] {individual_website} - не найден ...\n'
                            bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id,
                                                  text=f'{result_tg}\n')
                    else:
                        result_tg += f'[-] {individual_website} - не найден ...\n'
                        bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id,
                                              text=f'{result_tg}\n')

                except Exception as e:
                    result_tg += f'[!] {individual_website} ошибка!\n'
                    bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id,
                                          text=f'{result_tg}\n')

        username_check()



    else:
        response = openai.Completion.create(
            model='text-davinci-003',
            prompt=message.text,
            temperature=0.5,
            max_tokens=2000,
            top_p=1.0,
            frequency_penalty=0.5,
            presence_penalty=0.0,
        )

        print('\n - user: ', message.from_user.username)
        print(' - question: ', message.text)
        print(' - response: ', response['choices'][0]['text'])
        bot.send_message(chat_id=message.from_user.id, text=f"{response['choices'][0]['text']}")


def polling():
    bot.send_message('1077463086', 'i`m online 🫡')

    try:
        bot.polling(none_stop=True)
    except:
        traceback_error_string = traceback.format_exc()
        print("\r\n<<ERROR polling>>\r\n" + traceback_error_string + "\r\n<<ERROR polling>>")
        with open(config.file_error_log, "a") as myfile:
            myfile.write("\r\n\r\n" + time.strftime(
                "%c") + "\r\n<<ERROR polling>>\r\n" + traceback_error_string + "\r\n<<ERROR polling>>")
        bot.stop_polling()
        time.sleep(3)
        polling()



if __name__ == '__main__':
    thread_tg = Thread(target=polling)
    thread_vosk = Thread(target=stt.va_listen, args=(va_respond,))
    thread_tg.start()
    thread_vosk.start()

