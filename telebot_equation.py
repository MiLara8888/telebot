import telebot
from telebot import types
from telebot import util
import math

bot = telebot.TeleBot('')


@bot.message_handler(commands=['start'])
def start(message):
    kb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)  # клавиатура
    btn1 = types.InlineKeyboardButton(text='Решить квадратное уравнение')
    kb.add(btn1)
    bot.send_message(message.chat.id, 'Привет что тебя интересует?', reply_markup=kb)


@bot.message_handler(func=lambda x: x.text == 'Решить квадратное уравнение')
def func(message):
    n = bot.reply_to(message, 'Введите коэффициенты ax^2+bx+c  в виде: a b c, например: -1 2 3')
    bot.register_next_step_handler(n, hello)


def hello(message):
    try:
        n = message.text.split()
        a, b, c = float(n[0]), float(n[1]), float(n[2])
        bot.send_message(message.chat.id, 'Коэффициенты введены верно, начинаю решать уравнение')
        discr = b ** 2 - 4 * a * c
        bot.send_message(message.chat.id, f'Дискриминант равен {discr}')
        if discr > 0:
            bot.send_message(message.chat.id,
                             f'У уравнения 2 корня\nПервый корень {(-b + math.sqrt(discr)) / (2 * a)}\nВторой корень {(-b - math.sqrt(discr)) / (2 * a)}')
        elif discr == 0:
            bot.send_message(message.chat.id,
                             f'У уравнения 1 корень: {-b / (2 * a)}')
        else:
            bot.send_message(message.chat.id,'У уравнения нет корней')
    except:
        bot.send_message(message.chat.id,'Коэффициенты введены неверно')


bot.polling()
