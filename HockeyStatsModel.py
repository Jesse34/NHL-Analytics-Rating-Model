import json
import requests
import plotly
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
# def mergePlayerData(data1,data2):
#     for player1 in data1:
#         for player2 in data2:
#             if (player1['playerId'] == player2['playerId']):
#                 player1.update(player2)
#     return data1

# Process the data into a usable state

def processData():
    for player in allData:
        s = Skater(player['Player'], player['Team'][-3:], player['Position'], player['GP'])  # [-3:] Ensures that players with multiple teams only return the most recent team
        skaterList.append(s)
        
    for player in player5v5Data:
        for s in skaterList:
            if (player['Player'] == s.name):
        
                s.toi5v5 = player['TOI']
                s.goals5v5 = player['Goals']
                s.fAssists5v5 = player['First Assists']
                s.sAssists5v5 = player['Second Assists']
                s.shots5v5 = player['Shots']
                s.iPointPercentage = player['IPP']
        
                s.ixG = player['ixG']
                s.iCF = player['iCF']
                s.iFF = player['iFF']
                s.iSCF = player['iSCF']
                s.iHDCF = player['iHDCF']

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

    skaterList.sort(key=lambda x: x.offensiveRating, reverse=True)
    for s in skaterList:
        if (s.offensiveRating > 11 and s.toiALL > 1200):
            nameList.append(s.name)
            toiAllList.append(s.toiALL)
            evOffenceRatingList.append('{0:.3f}'.format(s.evOffensiveRating))
            ppOffenceRatingList.append('{0:.3f}'.format(s.ppOffensiveRating))
            pkOffenceRatingList.append('{0:.3f}'.format(s.pkOffensiveRating))
            print(s)


# Configure the settings for the chart and sent the data to Plot.ly
def plotChart():
    print ('Plotting...')

    # Traces
    traceOffence = go.Bar(
        x=nameList,
        y=evOffenceRatingList,
        name='5v5 Offense Rating',
        marker=dict(
            color='rgb(22, 50, 116)'
        )
    )
    traceDefence = go.Bar(
        x=nameList,
        y=ppOffenceRatingList,
        name='PP Offense Rating',
        marker=dict(
            color='rgb(10, 136, 38)'
        )
    )
    traceGrit = go.Bar(
        x=nameList,
        y=pkOffenceRatingList,
        name='PK Offense Rating',
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
        xaxis = dict(tickangle=-35)
    )
    data = [traceOffence, traceDefence, traceGrit]
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

# Plot data with matplotlib
#matPlotChart()



endTimer()