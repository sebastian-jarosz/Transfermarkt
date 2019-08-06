import requests

import PySimpleGUI as sg
from bs4 import BeautifulSoup
from Scripts.Team.PlayersFromTeam import findPlayersFromTeam
from Scripts.Team.TeamsFromLeague import findTeamsFromLeague
from Scripts.Player.AttributesFromPlayer import findPlayerAttributes
import time
import pandas as pd
from pathlib import Path
import os
from sys import platform
if platform == "darwin":
	import caffeine

def generateListOfPlayersFromLeague(leagueName, saison, LeagueHyperlink):
	sg.Popup("Start of export")
	teamIds, teamNames, teamHyperlinks = findTeamsFromLeague(LeagueHyperlink)

	playerIds = []
	playerNames = []
	playerTeams = []
	playerHyperlinks = []
	playerPositions = []
	playerAgents = []
	playerDatesOfBirth = []

	if platform == "darwin":
		directory = os.environ['HOME'] + "/Desktop/Transfermark Export/" + str(saison) + "/" + leagueName
		path = directory + "/Players.xlsx"
	if platform == "win32":
		directory = os.environ['HOMEPATH'] + "\Desktop\Transfermark Export\\" + str(saison) + "\\" + leagueName
		path = directory + "\Players.xlsx"
	if not os.path.exists(directory):
		os.makedirs(directory)
	for i in range(0,len(teamHyperlinks)):
		tempIds, tempNames, tempHyperlinks = findPlayersFromTeam(teamHyperlinks[i])
		sg.OneLineProgressMeter('Export', i, len(teamHyperlinks), 'key','Export of players from teams')
		tempTeamName = teamNames[i]
		print("Start of import for " + teamNames[i])
		for j in range(0, (len(tempIds))):
			playerTeams.append(tempTeamName)
			time.sleep(1)
			tempDateOfBirth, tempPosition, tempAgent = findPlayerAttributes(tempHyperlinks[j])
			playerDatesOfBirth.append(tempDateOfBirth)
			playerPositions.append(tempPosition)
			playerAgents.append(tempAgent)
		print("End of import for " + teamNames[i])
		playerIds.extend(tempIds)
		playerNames.extend(tempNames)
		playerHyperlinks.extend(tempHyperlinks)
	
	sg.OneLineProgressMeter('Export',  len(teamHyperlinks), len(teamHyperlinks), 'key','Export of players from teams')
	df = pd.DataFrame({"ID":playerIds,"NAME":playerNames, "TEAM":playerTeams,"HYPERLINK":playerHyperlinks, "DATE OF BIRTH":playerDatesOfBirth, "POSITION":playerPositions, "AGENT":playerAgents})
	df.to_excel(path)
	
	sg.Popup("End of export")

