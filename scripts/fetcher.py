import time                             # | Эти четыре импорта нужны для взятия информации о курсе
from datetime import datetime           # | доллара с сайта ЦБ
from xml.etree import ElementTree       # |
import requests                         # |
import gspread                          # || Эти импорты здесь для забора данных из гуглдока
import pandas                           # || 

def usd_finder(xml_tree):
    for currency in xml_tree:
        code = currency.find('CharCode').text
        value = currency.find('Value').text
        if code == 'USD':
            value = value.replace(',', '.')
            return float(value)


def get_sheet():
    today = datetime.now().timetuple()

    # подгоняем дату под формат, который воспримет сайт ЦБ

    today = [str(x) for x in today]
    if len(today[1]) == 1:
        today[1] = f'0{today[1]}'

    # Открываем гуглдок

    sa = gspread.service_account(filename='./credentials/token.json')
    sh = sa.open('test_case')
    wsh = sh.worksheet('data')

    # Переводим все данные из гуглдока в таблицу pandas

    data = pandas.DataFrame(wsh.get_all_records())
    currency_data = ElementTree.fromstring(requests.get(f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={today[2]}/{today[1]}/{today[0]}').content)
    usd_data = usd_finder(currency_data)

    # Считаем рублевые значения

    rub_data = []
    for i, row in data.iterrows():
        result = round(row['стоимость,$'] * usd_data, 2)
        rub_data.append(result)

    data['стоимость в руб.'] = rub_data

    return data

