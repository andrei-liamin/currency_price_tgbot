import telebot

from extensions import APIException, Exchange
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

# start
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    greetings = """Чтобы получить стоимость нужной валюты отправь мне сообщение в таком формате (через пробел):
A B N
где A - валюта, стоимость которой хочешь узнать
B - валюта, в которой нужно узнать стоимость
N - количество первой валюты A

Например, чтобы узнать сколько стоит 1 доллар в рублях отправь:
USD RUB 1
    
Чтобы узнать доступные для конвертации валюты жми /values"""

    bot.send_message(message.chat.id, greetings)

# values
@bot.message_handler(commands=['values'])
def handle_values(message):
    bot.send_message(message.chat.id, Exchange.get_values())

# default handler
@bot.message_handler(content_types=["text"])
def handle_get_price(message):
    values = message.text.split()
    try:
        # error: too many counts
        if len(values) != 3:
            raise APIException("Неверное количество параметров")
        base, quote, amount = values
        result = Exchange.get_price(base, quote, amount)
    except APIException as e:
        bot.send_message(message.chat.id, f"Неправильно введены данные:\n{e}")
        handle_start_help(message)
    except Exception as e:
        bot.send_message(message.chat.id, f"Неизвестная ошибка:\n{e}\n\nПопробуйте еще раз чуть позже")
    else:
        bot.send_message(message.chat.id, result)

bot.polling(none_stop=True)
