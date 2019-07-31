import PySimpleGUI as sg
import datetime
from Scripts.League.PlayersFromLeague import generateListOfPlayersFromLeague


#GUI VARIABLES
#Get 10 years from this year
YEARS = []
year = datetime.datetime.today().year
for i in range(0, 10):
    YEARS.append(year-i)

LEAGUENAMES = ['Ekstraklasa', 'I liga', 'II liga', 'III liga - I Grupa', 'III liga - II Grupa', 'III liga - III Grupa', 'III liga - IV Grupa']

LEAGUEMAP = {'Ekstraklasa' : 'https://www.transfermarkt.com/jumplist/startseite/wettbewerb/PL1',
             'I liga' : 'https://www.transfermarkt.com/jumplist/startseite/wettbewerb/PL2',
             'II liga' : 'https://www.transfermarkt.com/jumplist/startseite/wettbewerb/PL2L',
             'III liga - I Grupa' : 'https://www.transfermarkt.com/jumplist/startseite/wettbewerb/PL31',
             'III liga - II Grupa' : 'https://www.transfermarkt.com/jumplist/startseite/wettbewerb/PL32',
             'III liga - III Grupa' : 'https://www.transfermarkt.com/jumplist/startseite/wettbewerb/PL33',
             'III liga - IV Grupa' : 'https://www.transfermarkt.com/jumplist/startseite/wettbewerb/PL34'}


tab1_layout =  [[sg.Combo(LEAGUENAMES, size=(100,100), readonly="True")],
                 [sg.Combo(YEARS, size=(100,100), readonly="True")]]

tab2_layout = [[sg.Text('This is inside tab 2')]]

layout = [[sg.TabGroup([[sg.Tab('Players from league', tab1_layout),
                         sg.Tab('Matches from queue', tab2_layout)]])],
          [sg.ReadButton('Read'), sg.Exit()]]

window = sg.Window('S4S Transfermarkt Data Manager', size=(1000, 500)).Layout(layout)

while True:
    event, values = window.Read()
    if event is None or event == 'Exit':
        break
    elif event == 'Read':
        print(LEAGUEMAP[values[0]])
