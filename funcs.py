#!/usr/bin/python3.7


from telebot import types

import time
import datetime as dt

import threading as th


def hours_kb():
    # Создадим систему кнопок для следующего вопроса
    keyboard = types.ReplyKeyboardMarkup()
    k0 = types.InlineKeyboardButton(text='00:00', callback_data='00:00')
    k1 = types.InlineKeyboardButton(text='01:00', callback_data='01:00')
    k2 = types.InlineKeyboardButton(text='02:00', callback_data='02:00')
    k3 = types.InlineKeyboardButton(text='03:00', callback_data='03:00')
    k4 = types.InlineKeyboardButton(text='04:00', callback_data='04:00')
    k5 = types.InlineKeyboardButton(text='05:00', callback_data='05:00')
    k6 = types.InlineKeyboardButton(text='06:00', callback_data='06:00')
    k7 = types.InlineKeyboardButton(text='07:00', callback_data='07:00')
    k8 = types.InlineKeyboardButton(text='08:00', callback_data='08:00')
    k9 = types.InlineKeyboardButton(text='09:00', callback_data='09:00')
    k10 = types.InlineKeyboardButton(text='10:00', callback_data='10:00')
    k11 = types.InlineKeyboardButton(text='11:00', callback_data='11:00')
    k12 = types.InlineKeyboardButton(text='12:00', callback_data='12:00')
    k13 = types.InlineKeyboardButton(text='13:00', callback_data='13:00')
    k14 = types.InlineKeyboardButton(text='14:00', callback_data='14:00')
    k15 = types.InlineKeyboardButton(text='15:00', callback_data='15:00')
    k16 = types.InlineKeyboardButton(text='16:00', callback_data='16:00')
    k17 = types.InlineKeyboardButton(text='17:00', callback_data='17:00')
    k18 = types.InlineKeyboardButton(text='18:00', callback_data='18:00')
    k19 = types.InlineKeyboardButton(text='19:00', callback_data='19:00')
    k20 = types.InlineKeyboardButton(text='20:00', callback_data='20:00')
    k21 = types.InlineKeyboardButton(text='21:00', callback_data='21:00')
    k22 = types.InlineKeyboardButton(text='22:00', callback_data='22:00')
    k23 = types.InlineKeyboardButton(text='23:00', callback_data='23:00')
    keyboard.add(k0, k1, k2)
    keyboard.add(k3, k4, k5)
    keyboard.add(k6, k7, k8)
    keyboard.add(k9, k10, k11)
    keyboard.add(k12, k13, k14)
    keyboard.add(k15, k16, k17)
    keyboard.add(k18, k19, k20)
    keyboard.add(k21, k22, k23)

    return keyboard


def yes_no():
    # Создадим систему кнопок для следующего вопроса
    new_keyboard = types.InlineKeyboardMarkup()
    k0 = types.InlineKeyboardButton(text='Да', callback_data='Да')
    k1 = types.InlineKeyboardButton(text='Нет', callback_data='Нет')
    new_keyboard.add(k0, k1)

    return new_keyboard


def utc_keyboard():
    # Создадим систему кнопок для следующего вопроса
    keyboard = types.ReplyKeyboardMarkup()
    k0 = types.InlineKeyboardButton(text='UTC -12', callback_data='UTC -12')
    k1 = types.InlineKeyboardButton(text='UTC -11', callback_data='UTC -11')
    k2 = types.InlineKeyboardButton(text='UTC -10', callback_data='UTC -10')
    k3 = types.InlineKeyboardButton(text='UTC -9', callback_data='UTC -9')
    k4 = types.InlineKeyboardButton(text='UTC -8', callback_data='UTC -8')
    k5 = types.InlineKeyboardButton(text='UTC -7', callback_data='UTC -7')
    k6 = types.InlineKeyboardButton(text='UTC -6', callback_data='UTC -6')
    k7 = types.InlineKeyboardButton(text='UTC -5', callback_data='UTC -5')
    k8 = types.InlineKeyboardButton(text='UTC -4', callback_data='UTC -4')
    k9 = types.InlineKeyboardButton(text='UTC -3', callback_data='UTC -3')
    k10 = types.InlineKeyboardButton(text='UTC -2', callback_data='UTC -2')
    k11 = types.InlineKeyboardButton(text='UTC 0', callback_data='UTC 0')
    k12 = types.InlineKeyboardButton(text='UTC +1', callback_data='UTC +1')
    k13 = types.InlineKeyboardButton(text='UTC +2', callback_data='UTC +2')
    k14 = types.InlineKeyboardButton(text='UTC +3', callback_data='UTC +3')
    k15 = types.InlineKeyboardButton(text='UTC +4', callback_data='UTC +4')
    k16 = types.InlineKeyboardButton(text='UTC +5', callback_data='UTC +5')
    k17 = types.InlineKeyboardButton(text='UTC +6', callback_data='UTC +6')
    k18 = types.InlineKeyboardButton(text='UTC +7', callback_data='UTC +7')
    k19 = types.InlineKeyboardButton(text='UTC +8', callback_data='UTC +8')
    k20 = types.InlineKeyboardButton(text='UTC +9', callback_data='UTC +9')
    k21 = types.InlineKeyboardButton(text='UTC +10', callback_data='UTC +10')
    k22 = types.InlineKeyboardButton(text='UTC +11', callback_data='UTC +11')
    k23 = types.InlineKeyboardButton(text='UTC +12', callback_data='UTC +12')
    keyboard.add(k0, k1, k2)
    keyboard.add(k3, k4, k5)
    keyboard.add(k6, k7, k8)
    keyboard.add(k9, k10, k11)
    keyboard.add(k12, k13, k14)
    keyboard.add(k15, k16, k17)
    keyboard.add(k18, k19, k20)
    keyboard.add(k21, k22, k23)

    return keyboard


def task_checker(bot, user, task_msg, ans):
    '''
    Функция отправки напоминающих сообщений юзеру.
    :param msg: Сообщение с задачей
    :return:
    '''

    # Задание функции отправляющей вопрос
    def ask_task(bot, user, task_msg):
        # Таймер
        time.sleep(user.timer)

        # Время юзера
        user_nowtime = dt.datetime.utcnow() + dt.timedelta(hours=user.utc_offset)

        # Булева переменная для рабочего времемни.
        working_hours = True if (user_nowtime.time() >= user.start_time) and \
                                (user_nowtime.time() <= user.end_time) else False

        # Если время юезра рабочее - спросим
        if working_hours:
            # Спросим статус
            bot.reply_to(task_msg, 'Задача выполнена?', reply_markup=yes_no())
        else:
            time.sleep(60*30)
            ask_task(bot, user, task_msg)

            return

    if ans == 'Нет':
        # Время юзера
        user_nowtime = dt.datetime.utcnow() + dt.timedelta(hours=user.utc_offset)

        # Булева переменная для рабочего времемни.
        working_hours = True if (user_nowtime.time() >= user.start_time) and \
                                (user_nowtime.time() <= user.end_time) else False

        # Цикл ожидания рабочих часов
        while not working_hours:
            # Спим
            time.sleep(60*60*1.5)

            # Время юзера
            user_nowtime = dt.datetime.utcnow() + dt.timedelta(hours=user.utc_offset)

            # Булева переменная для рабочего времемни.
            working_hours = True if (user_nowtime.time() >= user.start_time) and \
                                    (user_nowtime.time() <= user.end_time) else False

        # Запустим Тред задачи
        t = th.Thread(target=ask_task, args=(bot, user, task_msg))
        t.start()

    return
