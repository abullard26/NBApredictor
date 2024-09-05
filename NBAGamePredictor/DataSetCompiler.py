import pandas as pd
import numpy as np

years = range(2010, 2024)

Data = []
hdrs = []
for year in years:
    totalStats = pd.read_csv('TotalStats/NBA_Stats_{}.csv'.format(year))
    hdrs = totalStats.columns.tolist()[2:]
    print(hdrs)
    with open('BoxScores/box_scores_{}.txt'.format(year), 'r') as f:

        lines = f.readlines()
        for line in lines:
            line = line.strip('\n')
            game = line.split(',')
            game[1] = game[1].strip(' ')
            game[2] = int(game[2])

            game[0] = game[0].split(' ')
            game[1] = game[1].split(' ')

            i = 0
            homeTeamIndex = 0
            awayTeamIndex = 0
            for team in totalStats['Team']:
                if team.find(game[0][-1]) != -1:
                    homeTeamIndex = i
                if team.find(game[1][-1]) != -1:
                    awayTeamIndex = i
                i+=1
            homeTeamStats = totalStats.iloc[homeTeamIndex].to_numpy()[2:]
            awayTeamStats = totalStats.iloc[awayTeamIndex].to_numpy()[2:]
            diffStats = homeTeamStats - awayTeamStats
            pointDiff = game[2]

            dataPoint = np.concatenate((diffStats, [pointDiff]))

            Data.append(dataPoint)



d = pd.DataFrame(Data, columns=hdrs+['PointDiff'])
d.to_csv('CompiledHeadToHeadStatsDifference.csv', index=False)



