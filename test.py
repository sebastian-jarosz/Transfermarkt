import os
import requests 
from bs4 import BeautifulSoup
import pandas as pd
import codecs
import json
from multiprocessing import Pool
from Scripts.Other.CountriesFromTransfermarkt import *
from Scripts.Other.LeaguesFromCountries import getLeaguesFromCountry
from Scripts.Team.TeamsFromLeague import findTeamsFromLeague
from Scripts.Team.PlayersFromTeam import findPlayersFromTeam
from Scripts.Player.AttributesFromPlayer import findPlayerAttributes

COUNTRIES = []
countriesJSON = getCountriesFromFile()
for country in countriesJSON.keys():
    COUNTRIES.append(country)

hyperlinks = []
for country in COUNTRIES:    
    hyperlinks.append(countriesJSON[country]['hyperlink'])
    print(country)

p = Pool(10)
records = p.map(getLeaguesFromCountry, hyperlinks)
p.terminate()
p.join()


leaguesHyperlinks = []

for record in records[5]:
    leaguesHyperlinks.append(record['hyperlink'])

print(leaguesHyperlinks[0])

teamIds, teamNames, teamHyperlinks = findTeamsFromLeague(leaguesHyperlinks[0])

p = Pool(50)
recordsTeamsWithPlayers = p.map(findPlayersFromTeam, teamHyperlinks)
p.terminate()
p.join()

# for r in recordsTeamsWithPlayers[3][2]:
#     print(r)
#     print((recordsTeamsWithPlayers[3][2]).index(r))


# print(recordsPlayersFromTeams[3][2])

testingAttr = []

for recordTeamWithPlayers in recordsTeamsWithPlayers:
    p = Pool(50)
    recordsAttributes = p.map(findPlayerAttributes, recordTeamWithPlayers[2])
    p.terminate()
    p.join()
    for i in recordsAttributes:
        print(i[3])