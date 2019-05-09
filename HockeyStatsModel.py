import json
import requests
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import time
from operator import itemgetter
from Skater import Skater

NHL_TEAM_5v5_GOALS_DICT = {}

# Lists to collect the data together from different sources.
skaterList = []
nameList = []
gamesPlayedList = []
teamList = []
teamColourList = []
toiAllList = []

# THESE STATS SHOULD LOOK AT ALL SITUATIONS, NOT JUST 5V5
#hitsList = []
#takeawaysList = []
#blocksList = []
#faceoffWinsList = []

offenceRatingList = []
evOffenceRatingList = []
ppOffenceRatingList = []
pkOffenceRatingList = []

evShotsRatingList = []
ppShotsRatingList = []
pkShotsRatingList = []

evPointsRatingList = []
ppPointsRatingList = []
pkPointsRatingList = []

defenceRatingList = []

# Open and Load json data
def loadAllTeamData():
    with open('Team Season Stats 2018-19.json') as f:
        allTeamData = json.load(f)
        return allTeamData
def load5v5TeamData():
    with open('5v5 Team Season Stats 2018-19.json') as f:
        team5v5Data = json.load(f)
        return team5v5Data
def loadAllIndividualData():
    with open('Total Individual Skater Stats 2018-19.json') as f:
        allSkaterData = json.load(f)
        return allSkaterData
def load5v5IndividualData():
    with open('5v5 Individual Skater Stats 2018-19.json') as f:
        i5v5Data = json.load(f)
        return i5v5Data
def loadPPIndividualData():
    with open('PP Individual Skater Stats 2018-19.json') as f:
        iPPData = json.load(f)
        return iPPData
def loadPKIndividualData():
    with open('PK Individual Skater Stats 2018-19.json') as f:
        iPKData = json.load(f)
        return iPKData

# Iterates through two JSON Object lists and merges the matching records
# def mergePlayerData(data1,data2):
#     for player1 in data1:
#         for player2 in data2:
#             if (player1['playerId'] == player2['playerId']):
#                 player1.update(player2)
#     return data1

# Process the data into a usable state

def processData():
    NHL_TEAM_5v5_GOALS_DICT = {}

    for team in team5v5Data:
        NHL_TEAM_5v5_GOALS_DICT[team['Abbr']] = team['GF']

    for player in allSkaterData:
        s = Skater(player['Player'], player['Team'][-3:], player['Position'], player['GP'], player['TOI'], player['SH%'])  # [-3:] Ensures that players with multiple teams only return the most recent team
        skaterList.append(s)
        
    for player in player5v5Data:
        for s in skaterList:
            if (player['Player'] == s.name):
        
                s.toi5v5 = player['TOI']
                s.goals5v5 = player['Goals']
                s.fAssists5v5 = player['First Assists']
                s.sAssists5v5 = player['Second Assists']
                s.iPointPercentage = player['IPP']

                if (player['Total Points'] > 0):
                    ptsPerGP =  player['Total Points'] / s.games
                    teamGoalsPerGame =  NHL_TEAM_5v5_GOALS_DICT[s.team] / 82
                    s.iTeamPointPercentage = ptsPerGP / teamGoalsPerGame
                    #print (s.team + ", " + s.name + ": " + "{0:.3f}".format(ptsPerGP) + " / " + "{0:.3f}".format(teamGoalsPerGame) + " = " + "{0:.3f}".format(s.iTeamPointPercentage) + " : " + "{0:.3f}".format(s.iTeamPointPercentage * 0.05))
                    #print ("  -  " + "{0:.2f}".format(s.toiALL/s.games) + "  -  " + "{0:.3f}".format(((s.toiALL/s.games)*0.05)))
                else:
                    s.iTeamPointPercentage = 0

                s.evixG = player['ixG']
                s.eviCF = player['iCF']
                s.eviFF = player['iFF']
                s.eviSF = player['Shots']
                s.eviSCF = player['iSCF']
                s.eviHDCF = player['iHDCF']

                # s.teamGoals5v5
                # s.ippTeamGoals5v5

                # TRACK THESE IN ALL SITUATIONS
                # takeaways = player['Takeaways']
                # hits = player['Hits']
                # hitsAgainst = player['Hits Taken']
                # shotsBlocked = player['Shots Blocked']
                # faceoffWins = player['Faceoffs Won']
                # faceoffLosses = player['Faceoffs Lost']

                # minorPenalties = player['Minor']
                # majorPenalties = player['Major']
                # misconductPenalties = player['Misconduct']

    for player in iPPData:
        for s in skaterList:
            if (player['Player'] == s.name):
                s.toiPP = player['TOI']
                s.ppGoals = player['Goals']
                s.ppAssists = player['Total Assists']
                s.badPenalties += player['Total Penalties']

                s.ppixG = player['ixG']
                s.ppiCF = player['iCF']
                s.ppiFF = player['iFF']
                s.ppiSF = player['Shots']
                s.ppiSCF = player['iSCF']
                s.ppiHDCF = player['iHDCF']

    for player in iPKData:
        for s in skaterList:
            if (player['Player'] == s.name):
                s.toiPK = player['TOI']
                s.pkGoals = player['Goals']
                s.pkAssists = player['Total Assists']
                s.badPenalties += player['Total Penalties']

                s.pkixG = player['ixG']
                s.pkiCF = player['iCF']
                s.pkiFF = player['iFF']
                s.pkiSF = player['Shots']
                s.pkiSCF = player['iSCF']
                s.pkiHDCF = player['iHDCF']

    for s in skaterList:
        offenceRatingList.append(s.calcOffensiveRating())

    skaterList.sort(key=lambda x: x.offensiveRating, reverse=True)

    count = 0
    limit = 30
    for s in skaterList:
        if (limit > count and s.toiALL > 1200):
            nameList.append(s.name)
            toiAllList.append(s.toiALL)
            evOffenceRatingList.append(s.evOffensiveRating)
            ppOffenceRatingList.append(s.ppOffensiveRating)
            pkOffenceRatingList.append(s.pkOffensiveRating)

            evShotsRatingList.append(s.evShotsRating)
            ppShotsRatingList.append(s.ppShotsRating)
            pkShotsRatingList.append(s.pkShotsRating)

            evPointsRatingList.append(s.evPointsRating)
            ppPointsRatingList.append(s.ppPointsRating)
            pkPointsRatingList.append(s.pkPointsRating)
            count += 1

            print(s)

    print (str(len(nameList)) + ' results\n')


