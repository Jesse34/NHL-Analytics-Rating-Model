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
    """Load JSON for Team Season Data in All Situations 2018-19"""
    with open('JSON\\Team Season Stats 2018-19.json') as f:
        allTeamData = json.load(f)
        return allTeamData
def load5v5TeamData():
    """Load JSON for Team Season Data at 5v5 (Even Strength) 2018-19"""
    with open('JSON\\5v5 Team Season Stats 2018-19.json') as f:
        team5v5Data = json.load(f)
        return team5v5Data
def loadAllIndividualData():
    """Load JSON for Player Data in All Situations 2018-19"""
    with open('JSON\\Total Individual Skater Stats 2018-19.json') as f:
        allSkaterData = json.load(f)
        return allSkaterData
def load5v5IndividualData():
    """Load JSON for Player Data at 5v5 (Even Strength) 2018-19"""
    with open('JSON\\5v5 Individual Skater Stats 2018-19.json') as f:
        i5v5Data = json.load(f)
        return i5v5Data
def loadPPIndividualData():
    """Load JSON for Player Data at 5v4 or 5-3 (Powerplay) 2018-19"""
    with open('JSON\\PP Individual Skater Stats 2018-19.json') as f:
        iPPData = json.load(f)
        return iPPData
def loadPKIndividualData():
    """Load JSON for Player Data at 4v5 or 3-5 (Penalty Kill) 2018-19"""
    with open('JSON\\PK Individual Skater Stats 2018-19.json') as f:
        iPKData = json.load(f)
        return iPKData

def processData():
    """
    Collects all of the data from different sources.
    Then Calculations are ran to gather each players Overall Offensive rating (and all other specific Offensive Ratings).
    The Player list is then sorts based on their overall rating to sort for display (Plot.ly cannot sort a stacked bar chart).
    Lastly, a filter is applied to select a specific dataset for display.
    """
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

    #Calculate Each Players Offensive Rating
    for s in skaterList:
        offenceRatingList.append(s.calcOffensiveRating())

    skaterList.sort(key=lambda x: x.offensiveRating, reverse=True)

    count = 0
    limit = 30

    # Data Selection Filter
    for s in skaterList:
        if (limit > count and s.toiALL > 1200 and s.position == "D"):
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
    """
    Utilizing the functions in the Plot.ly library, the data is organized to display the data in an appealing way.
    """
    print ('Plotting...\n')

    # Even Strength Traces
    tracePointOffence = go.Bar(
        x=nameList,
        y=evPointsRatingList,
        name='5v5 Point Scoring',
        marker=dict(
            color='rgb(22, 50, 116)'
        )
    )
    traceShotOffence = go.Bar(
        x=nameList,
        y=evShotsRatingList,
        name='5v5 Shot Contribution',
        marker=dict(
            color='rgb(22, 80, 156)'
        )
    )

    # Powerplay Traces
    tracePPPointOffence = go.Bar(
        x=nameList,
        y=ppPointsRatingList,
        name='PP Point Scoring',
        marker=dict(
            color='rgb(20, 136, 45)'
        )
    )
    tracePPShotOffence = go.Bar(
        x=nameList,
        y=ppShotsRatingList,
        name='PP Shot Contribution',
        marker=dict(
            color='rgb(20, 160, 50)'
        )
    )

    # Penalty Kill Traces
    tracePKPointOffence = go.Bar(
        x=nameList,
        y=pkPointsRatingList,
        name='PK Point Scoring',
        marker=dict(
            color='rgb(216, 21, 21)'
        )
    )
    tracePKShotOffence = go.Bar(
        x=nameList,
        y=pkShotsRatingList,
        name='PK Shot Contribution',
        marker=dict(
            color='rgb(255, 32, 52)'
        )
    )
    layout = go.Layout(
        barmode='stack',
        title=go.layout.Title(
            text='Offensive Efficiency (This currently ignores Quality of Teammates/Opponents)',
            x=0
        ),
        xaxis = dict(tickangle=-30)
    )
    data = [tracePointOffence, traceShotOffence, tracePPPointOffence, tracePPShotOffence, tracePKPointOffence, tracePKShotOffence]
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, file='player-model')

def endTimer():
    """
    Timer used for debugging to quickly catch issues that were costly to loading times.
    """
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

endTimer()