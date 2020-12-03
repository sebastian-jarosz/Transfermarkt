import requests
from bs4 import BeautifulSoup
from Scripts.Team.PlayersFromTeam import find_players_from_team
import pandas as pd


def find_teams_from_league(hyperlink):
    # For pretending being a browser
    headers = {'User-Agent':
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    # verein/teamid/season_id/year
    page = hyperlink;

    # Getting full page
    page_tree = requests.get(page, headers=headers)
    page_soup = BeautifulSoup(page_tree.content, 'html.parser')

    table = page_soup.find("div", {"id": "yw1"})

    full_team_tags = table.find_all("td", {"class": "hide-for-small"})

    team_tags = []

    for fullTeamTag in full_team_tags:
        team_tags.extend(fullTeamTag.find_all("a", {"class": "vereinprofil_tooltip"}))

    team_ids = []
    team_names = []
    team_hyperlinks = []

    for teamTag in team_tags:
        team_ids.append((teamTag['href'].split('/'))[-3])
        team_names.append(teamTag.text)
        team_hyperlinks.append("https://www.transfermarkt.com" + teamTag['href'])

    return team_ids, team_names, team_hyperlinks
