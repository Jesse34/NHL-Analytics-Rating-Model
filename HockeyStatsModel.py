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
defenceRatingList = []

# Open and Load json data
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
        if (player['Shots'] >= 80):

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

            nameList.append(s.name)
            gamesPlayedList.append(s.games)
            teamList.append(s.team)

            evGoalsList.append(s.goals5v5)

            fAssistsList.append(s.fAssists5v5)
            sAssistsList.append(s.sAssists5v5)
            print ('\nName: ' + s.name + ', GP: (' + str(s.games) + ') Team: (' + str(s.team) + ')\ni5v5Data:' + ' 5v5G: (' + str(s.goals5v5) + ') 5v5 1st A: (' + str(s.fAssists5v5) + ') 5v5 2nd A: (' + str(s.sAssists5v5) + ')')
            print (s.name + ' ' + s.team)
            print(s.calcOffensiveRating())
            offenceRatingList.append(s.calcOffensiveRating())

    for player in iPPData:
        for s in skaterList:
            if (player['Player'] == s.name):
                s.ppGoals = player['Goals']
                s.ppAssists = player['Total Assists']
                s.badPenalties += player['Total Penalties']

    for player in iPPData:
        for s in skaterList:
            if (player['Player'] == s.name):
                s.ppGoals = player['Goals']
                s.ppAssists = player['Total Assists']
                s.badPenalties += player['Total Penalties']

    skaterList.sort(key=lambda x: x.offensiveRating, reverse=True)
    for x in skaterList:
        print(x)

# Configure the settings for the chart and sent the data to Plot.ly
def plotChart():
    print ('Plotting...')

    # Traces
    traceOffence = go.Bar(
        x=nameList,
        y=offenceRatingList,
        name='Offensive Rating'
    )
    traceDefence = go.Bar(
        x=nameList,
        y=fAssistsList,
        name='5v5 1st Assists'
    )
    traceGrit = go.Bar(
        x=nameList,
        y=sAssistsList,
        name='5v5 2nd Assists'
    )

    layout = go.Layout(
        barmode='stack',
        title=go.layout.Title(
            text='N.U.T.S (Numbers Used to Simplify)',
            x=0

        )
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
i5v5Data = load5v5IndividualData()
iPPData = loadPPIndividualData()
iPKData = loadPKIndividualData()

# Merge Datasets (this section may still end up being used)
# playerData = mergePlayerData(summaryData, assistData)
# playerData = mergePlayerData(playerData, faceoffData)
# playerData = mergePlayerData(playerData, penaltyData)
# playerData = mergePlayerData(playerData, miscData)

player5v5Data = i5v5Data # On-Ice is for later
playerPPData = iPPData # On-Ice is for later
playerPKData = iPKData # On-Ice is for later


# Feed and manipulate the data for use
print ('Processing...')
processData()

# Plot data on Plot.ly
plotChart()

endTimer()