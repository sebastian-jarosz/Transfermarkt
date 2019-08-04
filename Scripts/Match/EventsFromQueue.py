from Scripts.Match.MatchesFromQueue import getMatchesFormQueue
from Scripts.Match.EventsFromMatch import getEventsFromMatch
import pandas as pd
import time
import pandas as pd
from pathlib import Path
import os
from sys import platform
import caffeine
import PySimpleGUI as sg


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
    for i in range(0, len(matchesHyperlinks)):
        sg.OneLineProgressMeter('Export', i+1, len(matchesHyperlinks), 'key','Export of events from queue')
        print(matchesHyperlinks[i])
        time.sleep(1)
        tempStartingLineUpIds, tempGoalsIds, tempAssistsIds, tempInIds, tempOutIds = getEventsFromMatch(matchesHyperlinks[i])
        df1 = pd.DataFrame({"SQUAD" : tempStartingLineUpIds})
        df2 = pd.DataFrame({"GOAL" : tempGoalsIds})
        df3 = pd.DataFrame({"ASSIST" : tempAssistsIds})
        df4 = pd.DataFrame({"IN" : tempInIds})
        df5 = pd.DataFrame({"OUT" : tempOutIds})
        finalDf = pd.concat([df1,df2, df3, df4, df5], ignore_index=True, axis=1)
        finalDf.columns = ['SQUAD','GOAL','ASSIST', 'IN','OUT']
        finalDf.to_excel(writer, str(i+1))
    writer.save()
    sg.Popup("End of export")  