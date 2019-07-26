import requests

from bs4 import BeautifulSoup
from Team.PlayersFromTeam import findPlayersFromTeam
from Team.TeamsFromLeague import findTeamsFromLeague
import pandas as pd

ekstraklasa = "https://www.transfermarkt.pl/jumplist/startseite/wettbewerb/PL1"
firstLeague = "https://www.transfermarkt.pl/jumplist/startseite/wettbewerb/PL2"
secondLeague = "https://www.transfermarkt.pl/jumplist/startseite/wettbewerb/PL2L"

teamIds, teamNames, teamHyperlinks = findTeamsFromLeague(ekstraklasa)

playerIds = []
playerNames = []
playerTeams = []
playerHyperlinks = []

for i in range(0,len(teamHyperlinks)):
	tempIds, tempNames, tempHyperlinks = findPlayersFromTeam(teamHyperlinks[i])
	tempTeamName = teamNames[i]
	for j in range(0, (len(tempIds))):
		playerTeams.append(tempTeamName)
	playerIds.extend(tempIds)
	playerNames.extend(tempNames)
	playerHyperlinks.extend(tempHyperlinks)

df = pd.DataFrame({"ID":playerIds,"NAME":playerNames, "TEAM":playerTeams,"HYPERLINK":playerHyperlinks})
df.to_excel("test.xlsx")