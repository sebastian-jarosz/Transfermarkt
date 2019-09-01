import os
import requests 
from bs4 import BeautifulSoup
import pandas as pd
import codecs
import json
from Scripts.Other.LeaguesFromCountries import getLeaguesFromCountry


def getCountriesFromTransfermarkt():
    #For pretending being a browser
    headers = {'User-Agent': 
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    #1580 line
    htmlpath = os.path.realpath(__file__)
    htmlpath = htmlpath.rsplit('/', 1)[0] + "/transfermarkt.html"

    f=codecs.open(htmlpath, 'r', encoding='utf-8', errors=' ignore')

    countries = {}

    #Getting full page
    # pageTree = requests.get(f.read(), headers=headers)
    pageSoup = BeautifulSoup(f, 'html.parser')

    countriesList = pageSoup.find("select", {"data-placeholder" : "Country"}).find_all('option')

    #When want more countries need to be added here
    neededCountries = ['Poland', 'Latvia', 'Lithuania', 'Serbia', 'Croatia', 'Czech Republic', 'Slovakia', 'Austria']

    del countriesList[0] #delete empty record

    for country in countriesList:
        tempCountry = {}
        tempCountry['id'] = country['value']
        tempCountry['name'] = country.text
        if tempCountry['name'] in neededCountries:
            tempCountry['hyperlink'] = 'https://www.transfermarkt.com/wettbewerbe/national/wettbewerbe/' + country['value']
            tempCountry['leagues'] = getLeaguesFromCountry(tempCountry['hyperlink'])
            countries[country.text] = tempCountry  

    with open(htmlpath.rsplit('/', 1)[0] + '/data.txt', 'w') as outfile:
        json.dump(countries, outfile)

def getCountriesFromFile():
    htmlpath = os.path.realpath(__file__)
    f=codecs.open(htmlpath.rsplit('/', 1)[0] + '/data.txt', 'r', encoding='utf-8', errors=' ignore')
    countries = json.load(f)  
    return countries