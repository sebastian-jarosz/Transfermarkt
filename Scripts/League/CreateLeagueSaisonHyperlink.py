
def generateLeagueSaisonHyperlink(leagueHyperlink, year):
    leagueSaisonHyperlink = leagueHyperlink + "/plus/?saison_id=" + str(year)
    return leagueSaisonHyperlink

def generateLeagueSaisonQueueHyperlink(leagueHyperlink, year, queueNumber):
    leagueSaisonHyperlink = generateLeagueSaisonHyperlink(leagueHyperlink, year)
    leagueSaisonHyperlink = leagueSaisonHyperlink.replace("startseite", "spieltag")
    leagueSaisonQueueHyperlink = leagueSaisonHyperlink + "&spieltag=" + str(queueNumber)
    return leagueSaisonQueueHyperlink   