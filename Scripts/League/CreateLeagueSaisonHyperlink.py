def generate_league_season_hyperlink(leagueHyperlink, year):
    league_season_hyperlink = leagueHyperlink + "/plus/?saison_id=" + str(year)
    return league_season_hyperlink


def generate_league_season_queue_hyperlink(leagueHyperlink, year, queueNumber):
    league_season_hyperlink = generate_league_season_hyperlink(leagueHyperlink, year)
    league_season_hyperlink = league_season_hyperlink.replace("startseite", "spieltag")
    league_season_queue_hyperlink = league_season_hyperlink + "&spieltag=" + str(queueNumber)
    return league_season_queue_hyperlink
