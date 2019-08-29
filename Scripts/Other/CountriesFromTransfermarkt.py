import os
import requests 
from bs4 import BeautifulSoup
import pandas as pd
import codecs
import json


def getCountriesFromTransfermarkt():
    #For pretending being a browser
    headers = {'User-Agent': 
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    #1580 line
    htmlpath = os.path.realpath(__file__)
    htmlpath = htmlpath.rsplit('/', 1)[0] + "/transfermarkt.html"

    f=codecs.open(htmlpath, 'r', encoding='utf-8', errors=' ignore')

    countries = []

    #Getting full page
    # pageTree = requests.get(f.read(), headers=headers)
    pageSoup = BeautifulSoup(f, 'html.parser')

    countryNames = []


    countriesList = pageSoup.find("select", {"data-placeholder" : "Country"}).find_all('option')

    del countriesList[0] #delete empty record

    for country in countriesList:
        tempCountry = {}
        tempCountry['id'] = country['value']
        tempCountry['name'] = country.text
        tempCountry['hyperlink'] = 'https://www.transfermarkt.com/wettbewerbe/national/wettbewerbe/' + country['value']
        countries.append(tempCountry)

    for country in countries:
        country['test'] = 'dupsko'

    return countries