# Configure the settings for the chart and sent the data to Plot.ly
def plotChart():
    print ('Plotting...\n')

    # Even Strength Traces
    tracePointOffence = go.Bar(
        x=nameList,
        y=evPointsRatingList,
        name='5v5 Point Scoring Rating',
        marker=dict(
            color='rgb(22, 50, 116)'
        )
    )
    traceShotOffence = go.Bar(
        x=nameList,
        y=evShotsRatingList,
        name='5v5 Shot Contribution Rating',
        marker=dict(
            color='rgb(22, 80, 156)'
        )
    )

    # Powerplay Traces
    tracePPPointOffence = go.Bar(
        x=nameList,
        y=ppPointsRatingList,
        name='PP Point Scoring Rating',
        marker=dict(
            color='rgb(20, 136, 45)'
        )
    )
    tracePPShotOffence = go.Bar(
        x=nameList,
        y=ppShotsRatingList,
        name='PP Shot Contribution Rating',
        marker=dict(
            color='rgb(20, 160, 50)'
        )
    )

    # Penalty Kill Traces
    tracePKPointOffence = go.Bar(
        x=nameList,
        y=pkPointsRatingList,
        name='PK Point Scoring Rating',
        marker=dict(
            color='rgb(216, 21, 21)'
        )
    )
    tracePKShotOffence = go.Bar(
        x=nameList,
        y=pkShotsRatingList,
        name='PK Shot Contribution Rating',
        marker=dict(
            color='rgb(255, 32, 52)'
        )
    )
    layout = go.Layout(
        barmode='stack',
        title=go.layout.Title(
            text='Offensive Efficiency',
            x=0
        ),
        xaxis = dict(tickangle=-30)
    )
    data = [tracePointOffence, traceShotOffence, tracePPPointOffence, tracePPShotOffence, tracePKPointOffence, tracePKShotOffence]
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, file='player-model')

#https://stackoverflow.com/questions/44309507/stacked-bar-plot-using-matplotlib
# def stacked_bar(data, series_labels, category_labels=None,
#                 show_values=False, value_format="{}", y_label=None,
#                 grid=True, reverse=False):
#     """Plots a stacked bar chart with the data and labels provided.
#
#     Keyword arguments:
#     data            -- 2-dimensional numpy array or nested list
#                        containing data for each series in rows
#     series_labels   -- list of series labels (these appear in
#                        the legend)
#     category_labels -- list of category labels (these appear
#                        on the x-axis)
#     show_values     -- If True then numeric value labels will
#                        be shown on each bar
#     value_format    -- Format string for numeric value labels
#                        (default is "{}")
#     y_label         -- Label for y-axis (str)
#     grid            -- If True display grid
#     reverse         -- If True reverse the order that the
#                        series are displayed (left-to-right
#                        or right-to-left)
#     """
#
#     ny = len(data[0])
#     ind = list(range(ny))
#
#     axes = []
#     cum_size = np.zeros(ny)
#
#     data = np.array(data)
#
#     if reverse:
#         data = np.flip(data, axis=1)
#         category_labels = reversed(category_labels)
#
#     for i, row_data in enumerate(data):
#         axes.append(plt.bar(ind, row_data, bottom=cum_size,
#                             label=series_labels[i]))
#         cum_size += row_data
#
#     if category_labels:
#         plt.xticks(ind, category_labels)
#
#     if y_label:
#         plt.ylabel(y_label)
#
#     plt.legend()
#
#     if grid:
#         plt.grid()
#
#     if show_values:
#         for axis in axes:
#             for bar in axis:
#                 w, h = bar.get_width(), bar.get_height()
#                 plt.text(bar.get_x() + w / 2, bar.get_y() + h / 2,
#                          value_format.format(h), ha="center",
#                          va="center")

#def matPlotChart():

def endTimer():
    print ('Finishing...\n')
    end = time.time()
    totalTime = "{0:.4f}".format(end - start)
    print ('Time elapsed: ' + totalTime + 's')

print ('Starting...\n')
start = time.time()

# Convert JSON data to usable object lists
allTeamData = loadAllTeamData()
team5v5Data = load5v5TeamData()
allSkaterData = loadAllIndividualData()
i5v5Data = load5v5IndividualData()
iPPData = loadPPIndividualData()
iPKData = loadPKIndividualData()

# Merge Datasets (this section may still end up being used)
# playerData = mergePlayerData(summaryData, assistData)
# playerData = mergePlayerData(playerData, faceoffData)
# playerData = mergePlayerData(playerData, penaltyData)
# playerData = mergePlayerData(playerData, miscData)

teamAllData = allTeamData
team5v5Data = team5v5Data
playerAllData = allSkaterData
player5v5Data = i5v5Data
playerPPData = iPPData
playerPKData = iPKData


# Feed and manipulate the data for use
print ('Processing...\n')
processData()

# Plot data on Plot.ly
plotChart()

# Plot data with matplotlib
#matPlotChart()


endTimer()