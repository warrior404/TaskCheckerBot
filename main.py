#!/usr/bin/python3.7
'''
Example: https://github.com/eternnoir/pyTelegramBotAPI/blob/master/examples/step_example.py
'''
from config import TG_TOKEN
from funcs import *
from classes import *
import os

import pandas as pd

import telebot

import requests


# TELEGRAM MODULE-------------------------------------------------------------------------------------------------------
# Проверка связи
BASE_URL = 'https://api.telegram.org/bot' + TG_TOKEN + '/'
print('Соединяюсь с телеграмм...')
r = requests.get(BASE_URL+'getMe').json()
if r['ok'] == True:
    print('Соединение с телеграмм установлено')

# Запуск бота
bot = telebot.TeleBot(TG_TOKEN)

# # Разрешаем получение обновлений из чата (если бот в чате). Также попробуйте зайти в настройки в @BotFather
# bot.get_updates(allowed_updates=["message"])

# Логин бота
bot_name = bot.get_me().username
print(bot_name, 'готов к работе\n')

# Создание словаря - user_id: timezone
user_dict = {}


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Команда выводит все методы класса
    # print(call.message.__dict__)

    # Если сообщение из чата с ботом
    if call.message:
        if call.data == "Да":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выполнено✅')
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Done")
        elif call.data == 'Нет':
            task_checker(bot, user_dict[str(call.message.chat.id)], call.message.reply_to_message, call.data)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='В прогрессе⏳')
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Keep going")
        return


# Handle '/start'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    msg = bot.reply_to(message, """\
Камчатка, Чукотка - UTC/GMT+12
Магадан, Верхоянск, Сахалин, Владивосток - UTC/GMT+10
Якутск - UTC/GMT+9
Иркутск - UTC/GMT+8
Красноярск - UTC/GMT+7
Омск - UTC/GMT+6
Екатеринбург - UTC/GMT+5
Самара, Ижевск - UTC/GMT+4
Москва  Московское время - UTC/GMT+3
Париж  "Среднеевропейское (Центральноевропейское) время" - UTC/GMT+1
Лондон "Гринвичское время" - UTC/GMT+0
"Среднеатлантическое время" - UTC/GMT-2
Аргентина, Буэнос-Айрес - UTC/GMT-3
Канада,  "Атлантическое время" - UTC/GMT-4
США, Нью-Йорк.  "Восточное время" - UTC/GMT-5
Чикаго (Chicago). "Центральное время" - UTC/GMT-6
Денвер (Denver), "Горное время" - UTC/GMT-7
США, Лос-Анджелес, Сан-Франциско - UTC/GMT-8

Привет! Я помогу тебе проследить за исполнением задач.
Какой у тебя часовой пояс? (см. клавиутуру)
""", reply_markup=utc_keyboard())

    bot.register_next_step_handler(msg, get_user_utc)


def get_user_utc(message):
    try:
        # Основные параметры сообщения
        text = str(message.text)
        id = str(message.chat.id)
        username = str(message.from_user.username)
        # print(text)

        # Создадим объект юзера и добавим его в словарь чатов
        user = User(username)
        user_dict[id] = user
        # print(f'Объект User создан: {user.username}')

        # Конвертируем отсуп UTC в int
        utc_offset = int(text.split(' ')[1])
        user_dict[id].utc_offset = utc_offset

        # Время старта по timezone юзера
        tz_start_time = dt.datetime.utcnow() + dt.timedelta(hours=utc_offset)
        user_dict[id].tz_start_time = tz_start_time

        # Спросим часы работы
        msg = bot.reply_to(message, 'Во сколько ты начинаешь работу?', reply_markup=hours_kb())

        # Передадим сообщение дальше
        bot.register_next_step_handler(msg, get_start_hours)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def get_start_hours(message):
    try:
        # Основные параметры сообщения
        text = str(message.text)
        id = str(message.chat.id)
        username = str(message.from_user.username)
        # print(text)

        # Параметры полученного времени
        start_h = int(text.split(':')[0])
        start_m = int(text.split(':')[1])

        # Получим время старта работы и время конца работы юзера
        user_now_time = dt.datetime.utcnow() + dt.timedelta(hours=user_dict[id].utc_offset)
        user_start_time = dt.datetime.combine(user_now_time.date(), dt.time(start_h, start_m),
                                              user_now_time.tzinfo).time()
        user_dict[id].start_time = user_start_time

        # Спросим часы работы
        msg = bot.reply_to(message, 'Во сколько заканчиваешь работу?', reply_markup=hours_kb())

        # Передадим сообщение дальше
        bot.register_next_step_handler(msg, get_end_hours)

    except Exception as e:
        bot.reply_to(message, 'oooops')


def get_end_hours(message):
    try:
        # Основные параметры сообщения
        text = str(message.text)
        id = str(message.chat.id)
        username = str(message.from_user.username)
        # print(text)

        # Параметры полученного времени
        end_h = int(text.split(':')[0])
        end_m = int(text.split(':')[1])

        # Получим время конца работы юзера
        user_now_time = dt.datetime.utcnow() + dt.timedelta(hours=user_dict[id].utc_offset)
        user_end_time = dt.datetime.combine(user_now_time.date(), dt.time(end_h, end_m),
                                            user_now_time.tzinfo).time()
        user_dict[id].end_time = user_end_time

        # Инфо сообщение +  приглашение написать/переслать задачу
        text = f'Отлично, {user_dict[id].username}!\nТвой Timezone: {"UTC " + str(user_dict[id].utc_offset)}\n' \
               f'Твои часы работы: {str(user_dict[id].start_time)[:5]} - {str(user_dict[id].end_time)[:5]}\n\n' \
               f'Для начала работы, напиши или перешли мне задачу, о которой не хочешь забыть.'
        bot.send_message(id, text, reply_markup=types.ReplyKeyboardRemove())
        print(f'Новый пользователь!\nUsername: {username}; Timezone: {"UTC " + str(user_dict[id].utc_offset)}; '
              f'Working Hours: {str(user_dict[id].start_time)[:5]} - {str(user_dict[id].end_time)[:5]}\n')
    except Exception as e:
        bot.reply_to(message, 'oooops')


# Handle '/timer'
@bot.message_handler(commands=['timer'])
def send_welcome(message):
    msg = bot.reply_to(message, """\
