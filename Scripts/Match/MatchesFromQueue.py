import requests 
from bs4 import BeautifulSoup
import pandas as pd


def getMatchesFormQueue(hyperlink):
    #For pretending being a browser
    headers = {'User-Agent': 
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    page = hyperlink

    #Getting full page
    pageTree = requests.get(page, headers=headers)
    pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

    allMatchesTags = pageSoup.findAll("a", {"class" : "ergebnis-link"})

    matchHyperlinks = []

    for matchTag in allMatchesTags:
        matchHyperlinks.append("https://www.transfermarkt.com" + matchTag['href'])

    return matchHyperlinks