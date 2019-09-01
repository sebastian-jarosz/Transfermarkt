import os
import requests 
from bs4 import BeautifulSoup
import pandas as pd
import codecs
import json
from Scripts.Other.CountriesFromTransfermarkt import *

COUNTRIES = []
LEAGUES = []
countriesJSON = getCountriesFromFile()
for country in countriesJSON.keys():
    COUNTRIES.append(country)
    tempLeagues = []
    for league in countriesJSON[country]['leagues']:
        tempLeagues.append(league['name'])
    
    print(country)
    for league in tempLeagues:
        print(league)
    print()
     


