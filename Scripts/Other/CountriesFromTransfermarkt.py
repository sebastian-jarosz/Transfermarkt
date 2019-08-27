import os
import requests 
from bs4 import BeautifulSoup
import pandas as pd


 #For pretending being a browser
headers = {'User-Agent': 
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

page = 'https://www.transfermarkt.com'
    
#Getting full page
pageTree = requests.get(page, headers=headers)
pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

countryNames = []

# countriesList = pageSoup.find("div", {"class" :["chzn-container", "chzn-container-single" , "chzn-container-active"]})
countriesList = pageSoup.find("select", {"id" : "land_select_breadcrumb"})
# test = countriesList.find("div", {"class" : "land_select_breadcrumb_chzn"})
print(countriesList)
