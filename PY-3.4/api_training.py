import requests
import osa
import os


URL = 'http://fx.currencysystem.com/webservices/CurrencyServer4.asmx?WSDL'
URL_TEMP = 'http://www.webservicex.net/ConvertTemperature.asmx?WSDL'
URL_DIST = 'http://www.webservicex.net/length.asmx?WSDL'

# конвертирует из миль в километры, может быть доработана для конвертации из другой меры длины
def convert_to_km(distances_dict):
    client = osa.client.Client(URL_DIST)
    for cities, distances in distances_dict.items():
        amount_value = ''.join(distances['amount'].split(','))
        measure = distances['measure']
        if measure == 'mi':
            response =  round(client.service.ChangeLengthUnit(LengthValue=amount_value,
                                                          fromLengthUnit='Miles', toLengthUnit='Kilometers'), 2)
        print('Длина перелета {0}: {1} км' .format(cities, response))


# конвертирует из валюты взятой из файла в рубли
def convert_to_ruble(cities_dict):
    client = osa.client.Client(URL)
    for cities, currency in cities_dict.items():
        amount_value = currency['amount']
        measure = currency['measure']
        response =  round(client.service.ConvertToNum(fromCurrency=measure,
                    toCurrency='RUB', amount=amount_value, rounding=True), 1)
        print('При перелете {0} мы потратим {1} рублей' .format(cities, response))

# конвертирует темперуру в Цельсий и находит среднее значение
def temperature_c(temps):
    client = osa.client.Client(URL_TEMP)
    temps_in_c = []
    for temp, unit in temps:
        if unit == 'F':
            response = client.service.ConvertTemp(Temperature=temp,
                    FromUnit='degreeFahrenheit', ToUnit='degreeCelsius')
            temps_in_c.append(response)
    avg_week = round(sum(temps_in_c) / len(temps_in_c), 1)
    print('Средняя температура за неделю: ', avg_week)

# создает список температур для последующей обработки
def temperature_list(temps_file):
    with open(temps_file, 'r',encoding='utf_8') as f:
        temps_list = []
        for line in f:
            parameter_data = tuple(line.strip().split(' '))
            temps_list.append(parameter_data)
    return temps_list

# создает словарь из файла перелетов или валют
def currencies_convert(currency_file):
    with open(currency_file, 'r',encoding='utf_8') as f:
        line_data = []
        cities_dictionary = dict()
        for line in f:
            line_data = line.strip().split(' ')
            cities_dictionary[line_data[0]] = {'amount': line_data[1], 'measure': line_data[2]}
    return cities_dictionary

# создает путь к файлу
def make_file_path(file_name):
    data_dir = os.path.join(os.getcwd(), '3.4-currencies')
    file_path = os.path.join(data_dir, file_name)
    return file_path


temps__to_convert = temperature_list(make_file_path('temps.txt'))
temperature_c(temps__to_convert)
print('-' * 20)

currencies = currencies_convert(make_file_path('currencies.txt'))
convert_to_ruble(currencies)
print('-' * 20)

miles = currencies_convert(make_file_path('travel.txt'))
convert_to_km(miles)

