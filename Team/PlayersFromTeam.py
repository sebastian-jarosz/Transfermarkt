import requests 
from bs4 import BeautifulSoup
import pandas as pd


def findPlayersFromTeam(teamHyperlink):
    #For pretending being a browser
    headers = {'User-Agent': 
               'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    #verein/teamid/season_id/year
    #page = "https://www.transfermarkt.com/miedz-legnica/startseite/verein/8936/saison_id/2019"

    #Getting full page
    pageTree = requests.get(teamHyperlink, headers=headers)
    pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

    table = pageSoup.find("div", {"id":"yw1"})

    fullNameTags = table.find_all("span", {"class" : "hide-for-small"})

    playerTags = []

    for fullNameTag in fullNameTags:
        playerTags.extend(fullNameTag.find_all("a", {"class":"spielprofil_tooltip"}))

    playerIds = []
    playerNames = []
    playerHyperlinks = []

    for playerTag in playerTags:
        playerIds.append((playerTag['href'].rsplit('/',1))[-1])
        playerNames.append(playerTag.text)
        playerHyperlinks.append("https://www.transfermarkt.com" + playerTag['href'])

    return playerIds, playerNames, playerHyperlinks
