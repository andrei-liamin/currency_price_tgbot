# Бот возвращает цену на определённое количество валюты (евро, доллар или рубль).
# При написании бота необходимо использовать библиотеку pytelegrambotapi.
# Человек должен отправить сообщение боту в виде <имя валюты цену которой он хочет узнать> <имя валюты в которой надо узнать цену первой валюты> <количество первой валюты>.
# При вводе команды /start или /help пользователю выводятся инструкции по применению бота.
# При вводе команды /values должна выводиться информация о всех доступных валютах в читаемом виде.
# Для взятия курса валют необходимо использовать любое удобное API и отправлять к нему запросы с помощью библиотеки Requests.
# Для парсинга полученных ответов использовать библиотеку JSON.
# При ошибке пользователя (например, введена неправильная или несуществующая валюта или неправильно введено число) вызывать собственно написанное исключение APIException с текстом пояснения ошибки.
# Текст любой ошибки с указанием типа ошибки должен отправляться пользователю в сообщения.
# Для отправки запросов к API описать класс со статическим методом get_price(), который принимает три аргумента: имя валюты, цену на которую надо узнать, — base, имя валюты, цену в которой надо узнать, — quote, количество переводимой валюты — amount и возвращает нужную сумму в валюте.
# Токен telegramm-бота хранить в специальном конфиге (можно использовать .py файл).
# Все классы спрятать в файле extensions.py.

from tokenize import Number
import requests
import json

import telebot

TOKEN = "5523246168:AAGEEOiCu4CV-itd7i8mEyVWm0CZjGQ9geY"

bot = telebot.TeleBot(TOKEN)

# get currency exchange values

class Exchange():
    def __init__(self):
        self.path = 'https://www.cbr-xml-daily.ru/daily_json.js'

    def getPrice(self, base, quote, amount):
        data_json = requests.get(self.path).content
        data_dict = json.loads(data_json)["Valute"]
        data_dict["RUB"] = {"Value": 1}
        base_value = float(data_dict[base]["Value"])
        quote_value = float(data_dict[quote]["Value"])

        return round((base_value / quote_value * amount), 4)

test = Exchange()
print(test.getPrice("USD", "EUR", 3))
