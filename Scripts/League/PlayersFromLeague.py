import requests

import PySimpleGUI as sg
from bs4 import BeautifulSoup
from Scripts.Team.PlayersFromTeam import findPlayersFromTeam
from Scripts.Team.TeamsFromLeague import findTeamsFromLeague
from Scripts.Player.AttributesFromPlayer import findPlayerAttributes
from multiprocessing import Pool
import time
import pandas as pd
from pathlib import Path
import os
from sys import platform
if platform == "darwin":
	import caffeine

def generateListOfPlayersFromLeague(countryName, leagueName, saison, LeagueHyperlink):
	sg.Popup("Start of export")
	teamIds, teamNames, teamHyperlinks = findTeamsFromLeague(LeagueHyperlink)

	playerIds = []
	playerNames = []
	playerTeams = []
	playerHyperlinks = []
	playerPositions = []
	playerFoots = []
	playerAgents = []
	playerDatesOfBirth = []

	if platform == "darwin":
		directory = os.environ['HOME'] + "/Desktop/Transfermarkt Export/" + countryName + "/"+ str(saison) + "/" + leagueName
		path = directory + "/Players.xlsx"
	if platform == "win32":
		directory = os.environ['HOMEPATH'] + "\Desktop\Transfermarkt Export\\" + countryName + "\\" + str(saison) + "\\" + leagueName
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
			time.sleep(1.5)
			tempDateOfBirth, tempPosition, tempAgent, tempFoot = findPlayerAttributes(tempHyperlinks[j])
			playerDatesOfBirth.append(tempDateOfBirth)
			playerPositions.append(tempPosition)
			playerFoots.append(tempFoot)
			playerAgents.append(tempAgent)
		print("End of import for " + teamNames[i])
		playerIds.extend(tempIds)
		playerNames.extend(tempNames)
		playerHyperlinks.extend(tempHyperlinks)
	
	sg.OneLineProgressMeter('Export',  len(teamHyperlinks), len(teamHyperlinks), 'key','Export of players from teams')
	df = pd.DataFrame({"ID":playerIds,"NAME":playerNames, "TEAM":playerTeams,"HYPERLINK":playerHyperlinks, "DATE OF BIRTH":playerDatesOfBirth, "POSITION":playerPositions, "FOOT":playerFoots, "AGENT":playerAgents})
	df.to_excel(path)
	
	sg.Popup("End of export")


def generateListOfPlayersFromLeaguePool(countryName, leagueName, saison, LeagueHyperlink):
	sg.Popup("Start of export")
	teamIds, teamNames, teamHyperlinks = findTeamsFromLeague(LeagueHyperlink)

	playerIds = []
	playerNames = []
	playerTeams = []
	playerHyperlinks = []
	playerPositions = []
	playerFoots = []
	playerAgents = []
	playerDatesOfBirth = []

	if platform == "darwin":
		directory = os.environ['HOME'] + "/Desktop/Transfermarkt Export/" + countryName + "/"+ str(saison) + "/" + leagueName
		path = directory + "/Players.xlsx"
	if platform == "win32":
		directory = os.environ['HOMEPATH'] + "\Desktop\Transfermarkt Export\\" + countryName + "\\" + str(saison) + "\\" + leagueName
		path = directory + "\Players.xlsx"
	if not os.path.exists(directory):
		os.makedirs(directory)

	p = Pool(50)
	recordsTeamsWithPlayers = p.map(findPlayersFromTeam, teamHyperlinks)
	p.terminate()
	p.join()

	for recordTeamWithPlayers in recordsTeamsWithPlayers:
		tempTeamName = teamNames[recordsTeamsWithPlayers.index(recordTeamWithPlayers)] #getting index of record in all records pooled before
		print("Start of import for " + tempTeamName)
		p = Pool(50)
		recordsPlayersWithAttributes = p.map(findPlayerAttributes, recordTeamWithPlayers[2])
		p.terminate()
		p.join()
		for recordPlayerWithAttribudes in recordsPlayersWithAttributes:
			playerTeams.append(tempTeamName)
			playerDatesOfBirth.append(recordPlayerWithAttribudes[0])
			playerPositions.append(recordPlayerWithAttribudes[1])
			playerFoots.append(recordPlayerWithAttribudes[3])
			playerAgents.append(recordPlayerWithAttribudes[2])
		playerIds.extend(recordTeamWithPlayers[0])
		playerNames.extend(recordTeamWithPlayers[1])
		playerHyperlinks.extend(recordTeamWithPlayers[2])
		print("End of import for " + tempTeamName)
	
	df = pd.DataFrame({"ID":playerIds,"NAME":playerNames, "TEAM":playerTeams,"HYPERLINK":playerHyperlinks, "DATE OF BIRTH":playerDatesOfBirth, "POSITION":playerPositions, "FOOT":playerFoots, "AGENT":playerAgents})
	df.to_excel(path)
	
	sg.Popup("End of export")
