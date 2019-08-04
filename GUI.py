import PySimpleGUI as sg
import datetime
from Scripts.League.PlayersFromLeague import generateListOfPlayersFromLeague
from Scripts.League.CreateLeagueSaisonHyperlink import *
from Scripts.Match.EventsFromQueue import generateEventsFromQueue
import os
from sys import platform

#GUI VARIABLES

#Leagues
LEAGUENAMES = ['Ekstraklasa', 'I liga', 'II liga', 'III liga - I Grupa', 'III liga - II Grupa', 'III liga - III Grupa', 'III liga - IV Grupa']

LEAGUEMAP = {'Ekstraklasa' : 'https://www.transfermarkt.com/jumplist/startseite/wettbewerb/PL1',
             'I liga' : 'https://www.transfermarkt.com/jumplist/startseite/wettbewerb/PL2',
             'II liga' : 'https://www.transfermarkt.com/jumplist/startseite/wettbewerb/PL2L',
             'III liga - I Grupa' : 'https://www.transfermarkt.com/jumplist/startseite/wettbewerb/PL31',
             'III liga - II Grupa' : 'https://www.transfermarkt.com/jumplist/startseite/wettbewerb/PL32',
             'III liga - III Grupa' : 'https://www.transfermarkt.com/jumplist/startseite/wettbewerb/PL33',
             'III liga - IV Grupa' : 'https://www.transfermarkt.com/jumplist/startseite/wettbewerb/PL34'}

#Get 10 years from this year
SEASONS = []
year = datetime.datetime.today().year
for i in range(0, 10):
    tempSeason = str(year - i) + '/' + str(year - i +1)
    SEASONS.append(tempSeason)

#Queues    
QUEUES = []
for i in range(1, 38):
    QUEUES.append(i)
	
if platform == "darwin":
		image = os.environ['HOME'] + "/Desktop/GitLab/Transfermarkt/Transfermarkt/GUI/Logo.png"
if platform == "win32":
		image = os.environ['HOMEPATH'] + "\Desktop\MyProjects\Transfermarkt\GUI\Logo.png"	

tab1_layout =  [[sg.Text("League"), sg.Combo(LEAGUENAMES, size=(100,100), readonly="True")],
                [sg.Text("Season"), sg.Combo(SEASONS, size=(100,100), readonly="True")],
                [sg.ReadButton('Export players')]]

tab2_layout = [[sg.Text("League"), sg.Combo(LEAGUENAMES, size=(100,100), readonly="True")],
               [sg.Text("Season"), sg.Combo(SEASONS, size=(100,100), readonly="True")],
               [sg.Text("Queue"), sg.Combo(QUEUES, size=(100,100), readonly="True")],
               [sg.ReadButton('Export matches')]]

layout = [[sg.Image(image, 
           pad=(100, 0))],
          [sg.TabGroup([[sg.Tab('Players from league', tab1_layout),
                         sg.Tab('Matches from queue', tab2_layout)]], pad=((100, 100), (100,100)))],
          [sg.Exit()]]

window = sg.Window('S4S Transfermarkt Data Manager').Layout(layout)

while True:
    event, values = window.Read()
    if event is None or event == 'Exit':
        break
    elif event == 'Export players':
        generateListOfPlayersFromLeague(values[1], values[2].replace('/', '_'), generateLeagueSaisonHyperlink(LEAGUEMAP[values[1]], values[2].split('/')[0]))
    elif event == 'Export matches':
        generateEventsFromQueue(values[5], generateLeagueSaisonQueueHyperlink(LEAGUEMAP[values[3]],values[4].split('/')[0], values[5]))
