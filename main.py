import requests
import datetime
import csv
import pandas as pd
import keyboard

def changing_month(month, f):
    # Изменение строки для месяца
    if month < 10:
        month = "0" + str(f)
    return month


def changing_day(day, f):
    # Изменение строки для дней
    if day < 10:
        day = "0" + str(f)
    return day

def date1(s):
    return s[:10]


def date_month(s):
    return s[5:7]


def date_year(s):
    return s[:4]

def record(path, t, u):
    with open(path, "a", newline='') as scoreFile:
        file_writer = csv.writer(scoreFile, delimiter=',')
        for d, r in zip(t, u):
            file_writer.writerow([d, r])
        scoreFile.close()

def recording_data():
    t = []
    u = []
    t.append('Date')
    u.append('USD')
    # Дата с которой будем записать данные
    d = datetime.date(2000, 1, 1)
    df = datetime.datetime.now() + datetime.timedelta(days=1)
    # цикл для изменения дат
    while d.year != df.year or d.month != df.month or d.day != df.day:
        month = d.month
        day = d.day
        month = changing_month(month, d.month)
        day = changing_day(day, d.day)
        # url сайта с которого загружаем данные
        url = ('https://www.cbr-xml-daily.ru/archive/' + str(d.year) + '/' + str(month)
               + '/' + str(day) + '/daily_json.js')
        response = requests.get(url).json()
        # Проверка на ошибку, если по определённой дате нет данных
        if 'error' in response:
            d += datetime.timedelta(days=1)
        else:
            # Вытаскиваем данные из response
            date = date1(response['Date'])
            t.append(date)
            usd = response['Valute']['USD']['Value']
            u.append(usd)
            d += datetime.timedelta(days=1)
    record("dataset.csv", t, u)

def data_separation_x_y():
        df = pd.read_csv('dataset.csv', sep=',')
        x = df['Date']
        y = df['USD']
        x.to_csv("X.csv", sep='\t', encoding='utf-8')
        y.to_csv("Y.csv", sep='\t', encoding='utf-8')