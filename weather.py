# -*- coding: utf-8 -*-
""" Яндекс.Погода

Есть публичный урл со списком городов:
http://weather.yandex.ru/static/cities.xml

Для этих городов можно получить данные о погоде, подставив id города в шаблон:
http://export.yandex.ru/weather-ng/forecasts/<id города>.xml

1. Создает файл базы данных SQLite с следующей структурой данных (если файла 
   базы данных не существует):

    Погода
        id                  INTEGER PRIMARY KEY
        Город               VARCHAR(255)
        Дата                DATE
        Температура днем    INTEGER
        Температура ночью   INTEGER

2. Скачивает и парсит XML со списком городов
3. Выводит список стран из файла и предлагает пользователю выбрать страну
4. Скачивает XML файлы погоды в городах выбранной страны
5. Парсит последовательно каждый из файлов и добавляет данные о погоде в базу
   данных. Если данные для данного города и данного дня есть в базе - обновить
   температуру в существующей записи.


Температура днем и температура ночью берется из 
forecast/day/day_part@day_short/temperature и 
forecast/day/day_part@night_short/temperature соответственно:

<forecast ...>
    <day date="...">
        <day_part typeid="5" type="day_short">
            <temperature>29</temperature> 
            ...
        </day_part>
        <day_part typeid="6" type="night_short">
            <temperature>18</temperature>
            ...
        </day_part>
    </day>
</forecast>

При повторном запуске скрипта:
- используется уже скачанный файл с городами
- используется созданная база данных, новые данные добавляются и обновляются

Важное примечание:

Доступ к данным в XML файлах происходит через простансво имен:
<forecast ... xmlns="http://weather.yandex.ru/forecast ...>

Чтобы работать с простанствами имен удобно пользоваться такими функциями:

# Получим пространство имен из первого тега:
def gen_ns(tag):
    if tag.startswith('{'):
        ns, tag = tag.split('}')
        return ns[1:]
    else:
        return ''

tree = ET.parse(f)
root = tree.getroot()


"""

import os
import sqlite3 as lite
import urllib.request
from xml.etree import ElementTree as ET


class Weather(object):
    def url_request(self, city_id):
        while True:
            try:
                urllib.request.urlretrieve('http://export.yandex.ru/weather-ng/forecasts/{}.xml'.format(city_id),
                                           'd:/python/weather/{}.xml'.format(city_id))
                break
            except:
                continue

    def day_date(self, city_id):
        f = open('d:/python/weather/{}.xml'.format(city_id), 'r')
        forecast = f.read()
        root = ET.fromstring(forecast)
        date = root.find('.//{http://weather.yandex.ru/forecast}day').attrib
        return date['date']

    def night_short(self, city_id):
        f = open('d:/python/weather/{}.xml'.format(city_id), 'r')
        forecast = f.read()
        root = ET.fromstring(forecast)
        temperature = root.find('.//{http://weather.yandex.ru/forecast}day_part[@type="night_short"]/').text
        return temperature

    def day_short(self, city_id):
        f = open('d:/python/weather/{}.xml'.format(city_id), 'r')
        forecast = f.read()
        root = ET.fromstring(forecast)
        temperature = root.find('.//{http://weather.yandex.ru/forecast}day_part[@type="day_short"]/').text
        return temperature


def create_table():
    con = lite.connect('d:/python/weather/weather.db')
    with con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS Погода
                   (Id INTEGER PRIMARY KEY, Город VARCHAR(255), Дата DATE,
                    Температура_днем INTEGER, Температура_ночью INTEGER )""")

    if not os.path.exists('d:/python/weather/cities.db'):
        urllib.request.urlretrieve('http://weather.yandex.ru/static/cities.xml', 'd:/python/weather/cities.xml')
    tree = ET.parse('d:/python/weather/cities.xml')
    root = tree.getroot()
    list_city = []

    for child in root:
        list_city.append(child.attrib['name'])
        print('--->', child.attrib['name'])

    s = True
    weather = Weather()
    while s == True:
        country_id = input('Выбирете страну из списка и введите название или введите quit для выхода из программы:')
        if country_id in list_city:
            for country in root.findall('country'):
                if country.get('name') == country_id:
                    for city in country.iter('city'):
                        weather.url_request(city.get('id'))
                        id_city = [city.get('id'), city.text, weather.day_date(city.get('id')),
                                   weather.day_short(city.get('id')), weather.night_short(city.get('id'))]
                        con = lite.connect('d:\python\weather\weather.db')
                        print(id_city)
                        try:
                            with con:
                                cur = con.cursor()
                                cur.execute("INSERT INTO Погода VALUES (?,?,?,?,? );", id_city)
                                con.commit()
                        except:
                            with con:
                                cur = con.cursor()
                                cur.execute("UPDATE  Погода SET  Дата=? WHERE ID=?",
                                            (weather.day_date(city.get('id')), city.get('id')))
                                cur.execute("UPDATE Погода SET Температура_днем=? WHERE ID=?",
                                            (weather.day_short(city.get('id')), city.get('id')))
                                cur.execute("UPDATE Погода SET Температура_ночью=? WHERE ID=?",
                                            (weather.night_short(city.get('id')), city.get('id')))
                                con.commit()

            with con:
                cur = con.cursor()
                cur.execute("SELECT * FROM Погода")
                rows = cur.fetchall()

            for row in rows:
                print(row)
            s = False

        elif country_id == 'quit':
                break
        else:
            print('Введите страну из списка или quit для выхода из программы! :')


if __name__ == '__main__':
    create_table()







