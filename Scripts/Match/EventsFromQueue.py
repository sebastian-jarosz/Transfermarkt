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


def generateEventsFromQueue(queueNumber, queueHyperlink):
    print("Start of export")
    matchesHyperlinks = getMatchesFormQueue(queueHyperlink)
    writer = pd.ExcelWriter(str(queueNumber) + '.xlsx', engine='xlsxwriter')
    for i in range(0, len(matchesHyperlinks)):
        sg.OneLineProgressMeter('Export', i+1, len(matchesHyperlinks), 'key','Export of events from queue')
        print(matchesHyperlinks[i])
        time.sleep(1)
        tempStartingLineUpIds, tempGoalsIds, tempAssistsIds, tempInIds, tempOutIds = getEventsFromMatch(matchesHyperlinks[i])
        df1 = pd.DataFrame(tempStartingLineUpIds)
        print(tempStartingLineUpIds)
        df2 = pd.DataFrame(tempGoalsIds)
        df3 = pd.DataFrame(tempAssistsIds)
        df4 = pd.DataFrame(tempInIds)
        df5 = pd.DataFrame(tempOutIds)
        finalDf = pd.concat([df1,df2, df3, df4, df5], ignore_index=True, axis=1)
        finalDf.to_excel(writer, str(i+1))
    writer.save()
    print("End of export")   