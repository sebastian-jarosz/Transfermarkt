import requests 
from bs4 import BeautifulSoup
import pandas as pd
from Scripts.Match.EventsFromMatch import getEventsFromMatch
from Scripts.Player.AttributesFromPlayer import findPlayerAttributes

playersInMatchIds, playersInMatchTimes, goalsIds, assistsIds = getEventsFromMatch("https://www.transfermarkt.com/spielbericht/index/spielbericht/3192608", "2019_2020")
print(playersInMatchIds)
print(playersInMatchTimes)