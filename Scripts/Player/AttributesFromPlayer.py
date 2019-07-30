import requests 
from bs4 import BeautifulSoup
import pandas as pd

import os

def findPlayerAttributes(playerHyperlink):
    #For pretending being a browser
    headers = {'User-Agent': 
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    
    page = playerHyperlink
    
    #Getting full page
    pageTree = requests.get(page, headers=headers)
    pageSoup = BeautifulSoup(pageTree.content, 'html.parser')
    
    #Get birthdate and trim left and right white signs
    dateOfBirth = pageSoup.find("span", {"itemprop" : "birthDate"}).text.strip().split('(')[0].strip()
    #Get span with text "Position:" then get next span with actual position of player, then stip spaces
    position = pageSoup.find("span", text="Position:").findNext("span").text.strip()
    #Get span with text "Agent:" then get next span with actual agent of player, then stip spaces (try in case there is an agent)
    try:
        agent = pageSoup.find("span", text="Agent:").findNext("a")["title"]
        if(agent.startswith("<span")):
            agent = agent.split("\"")[3]
    except:
        agent = "None"
    
    return dateOfBirth, position, agent
