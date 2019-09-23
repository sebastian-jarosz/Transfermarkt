import os
import requests 
from bs4 import BeautifulSoup
import pandas as pd
import codecs
import json
from multiprocessing import Pool
from Scripts.Other.CountriesFromTransfermarkt import *

COUNTRIES = []
countriesJSON = getCountriesFromFile()
for country in countriesJSON.keys():
    COUNTRIES.append(country)

hyperlinks = []
for country in COUNTRIES:    
    hyperlinks.append(countriesJSON[country]['hyperlink'])
    print(country)

p = Pool(10)
records = p.map(getLeaguesFromCountry, hyperlinks)
p.terminate()
p.join()

for record in records:
    print(record)


