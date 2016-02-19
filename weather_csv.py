# -*- coding: utf-8 -*-

import csv
import sqlite3 as lite

con = lite.connect('d:\python\weather\weather.db')
with con:
    cur = con.cursor()
    cur.execute("SELECT * FROM Погода")
with open("d:\python\weather\weather.db"):
    print '{},{},{},{}'.format(row['Город'], row['ДАТА'], row['Температура_днем'], row['Температура_ночью'])