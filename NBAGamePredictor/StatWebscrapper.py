import certifi
import ssl

from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup

years = range(2010, 2025)
url_template = 'https://www.basketball-reference.com/leagues/NBA_{}.html#all_per_game_team-opponent'

for year in years:
    url = url_template.format(year)
    page = requests.get(url, timeout=10)


    with open('TeamStats/NBA_{}.html'.format(year), 'w+') as f:
        f.write(page.text)
