import os
import requests 
from bs4 import BeautifulSoup
import pandas as pd
import codecs


 #For pretending being a browser
headers = {'User-Agent': 
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

#1580 line
f=codecs.open("transfermarkt.html", 'r')
    
#Getting full page
# pageTree = requests.get(f.read(), headers=headers)
pageSoup = BeautifulSoup(f, 'html.parser')

countryNames = []

countriesList = pageSoup.find("select", {"data-placeholder" : "Country"}).find_all('option')

print(countriesList)

for country in countriesList:
    print(country)
