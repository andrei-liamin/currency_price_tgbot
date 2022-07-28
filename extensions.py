import requests
import json

class APIException(Exception):
    pass

class Exchange():
    def __init__(self):
        self.path = 'https://www.cbr-xml-daily.ru/daily_json.js'
    
    def __get_data__(self):
        data_json = requests.get(self.path).content
        data_dict = json.loads(data_json)["Valute"]
        result_data = dict(filter(lambda curr: curr[0] == "USD" or curr[0] == "EUR", data_dict.items()))
        result_data["RUB"] = {"Value": 1}
        return result_data

    def getPrice(self, base, quote, amount):
        data = self.__get_data__()
        base_value = float(data[base]["Value"])
        quote_value = float(data[quote]["Value"])

        return round((base_value / quote_value * amount), 4)
    
    def getValues(self):
        data = self.__get_data__()
        result = "Доступные для просмотра валюты:\n\n"
        for curr in data.keys():
            result += f"{curr}\n"
        return result
