# Yandex_weather
Python 3.x 
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

Порядок запуска скриптов. 

Все скрипты звпускаются с командной строки.

1. weather.py - собственно скрипт забирает фаел с yandex.ru с названием стран парсит его и предлдогает выбрать страну, после выборы страны выбирает города этой страны и соответсвенно дневную и ночную температуру создает таблицу в базе данных 
                sqlite.db и складывает информацию о городах и погоде в базу!
                 
    export_weather.py - скрипт с возможностью допю опций берет фаел базы данных конвертирует его в csv-формат и если выбрана оп 
                     
                        --csv выводит все содержимое файла
                        
                        --city выводит информацию о погоде конкретного города.

