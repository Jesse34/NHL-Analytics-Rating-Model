import json
import requests
import plotly.plotly as py
import plotly.graph_objs as go
import time
from operator import itemgetter
from Skater import Skater

# Lists to collect the data together from different sources.
skaterList = []
nameList = []
gamesPlayedList = []
teamList = []
teamColourList = []
toiAllList = []

evGoalsList = [] # Not actually even strength, 5v5.
#ppGoalsList = []
#shGoalsList = []

fAssistsList = []
sAssistsList = []
#ppAssistsList = []
#pkAssistsList = []

# THESE STATS SHOULD LOOK AT ALL SITUATIONS, NOT JUST 5V5
#hitsList = []
#takeawaysList = []
#blocksList = []
#faceoffWinsList = []

offenceRatingList = []
evOffenceRatingList = []
ppOffenceRatingList = []
pkOffenceRatingList = []

defenceRatingList = []

# Open and Load json data
def loadAllIndividualData():
    with open('Total Individual Skater Stats 2018-19.json') as f:
        allData = json.load(f)
        return allData
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
def mergePlayerData(data1,data2):
    for player1 in data1:
        for player2 in data2:
            if (player1['playerId'] == player2['playerId']):
                player1.update(player2)
    return data1

# Process the data into a usable state
def processData():
    for player in player5v5Data:
        s = Skater(player['Player'], player['Team'][-3:], player['Position'], player['GP']) # [-3:] Ensures that players with multiple teams only return the most recent team

        s.toi5v5 = player['TOI']
        s.goals5v5 = player['Goals']
        s.fAssists5v5 = player['First Assists']
        s.sAssists5v5 = player['Second Assists']
        s.shots5v5 = player['Shots']
        s.iPointPercentage5v5 = player['IPP']

        s.ixG = player['ixG']
        s.iCF = player['iCF']
        s.iFF = player['iFF']
        s.iSCF = player['iSCF']
        s.iHDCF = player['iHDCF']

        skaterList.append(s)
        #goalsPK = player['shGoals']
        #assistsPK = player['shAssists']

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

        # nameList.append(s.name)
        # gamesPlayedList.append(s.games)
        # teamList.append(s.team)
        #
        # evGoalsList.append(s.goals5v5)
        #
        # fAssistsList.append(s.fAssists5v5)
        # sAssistsList.append(s.sAssists5v5)

    for player in iPPData:
        for s in skaterList:
            if (player['Player'] == s.name):
                s.toiPP = player['TOI']
                s.ppGoals = player['Goals']
                s.ppAssists = player['Total Assists']
                s.badPenalties += player['Total Penalties']

    for player in iPKData:
        for s in skaterList:
            if (player['Player'] == s.name):
                s.toiPK = player['TOI']
                s.pkGoals = player['Goals']
                s.pkAssists = player['Total Assists']
                s.badPenalties += player['Total Penalties']

    for player in allData:
        for s in skaterList:
            if (player['Player'] == s.name):
                s.toiALL = player['TOI']
                offenceRatingList.append(s.calcOffensiveRating())

    for s in skaterList:
        if (s.toiALL > 1000):
            nameList.append(s.name)
            toiAllList.append(s.toiALL)
            evOffenceRatingList.append(s.evOffensiveRating)
            ppOffenceRatingList.append(s.ppOffensiveRating)
            pkOffenceRatingList.append(s.pkOffensiveRating)
            print(s)

    skaterList.sort(key=lambda x: x.offensiveRating, reverse=True)
    # for x in skaterList:
    #     print(x)

# Configure the settings for the chart and sent the data to Plot.ly
def plotChart():
    print ('Plotting...')

    # Traces
    traceOffence = go.Bar(
        x=nameList,
        y=evOffenceRatingList,
        name='5v5 Offensive Rating',
        marker=dict(
            color='rgb(22, 50, 116)'
        )
    )
    traceDefence = go.Bar(
        x=nameList,
        y=ppOffenceRatingList,
        name='PP Offensive Rating',
        marker=dict(
            color='rgb(10, 136, 38)'
        )
    )
    traceGrit = go.Bar(
        x=nameList,
        y=pkOffenceRatingList,
        name='PK Offensive Rating',
        marker=dict(
            color='rgb(230,16,46)'
        )
    )

    layout = go.Layout(
        barmode='stack',
        title=go.layout.Title(
            text='N.U.T.S (Numbers Used to Simplify)',
            x=0
        ),
        xaxis = dict(tickangle=-40)
    )
    data = [traceOffence, traceDefence, traceGrit]
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, file='player-model')

def endTimer():
    print ('Finishing...')
    end = time.time()
    totalTime = "{0:.4f}".format(end - start)
    print ('\nTime elapsed: ' + totalTime + 's')

print ('Starting...')
start = time.time()

# Convert JSON data to usable object lists
allData = loadAllIndividualData()
i5v5Data = load5v5IndividualData()
iPPData = loadPPIndividualData()
iPKData = loadPKIndividualData()

# Merge Datasets (this section may still end up being used)
# playerData = mergePlayerData(summaryData, assistData)
# playerData = mergePlayerData(playerData, faceoffData)
# playerData = mergePlayerData(playerData, penaltyData)
# playerData = mergePlayerData(playerData, miscData)

playerAllData = allData # On-Ice is for later
player5v5Data = i5v5Data # On-Ice is for later
playerPPData = iPPData # On-Ice is for later
playerPKData = iPKData # On-Ice is for later


# Feed and manipulate the data for use
print ('Processing...')
processData()

# Plot data on Plot.ly
plotChart()

endTimer()