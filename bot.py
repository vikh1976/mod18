import telebot

from config import *
from extensions import APIException, Converter

bot = telebot.TeleBot(TOKEN)


# Вывод инструкции по использованию бота
@bot.message_handler(commands=['start', 'help'])
def help_msg(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n<Имя валюты> ' \
           '<в какую валюту перевести>' \
           '<количество переводимой валюты>' \
           'Для списка доступных валют введите /values'
    bot.reply_to(message, text)


# Вывод списка допустимых валют
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text += '\n' + key
    bot.reply_to(message, text)


# Основная функция обработки ввода пользователя
@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        # Если введено менее или более трех параметров - сообщение об ошибке
        mes = message.text.split()
        if len(mes) != 3:
            raise APIException('Неверное число параметров')
        quote, base, amount = mes
        # Получаем цену выбранной валюты
        total_base = (Converter.get_price(quote, base, amount))
    except APIException as e:
        # В случае ошибок ввода выводим соотв. сообщение
        bot.reply_to(message, f'Ошибка ввода:\n{e}')
    except Exception as e:
        # При любых других ошибках показываем эту ошибку
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        # Если все в порядке - выводим результат работы
        text = f'Цена {amount} {quote} в {base} - {total_base:.2f}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
