import requests 
from bs4 import BeautifulSoup

import pandas as pd

#For pretending being a browser
headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

page = "https://www.transfermarkt.pl/1-liga/spieltag/wettbewerb/PL2/saison_id/2018/spieltag/1"

#Getting full page
pageTree = requests.get(page, headers=headers)
pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

Players = pageSoup.find_all("span", {"class": "hide-for-small"})
PlayersList = []

for i in range(0, len(Players)):
    print(Players[i].text)
