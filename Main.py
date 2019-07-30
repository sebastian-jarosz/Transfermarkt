import requests

from bs4 import BeautifulSoup
from Team.PlayersFromTeam import findPlayersFromTeam
from Team.TeamsFromLeague import findTeamsFromLeague
from Player.AttributesFromPlayer import findPlayerAttributes
import time
import pandas as pd

ekstraklasa = "https://www.transfermarkt.com/jumplist/startseite/wettbewerb/PL1"
firstLeague = "https://www.transfermarkt.pl/jumplist/startseite/wettbewerb/PL2"
secondLeague = "https://www.transfermarkt.pl/jumplist/startseite/wettbewerb/PL2L"

teamIds, teamNames, teamHyperlinks = findTeamsFromLeague(ekstraklasa)

playerIds = []
playerNames = []
playerTeams = []
playerHyperlinks = []
playerPositions = []
playerAgents = []
playerDatesOfBirth = []

for i in range(0,len(teamHyperlinks)):
	tempIds, tempNames, tempHyperlinks = findPlayersFromTeam(teamHyperlinks[i])
	tempTeamName = teamNames[i]
	print("Staring of import for " + teamNames[i])
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
	

df = pd.DataFrame({"ID":playerIds,"NAME":playerNames, "TEAM":playerTeams,"HYPERLINK":playerHyperlinks, "DATE OF BIRTH":playerDatesOfBirth, "POSITION":playerPositions, "AGENT":playerAgents})
df.to_excel("test.xlsx")

