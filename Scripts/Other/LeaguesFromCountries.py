import os
import requests 
from bs4 import BeautifulSoup
import pandas as pd
import codecs
import json


def getLeaguesFromCountry(countryHyperlink):
    #For pretending being a browser
    headers = {'User-Agent': 
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    #verein/teamid/season_id/year

    #Getting full page
    pageTree = requests.get(countryHyperlink, headers=headers)
    pageSoup = BeautifulSoup(pageTree.content, 'html.parser')
    leagues = []
    leaguesTags = pageSoup.find('select', {'data-placeholder' :'Competition'}).findAll('option')
    del leaguesTags[0] #delete empty record

    for leagueTag in leaguesTags:
        league = {}
        league['id'] = leagueTag['value']
        league['name'] = leagueTag.text
        league['hyperlink'] = 'https://www.transfermarkt.com/jumplist/startseite/wettbewerb/' + league['id']
        if league['name'] not in ['ÖFB-Cup', 'Hrvatski nogometni kup', 'MOL Cup', 'Polish Cup', 'Superpuchar', 'Slovnaft Cup']:
            leagues.append(league)

    return leagues   
