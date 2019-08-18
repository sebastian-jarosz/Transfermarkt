from Scripts.Match.MatchesFromQueue import getMatchesFormQueue
from Scripts.Match.EventsFromMatch import getEventsFromMatch
import pandas as pd
import time
import pandas as pd
from pathlib import Path
import os
from sys import platform
import PySimpleGUI as sg
if platform == "darwin":
    import caffeine


def generateEventsFromQueue(leagueName, saison, queueNumber, queueHyperlink):
    sg.Popup("Start of export")
    print("Start of export for " + leagueName + " " + str(saison) + " " + str(queueNumber))
    if platform == "darwin":
        directory = os.environ['HOME'] + "/Desktop/Transfermarkt Export/" + str(saison) + "/" + leagueName + "/Matches"
        path = directory + "/" + str(queueNumber) + ".xlsx"
    if platform == "win32":
        directory = os.environ['HOMEPATH'] + "\Desktop\Transfermarkt Export\\" + str(saison) + "\\" + leagueName + "\Matches"
        path = directory + "\\" + str(queueNumber) + ".xlsx"
    matchesHyperlinks = getMatchesFormQueue(queueHyperlink)
    if not os.path.exists(directory):
        os.makedirs(directory)
    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    tempTable1 = []
    tempTable2 = []
    tempTable3 = []
    tempTable4 = []
    tempTable5 = []

    for i in range(0, len(matchesHyperlinks)):
        sg.OneLineProgressMeter('Export', i, len(matchesHyperlinks), 'key','Export of events from queue')
        print(matchesHyperlinks[i])
        time.sleep(1)
        tempPlayersInMatchIds, tempPlayersInMatchTimes, tempGoalsIds, tempAssistsIds = getEventsFromMatch(matchesHyperlinks[i], saison)
        tempTable1.extend(tempPlayersInMatchIds)
        tempTable2.extend(tempPlayersInMatchTimes) 
        tempTable3.append(tempGoalsIds) 
        tempTable4.append(tempAssistsIds)

    sg.OneLineProgressMeter('Export',  len(matchesHyperlinks), len(matchesHyperlinks), 'key','Export of events from queue')
    df1 = pd.DataFrame(tempTable1)
    df1['TIMES'] = tempTable2
    df2 = pd.DataFrame(tempTable3)
    df3 = pd.DataFrame(tempTable4)
    df1.to_excel(writer, "PLAYERSINMATCH")
    df2.to_excel(writer, "GOALS")
    df3.to_excel(writer, "ASSISTS")
    writer.save()
    print("End of export for " + leagueName + " " + str(saison) + " " + str(queueNumber))
    sg.Popup("End of export")  