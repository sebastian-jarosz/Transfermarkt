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
recordsPlayersFromTeams = p.map(findPlayersFromTeam, teamHyperlinks)
p.terminate()
p.join()

print(recordsPlayersFromTeams[3][2])


p = Pool(50)
recordsAttributes = p.map(findPlayerAttributes, recordsPlayersFromTeams[3][2])
p.terminate()
p.join()

print(recordsAttributes[0])
# teamIds, teamNames, teamHyperlinks = findTeamsFromLeague(hyperlinks[6])
