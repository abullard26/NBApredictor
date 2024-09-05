import time

import requests
import certifi
import ssl
import pandas as pd
from io import StringIO

import urllib3.exceptions
from bs4 import BeautifulSoup


def formatTable(df):
    homeTeam = df[0][1]
    homePoints = int(df[1][1])
    awayTeam = df[0][0]
    awayPoints = int(df[1][0])
    pointDifferential = homePoints-awayPoints

    return str(homeTeam) + ", " + str(awayTeam) + ", " + str(pointDifferential) + '\n'


url_template = 'https://www.basketball-reference.com/boxscores/?month={}&day={}&year={}'
years = range(2021, 2025)
months = [10, 11, 12, 1, 2, 3, 4, 5, 6]
days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

for year in years:
    with open('BoxScores/box_scores_{}.txt'.format(year), 'w+') as f:
        for month in months:
            for day in range(1,days[month]+1):
                try:
                    if month > 9:
                        url = url_template.format(month, day, year-1)
                    else:
                        url = url_template.format(month, day, year)

                    page = requests.get(url, timeout=50)
                    html = page.text

                    soup = BeautifulSoup(html, 'html.parser')
                    results = soup.find_all('table', class_='teams')

                    for result in results:
                        data = pd.read_html(StringIO(str(result))).pop()
                        f.write(formatTable(data))

                    if month > 9:
                        print(month, day, year - 1)
                    else:
                        print(month, day, year)
                except:
                    print("Error Due to Timeout")
                    with open('BoxScores/missed_dates.txt', 'a') as f:
                        f.write(str(month)+', '+str(day)+', ' + str(year))

                time.sleep(5)

'''
url = url_template.format(11, 15, 2015)
page = requests.get(url)
html = page.text

soup = BeautifulSoup(html, 'html.parser')
results = soup.find_all('table', class_='teams')

for result in results:
    data = pd.read_html(StringIO(str(result))).pop()
    print(data)
'''
