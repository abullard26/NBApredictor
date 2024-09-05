from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO


advancedTeamStats = {}
gameTeamStats = {}
totalTeamStats = {}

years = range(2010, 2025)
file_path = '/Users/alexbullard/PycharmProjects/NBAGamePredictor/TeamStats/NBA_{}.html'
for year in years:
    with open(file_path.format(year)) as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        soup.find('tr', class_='over_header').decompose()
        advancedStatsTable = soup.find(id='advanced-team')
        gameStatsTable = soup.find(id='per_game-team')

        advancedTeamStats[year] = pd.read_html(StringIO(str(advancedStatsTable))).pop().drop(columns=['Team'])
        gameTeamStats[year] = pd.read_html(StringIO(str(gameStatsTable))).pop()

        totalTeam = pd.concat([gameTeamStats[year], advancedTeamStats[year]], axis=1).drop(columns = ['Rk', 'Arena', 'Attend.', 'Attend./G', 'NRtg', 'Age', 'G', 'MP', 'PW', 'PL', 'MOV', 'Unnamed: 17', 'Unnamed: 22', 'Unnamed: 27'])

        totalTeamStats[year] = totalTeam

        totalTeamStats[year].to_csv('TotalStats/NBA_Stats_{}.csv'.format(year))