Эта команда нужна для измения времени таймера между пушами твоих нотификаций по задачам.

Введи желаемое количество минут:
""")
    bot.register_next_step_handler(msg, change_timer)


def change_timer(msg):
    try:
        # Основные параметры сообщения
        text = str(msg.text)
        id = str(msg.chat.id)

        # Условие для отлова незарегистрированных
        try:
            user = user_dict[id]
        except Exception:
            bot.reply_to(msg, 'Вначале пройди регистрацию. Используй команду /start')
            return

        # Изменим таймер
        if text.isdigit():
            user.timer = int(text)*60
            bot.reply_to(msg, 'Время изменено')
        else:
            bot.reply_to(msg, 'Не принято. Перезапустите команду /timer и введите численное значение.')

    except Exception as e:
        print('oops change_timer(msg)', e)

    return


# Handle '/bag_report'
@bot.message_handler(commands=['bag_report'])
def send_welcome(message):
    msg = bot.reply_to(message, """\
Эта команда нужна для сообщения о найденном баге.

Опишите проблему:
""")
    bot.register_next_step_handler(msg, bag_rep)


def bag_rep(msg):
    try:
        # Основные параметры сообщения
        text = str(msg.text)
        id = str(msg.chat.id)

        # Условие для отлова незарегистрированных
        try:
            user = user_dict[id]
        except Exception:
            bot.reply_to(msg, 'Вначале пройди регистрацию. Используй команду /start')
            return

        # Создадим файл и запишем в него сообщение
        mini_df = pd.DataFrame({'Username': [user.username],
                                'Bag_report': [text],
                                'Time': [str(dt.datetime.now().time())]})

        # Если файл csv не существует, => создадим. Существует? Дополним.
        if not os.path.exists('./BagReports.csv'):
            mini_df.to_csv('./BagReports.csv', index=False)
        else:
            main_df = pd.read_csv('./BagReports.csv')
            full_df = pd.concat([main_df, mini_df], ignore_index=True)
            full_df.to_csv('./BagReports.csv', index=False)

        # Ответ
        bot.reply_to(msg, 'Спасибо. Сообщение принято в обработку.')

    except Exception as e:
        print('bag_rep(msg)', e)

    return


# Хэндлер обработки сообщений в канале
@bot.message_handler(content_types='text')
def hello(task_msg):
    '''
    Здесь бот будет реагировать на новые текстовые сообщения
    '''
    # Основные параметры сообщения
    text = str(task_msg.text)
    id = str(task_msg.chat.id)
    user = user_dict[id]
    username = str(task_msg.from_user.username)
    print(f'{id + " @" + username}: {text}\n')

    # Проинформируем юзера, что задача принята
    bot.reply_to(task_msg, 'Задача принята')

    # Пополним список задач юзера
    user.tasks[len(user.tasks.keys()) + 1] = task_msg

    # Вызов функции решения - отправлять или нет
    task_checker(bot, user, task_msg, 'Нет')

    return


# Polling (конец бота)
while True:
    try:
        bot.polling()
    except Exception as e:
        print(e)
        print('Ошибка polling, засыпаю на 15сек')
        time.sleep(15)
# TELEGRAM MODULE-------------------------------------------------------------------------------------------------------
