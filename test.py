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
from Scripts.Match.EventsFromMatch import *

playersInMatchIds, playersInMatchTimes, goalsIds, assistsIds = getEventsFromMatchPool('https://www.transfermarkt.com/spielbericht/index/spielbericht/3210731', '2019_2020')
print(playersInMatchIds)
print(playersInMatchTimes)

# match = "https://www.transfermarkt.com/a/leistungsdatendetails/spieler/155202/plus/0?saison=2019&verein=&liga=&wettbewerb=&pos=&trainer_id=3061999"

# print(getMinutesFromPlayer(match))