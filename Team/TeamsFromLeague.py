import requests 
from bs4 import BeautifulSoup

import pandas as pd

#For pretending being a browser
headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

#verein/teamid/season_id/year
page = "https://www.transfermarkt.com/jumplist/startseite/wettbewerb/PL2L"

#Getting full page
pageTree = requests.get(page, headers=headers)
pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

table = pageSoup.find("div", {"id":"yw1"})

fullTeamTags = table.find_all("td", {"class" : "hide-for-small"})

teamTags = []

for fullTeamTag in fullTeamTags:
    teamTags.extend(fullTeamTag.find_all("a", {"class":"vereinprofil_tooltip"}))

teamNames = []
teamHyperlinks = []

for teamTag in teamTags:
    teamNames.append(teamTag.text)
    teamHyperlinks.append("https://www.transfermarkt.com" + teamTag['href'])

for teamName in teamNames:
    print(teamName)

for teamHyperlink in teamHyperlinks:
    print(teamHyperlink)
    