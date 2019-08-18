import requests 
from bs4 import BeautifulSoup
import pandas as pd
import time

def getEventsFromMatch(matchHyperlink, saison):
	#For pretending being a browser
	headers = {'User-Agent': 
				'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

	page = matchHyperlink
	matchId = matchHyperlink.rsplit('/', 1)[1]

	#Getting full page
	pageTree = requests.get(page, headers=headers)
	pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

	startingLineUpIdsTags = pageSoup.findAll("span", {"class" : ["aufstellung-rueckennummer-name","spielprofil_tooltip", "tooltipstered"]})
	if(len(startingLineUpIdsTags) == 0):	
		startingLineUpTags = pageSoup.find("h2", text="Line-Ups").parent.parent
		startingLineUpIdsTags = startingLineUpTags.findAll("a", {"class" : ["spielprofil_tooltip", "tooltipstered"]})
	goalTableTags = pageSoup.find("div", {"id" : "sb-tore"})
	substitutionsTableTags = pageSoup.find("div", {"id":"sb-wechsel"})
	try:
		goalPlayersTags = goalTableTags.findAll("a", {"class" : "wichtig"})
	except:
		goalPlayersTags = []	
	outPlayerSpanTags = substitutionsTableTags.findAll("span", {"class" : "sb-aktion-wechsel-aus"})
	inPlayerSpanTags = substitutionsTableTags.findAll("span", {"class" : "sb-aktion-wechsel-ein"})

	outPlayerTags = []
	inPlayerTags = []


	playersInMatchIds = []
	playersInMatchTimes = []
	startingLineUpIds = []
	startingLineUpsTimes = []
	goalsIds = []
	assistsIds = []
	inIds = []
	inTimes = []

	for idTag in startingLineUpIdsTags:
		time.sleep(1)
		playerLink = "https://www.transfermarkt.com/a/leistungsdatendetails/spieler/" + idTag['id'] + "/plus/0?saison=" + saison.split('_')[0] + "&verein=&liga=&wettbewerb=&pos=&trainer_id="
		playerPageTree = requests.get(playerLink, headers=headers)
		playerPageSoup = BeautifulSoup(playerPageTree.content, 'html.parser')
		minutes = playerPageSoup.find("a", {"id" : matchId}).findParent().findParent().find("td", {"class":"rechts"}).getText().split('\'')[0]
		startingLineUpIds.append(idTag['id'])
		startingLineUpsTimes.append(minutes)

	for i in range(0, len(goalPlayersTags)):
		#if even number
		if (i % 2 == 0):
			goalsIds.append((goalPlayersTags[i])['id'])
		#if odd number	
		else:	
			assistsIds.append((goalPlayersTags[i])['id'])

	for outPlayerSpanTag in outPlayerSpanTags:
		outPlayerTags.extend(outPlayerSpanTag.findAll("a", {"class" : "wichtig"}))

	for inPlayerSpanTag in inPlayerSpanTags:
		inPlayerTags.extend(inPlayerSpanTag.findAll("a", {"class" : "wichtig"}))

	for i in range(0,len(inPlayerTags)):
		time.sleep(1)
		playerLink = "https://www.transfermarkt.com/a/leistungsdatendetails/spieler/" + (inPlayerTags[i])['id'] + "/plus/0?saison=" + saison.split('_')[0] + "&verein=&liga=&wettbewerb=&pos=&trainer_id="
		playerPageTree = requests.get(playerLink, headers=headers)
		playerPageSoup = BeautifulSoup(playerPageTree.content, 'html.parser')
		minutes = playerPageSoup.find("a", {"id": matchId}).findParent().findParent().find("td", {"class":"rechts"}).getText().split('\'')[0]
		inIds.append((inPlayerTags[i])['id'])
		inTimes.append(minutes)


	playersInMatchIds.extend(startingLineUpIds)	
	playersInMatchIds.extend(inIds)
	playersInMatchTimes.extend(startingLineUpsTimes)
	playersInMatchTimes.extend(inTimes)	

	return playersInMatchIds, playersInMatchTimes, goalsIds, assistsIds




