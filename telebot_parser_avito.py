import re
import time
import requests
import random
from bs4 import BeautifulSoup
import telebot
import urllib3
from user_agent import generate_user_agent
import datetime

urllib3.disable_warnings()

url = '<>'
bot = telebot.TeleBot('<>')
resultat = []


@bot.message_handler(commands=['start'])
def start(message):
    while True:
        global url
        global resultat

        def get_html(url, params=None):
            """ получение кода страницы """
            headers = {
                "Accept": "*/*",
                "User-Agent": generate_user_agent()}
            html = requests.get(url, headers=headers, params=params)
            return html

        def get_content(html):

            soup = BeautifulSoup(html.text, 'lxml')
            blocks = soup.find_all('div', class_=re.compile('iva-item-content'))

            data = []
            for block in blocks:
                data.append({
                    "Наименование": block.find('h3', class_=re.compile('title-root')).get_text(strip=True),
                    'Цена': block.find('span', class_=re.compile('price-text')).get_text(strip=True).replace('₽', '').replace('\xa0', ''),
                    'Город': block.find('a', class_=re.compile('link-link')).get('href').split('/')[1],
                    'Район': block.find('div', class_=re.compile('geo-root')).get_text(strip=True),
                    'Ссылка': url + block.find('a', class_=re.compile('link-link')).get('href'),
                })
            return data

        n = get_html(url)
        res = get_content(n)
        now = datetime.datetime.now()
        print(now, 'программа выполнилась')
        for i in res:
            s = str(i['Ссылка']).split('/')

            l = str(s[2] + '/' + s[5] + '/' + s[6] + '/' + s[7])
            if l not in resultat:
                resultat.append(l)
                bot.send_message(message.chat.id, f"Новое объявление - {l}\nГород {i['Район']}\nЦена {i['Цена']}")

        time.sleep(random.randint(61, 232))


bot.infinity_polling(timeout=10, long_polling_timeout=5)
