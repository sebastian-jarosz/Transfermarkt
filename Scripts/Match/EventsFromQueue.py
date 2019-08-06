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
    print(queueHyperlink)
    if platform == "darwin":
        directory = os.environ['HOME'] + "/Desktop/Transfermark Export/" + leagueName + "/" + str(saison) + "/Matches"
        path = directory + "/" + str(queueNumber) + ".xlsx"
    if platform == "win32":
        directory = os.environ['HOMEPATH'] + "\Desktop\Transfermark Export\\" + leagueName + "\\" + str(saison) + "\Matches"
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
        tempStartingLineUpIds, tempGoalsIds, tempAssistsIds, tempInIds, tempOutIds = getEventsFromMatch(matchesHyperlinks[i])
        tempTable1.append(tempStartingLineUpIds)
        tempTable2.append(tempGoalsIds) 
        tempTable3.append(tempAssistsIds) 
        tempTable4.append(tempInIds) 
        tempTable5.append(tempOutIds)
    sg.OneLineProgressMeter('Export',  len(matchesHyperlinks), len(matchesHyperlinks), 'key','Export of events from queue')
    df1 = pd.DataFrame(tempTable1)
    df2 = pd.DataFrame(tempTable2)
    df3 = pd.DataFrame(tempTable3)
    df4 = pd.DataFrame(tempTable4)
    df5 = pd.DataFrame(tempTable5)
    df1.to_excel(writer, "SQUAD")
    df2.to_excel(writer, "GOALS")
    df3.to_excel(writer, "ASSISTS")
    df4.to_excel(writer, "IN")
    df5.to_excel(writer, "OUT")
    writer.save()
    sg.Popup("End of export")  