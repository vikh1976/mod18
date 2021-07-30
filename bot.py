import telebot
from bs4 import BeautifulSoup
import requests
import datetime

from config import *
from extensions import APIException, Converter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help_msg(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n<Имя валюты> ' \
           '<в какую валюту перевести>' \
           '<количество переводимой валюты>' \
           'Для списка доступных валют введите /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text += '\n' + key
    bot.reply_to(message, text)


@bot.message_handler(commands=['bash'])
def show_bash(message: telebot.types.Message):
    base = 'https://bash.im/'
    html = requests.get(base).content
    soup = BeautifulSoup(html, 'lxml')
    quotes = soup.find('section', class_='quotes')
    for _ in quotes.select('article', class_='quote'):
        div = _.find('div', class_='quote__body')
        header = _.find('div', class_='quote__header_date')
        date = (header.getText()).split()
        if date[0] == datetime.date.today().strftime('%d.%m.%Y'):
            bot.send_message(message.chat.id, header.getText() + '\n' + div.getText(separator="\n"))


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        mes = message.text.split()
        if len(mes) != 3:
            raise APIException('Неверное число параметров')
        quote, base, amount = mes
        total_base = (Converter.get_price(quote, base, amount))
    except APIException as e:
        bot.reply_to(message, f'Ошибка ввода:\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base:.2f}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
