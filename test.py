import os
import requests 
from bs4 import BeautifulSoup
import pandas as pd
import codecs
import json
from multiprocessing import Pool
from Scripts.Other.CountriesFromTransfermarkt import *
from Scripts.Other.LeaguesFromCountries import get_leagues_from_country
from Scripts.Team.TeamsFromLeague import findTeamsFromLeague
from Scripts.Team.PlayersFromTeam import findPlayersFromTeam
from Scripts.Player.AttributesFromPlayer import findPlayerAttributes
from Scripts.Match.EventsFromMatch import *
from Scripts.Match.EventsFromQueue import *


# print(checkIfQueueFileExist("Poland", "Ekstraklasa", "2019_2020", 1))

# for i in range(1, 9):
#     print(i)
#     print(i)

get_countries_from_transfermarkt()
# playersInMatchIds, playersInMatchTimes, goalsIds, assistsIds = getEventsFromMatchPool('https://www.transfermarkt.com/spielbericht/index/spielbericht/3210731', '2019_2020')
# print(playersInMatchIds)
# print(playersInMatchTimes)

# queueHyperlink = 'https://www.transfermarkt.com/pko-ekstraklasa/spieltag/wettbewerb/PL1/plus/?saison_id=2019&spieltag=1'

# generateEventsFromQueue('Poland', 'Ekstraklasa', '2019_2020', 1, queuehyperlink)

# print(getMatchesFormQueue(queuehyperlink))

# match = "https://www.transfermarkt.com/a/leistungsdatendetails/spieler/155202/plus/0?saison=2019&verein=&liga=&wettbewerb=&pos=&trainer_id=3061999"

# print(getMinutesFromPlayer(match))

#For pretending being a browser

# headers = {'User-Agent': 
#             'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

# page = queueHyperlink

#Getting full page
# pageTree = requests.get(page, headers=headers)
# pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

# allMatchesTags = pageSoup.findAll("a", {"title" : "Match Sheet"})

# print(allMatchesTags)

# matchHyperlinks = []

# for matchTag in allMatchesTags:
#     matchHyperlinks.append("https://www.transfermarkt.com" + matchTag['href'])

# print(matchHyperlinks)