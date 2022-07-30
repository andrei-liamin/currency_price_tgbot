import requests
import json

class APIException(Exception):
    pass

class Exchange():
    path = 'https://www.cbr-xml-daily.ru/daily_json.js'
    
    @staticmethod
    def __get_data__():
        data_json = requests.get(Exchange.path).content
        data_dict = json.loads(data_json)["Valute"]
        result_data = dict(filter(lambda curr: curr[0] == "USD" or curr[0] == "EUR", data_dict.items()))
        result_data["RUB"] = {"Value": 1, "Name": "Рубль"}
        return result_data

    @staticmethod
    def get_price(base, quote, amount):
        data = Exchange.__get_data__()
        try:
            base_value = float(data[base]["Value"])
        except KeyError:
            raise APIException(f"Валюта {base} не найдена")
        if base == quote:
            return f"Это было непросто, но наш суперкомпьютер вычислил, что {amount} {base} = {amount} {quote}. Не благодарите! :)"
        try:
            quote_value = float(data[quote]["Value"])
        except KeyError:
            raise APIException(f"Валюта {quote} не найдена")
        try:
            amount = int(amount)
        except ValueError:
            raise APIException(f"Не удалось обработать количество валюты: {amount}")
        result_value = round((base_value / quote_value * amount), 4)

        return f"{amount} {base} = {result_value} {quote}"
    
    @staticmethod
    def get_values():
        data = Exchange.__get_data__()
        result = "Доступные для просмотра валюты:\n\n"
        for key, param in data.items():
            result += f"{key} - {param['Name']}\n"
        return result
