import telebot
from telebot import types
from random import shuffle
from telebot import util

bot = telebot.TeleBot('<>')


@bot.message_handler(commands=['start'])
def start(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    b1 = types.KeyboardButton(text='Отправить геолокацию', request_location=True)
    kb.add(b1)
    bot.send_message(message.chat.id, 'Жду твоей геолокации', reply_markup=kb)


@bot.message_handler(content_types=['location'])
def phone(message):
    bot.send_message(message.chat.id, f'Геолокация получена\nШирина: {message.location.latitude}\nДолгота: {message.location.longitude}')


bot.polling()
