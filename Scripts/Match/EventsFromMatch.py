import requests 
from bs4 import BeautifulSoup
import pandas as pd

def getEventsFromMatch(matchHyperlink):
	#For pretending being a browser
	headers = {'User-Agent': 
				'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

	page = matchHyperlink

	#Getting full page
	pageTree = requests.get(page, headers=headers)
	pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

	startingLineUpIdsTags = pageSoup.findAll("span", {"class" : ["aufstellung-rueckennummer-name","spielprofil_tooltip", "tooltipstered"]})
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


	startingLineUpIds = []
	goalsIds = []
	assistsIds = []
	outIds = []
	inIds = []

	for IdTag in startingLineUpIdsTags:
		startingLineUpIds.append(IdTag["id"])

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

	for i in range(0,len(outPlayerTags)):
		outIds.append((outPlayerTags[i])['id'])

	for i in range(0,len(inPlayerTags)):
		inIds.append((inPlayerTags[i])['id'])

	return startingLineUpIds, goalsIds, assistsIds, inIds, outIds




