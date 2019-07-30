import PySimpleGUI as sg
from Test import printGowno
from Scripts.League.PlayersFromLeague import generateListOfPlayersFromLeague

layout = [[sg.Button('Export players'), sg.Button('Exit')]]

window = sg.Window('Window Title', layout)

while True:                 
  event, values = window.Read()
  if event is None or event == 'Exit':
      break
  if event == 'Export players':
      generateListOfPlayersFromLeague("https://www.transfermarkt.com/jumplist/startseite/wettbewerb/PL1")

window.Close()